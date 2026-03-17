# proxy.mcy — HTTP Forward Proxy with Rate Limiting

A lightweight HTTP forward proxy written in [Minimacy](https://minimacy.net). It enforces per-route rate limits and blocks unlisted URLs with HTTP 403.

Supports two proxy modes:
- **Plain HTTP proxy** — client sends the full absolute URL (`GET https://...`)
- **HTTPS CONNECT tunnel** — client sends `CONNECT host:port`, proxy relays raw bytes (used by curl, browsers, and most HTTP libraries for HTTPS)

## Run

```sh
./bin/minimacyMac programs/proxy.mcy [config.json]
```

The config file defaults to `proxy.json` in the current working directory.

## Configure

Create a JSON config file:

```json
{
  "port": 8080,
  "routes": [
    { "path": "https://api.openai.com/",    "rate": 5,  "window": 60 },
    { "path": "https://api.anthropic.com/", "rate": 10, "window": 60 }
  ]
}
```

| Field    | Description                                      |
|----------|--------------------------------------------------|
| `port`   | Port the proxy listens on                        |
| `path`   | URL prefix to allow (longest-prefix match)       |
| `rate`   | Max requests allowed per `window`                |
| `window` | Sliding window duration in seconds               |

CONNECT requests are matched by normalising `host:port` to `https://host:port/` before route lookup, so the same route table covers both modes.

## Use

Configure your HTTP client to route requests through the proxy.

**curl**
```sh
# HTTPS via CONNECT tunnel (recommended — works with all methods)
curl --proxy http://localhost:8080 https://api.openai.com/v1/models \
     -H "Authorization: Bearer $OPENAI_API_KEY"

# Plain HTTP proxy (absolute URL mode)
curl -x http://localhost:8080 https://api.openai.com/v1/models \
     -H "Authorization: Bearer $OPENAI_API_KEY"
```

**Python (requests)**
```python
import requests

proxies = {"https": "http://localhost:8080"}
response = requests.get("https://api.openai.com/v1/models",
                        headers={"Authorization": f"Bearer {api_key}"},
                        proxies=proxies)
```

**Environment variable (applies to most CLI tools)**
```sh
export https_proxy=http://localhost:8080
curl https://api.openai.com/v1/models -H "Authorization: Bearer $OPENAI_API_KEY"
```

## Responses

| Status | Meaning                                      |
|--------|----------------------------------------------|
| 200    | Request forwarded, upstream response returned |
| 403    | URL not in any configured route               |
| 429    | Rate limit exceeded for this route            |
| 502    | Upstream unreachable or DNS resolution failed |

Rate limit errors include details in the JSON body:

```json
{ "error": "rate limit exceeded", "limit": 5, "window": 60 }
```

## Limitations

- Request bodies with `Transfer-Encoding: chunked` (no `Content-Length`) are not supported; the body will be dropped. Standard API clients always use `Content-Length`, so this is rarely an issue.
- The CONNECT tunnel does not implement flow control; very large streaming responses may drop bytes if kernel buffers fill up.
