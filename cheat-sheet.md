
Note: `]` is the prefix used to show what you type. The rest is returned by the Minimacy compiler/interpreter.


## Lists (coming soon)

## Arrays (coming soon)

## Dictionaries (aka hashmap)

### New empty dictionary
You can create an empty dictionary, which comes with a generic (aka weak) type `a1 -> a2`.

```
] const D = hashmapCreate 10

> Compiler error: weak type warning
>   weak type pkg0.D: hashmap w1 -> w2
-> a1: CONST D
     Type: hashmap w1 -> w2
     hashmap #0 {
    }
```

Once you you insert your first element, a proper type gets assigned, e.g. `Str -> int`.
```
] hashmapSet D "pizza" 9
-> Int: 9 (0x9)

] D
-> hashmap Str -> Int: #1 {
     Str: "pizza"
   ->
     Int: 9 (0x9)
}
```

### New dictionary with some elements
You can also create dictionary with a list of key-value pairs.

```
] hashmapInit 10 ["pizza" 9]:["ice cream" 7]:nil
-> hashmap Str -> Int: #2 {
     Str: "ice cream"
   ->
     Int: 7 (0x7)
   ---
     Str: "pizza"
   ->
     Int: 9 (0x9)
}
```
The dictionary immediately gets its proper type.


Pairs need to be of the same type or you get an error.
```
] hashmapInit 10 ["pizza" 9]:["ice cream" 7.0]:nil

> Compiler error: '[Str Int]' does not match with '[Str Float]'
   global hashmapInit: fun Int list [a1 a2] -> (hashmap a1 -> a2)


> hashmapInit 10 ["pizza" 9]:["ice cream" 7.0]:nil;;
```

If the list if empty, this is equivalent to `hashmapCreate`.

```
hashmapInit 10 nil
-> hashmap a1 -> a2: #0 {
}
```

### get/set/count

```
] const D = hashmapInit 10 ["pizza" 5]:["ice cream" 7]:nil ; echoLn (hashmapGet D "pizza")
] echoLn (hashmapGet D "pizza") ;
hashmapSet D "salad" 4 ;;
```

and you can get the number of elements

```
] hashmapCount D
-> Int: 3 (0x3)
```

### Map
You can transform the dictionary into a list of pairs.

```
] listFromHashmap D
-> list [Str Int]:
    tuple #2 [
     0:
       Str: "tiramisu"
     1:
       Int: 1 (0x1)
  ]
    tuple #2 [
     0:
       Str: "pizza"
     1:
       Int: 5 (0x5)
  ]
    tuple #2 [
     0:
       Str: "ice cream"
     1:
       Int: 7 (0x7)
  ]
````

You can also do it "by hand" using the `hashmapMap` function: for key-value pair, return the tuple `[x y]`.
```
] hashmapMap D (lambda x y = [x y])
-> list [Str Int]:
    tuple #2 [
     0:
       Str: "tiramisu"
     1:
       Int: 1 (0x1)
  ]
    tuple #2 [
     0:
       Str: "pizza"
     1:
       Int: 5 (0x5)
  ]
    tuple #2 [
     0:
       Str: "ice cream"
     1:
       Int: 7 (0x7)
  ]
```

You can create your own pretty print function.
We iterate over the key-value pairs. For each pair, we create the string `key -> value`. We use `strBuild` to get a string from an arbitrary type. We use `strConcat` to concatenate the string.

```
fun hashmapPrint h = (strJoin "\n" (hashmapMap h (lambda x y = strConcat (strBuild x) (strConcat " -> " (strBuild y)))))
```
    
