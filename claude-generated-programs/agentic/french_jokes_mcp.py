#!/usr/bin/env python3
"""
MCP Server for French Jokes.

Returns a random French joke via a single tool, served over streamable HTTP.
"""

import logging
import random
from mcp.server.fastmcp import FastMCP

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

mcp = FastMCP("french_jokes_mcp", port=8000)

JOKES = [
    ("Pourquoi les plongeurs plongent-ils toujours en arrière ?",
     "Parce que sinon ils tomberaient dans le bateau !"),
    ("Qu'est-ce qu'un canif ?",
     "Un petit fien !"),
    ("Pourquoi l'épouvantail a-t-il reçu un prix ?",
     "Parce qu'il était exceptionnel dans son domaine !"),
    ("Que dit un vampire quand il rit ?",
     "Mua ha ha !"),
    ("Pourquoi les vaches ont-elles des sabots ?",
     "Parce qu'elles n'ont pas de sous !"),
    ("Quel est le comble pour un électricien ?",
     "De ne pas être au courant !"),
    ("Pourquoi Napoléon portait-il toujours la main dans sa veste ?",
     "Parce qu'il avait mal au ventre !"),
    ("Que fait un canif ?",
     "Il fend l'air, et la blague aussi !"),
    ("Comment appelle-t-on un chat tombé dans un pot de peinture le jour de Noël ?",
     "Un chat-peint de Noël !"),
    ("Quel est le sport préféré des boulangers ?",
     "Le pain-athlon !"),
]


@mcp.tool(
    name="get_random_french_joke",
    annotations={
        "title": "Get a Random French Joke",
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": False,
        "openWorldHint": False,
    }
)
def get_random_french_joke() -> str:
    """Return a random French joke with its punchline.

    Returns:
        str: A French joke formatted as:
             Question: <setup>
             Réponse: <punchline>
    """
    logger.info("Tool called: get_random_french_joke")
    setup, punchline = random.choice(JOKES)
    response = f"Question : {setup}\nRéponse : {punchline}"
    logger.info("Response: %s", response)
    return response


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
