
Note: `]` is the prefix used to show what you type. The rest is returned by the Minimacy compiler/interpreter.


## Lists

List are represented as the head (the first element from the list) followed by the tail (the rest of the list). `nil` is used to represent the empty list.

### Constructing a list

You can create list using using the `:` operator. Note that a list must always end with `nil`.
```
] 1:2:nil
-> list Int:
   Int: 1 (0x1)
   Int: 2 (0x2)
```

Also, all elements of the list must be of the same type.
```
] 1:"2":nil

> Compiler error: 'Int' does not match with 'Str'
```

You can add an element to the head of the list using `:`.
```
] const A = 1:2:3:nil
-> a1: CONST A
     Type: list Int
     list:
       Int: 1 (0x1)
       Int: 2 (0x2)
       Int: 3 (0x3)
] 0:A
-> list Int:
   Int: 0 (0x0)
   Int: 1 (0x1)
   Int: 2 (0x2)
   Int: 3 (0x3)
```

To add an element at the end of the list you can use `listConcat`.
```
] listConcat A 4:nil
-> list Int:
   Int: 1 (0x1)
   Int: 2 (0x2)
   Int: 3 (0x3)
   Int: 4 (0x4)
```

### Deconstructing a list

You extract the first element of the list using `head`. You extract the rest (aka tail) of the list using `tail`. You can extract an element at a given `index` using `listGet`. If there is no such element, the function returns `nil`.

```
] head A
-> Int: 1 (0x1)

] tail A
-> list Int:
   Int: 2 (0x2)
   Int: 3 (0x3)

] listGet A 0
-> Int: 1 (0x1)         // Same as head A

] listGet A 2
-> Int: 3 (0x3)

] listGet A 3           // no such element --> nil
-> Int:  nil
```

### Mapping functions

You can find more details at https://minimacy.net/book/#/page/page:205 .


## Arrays (coming soon)



## Dictionaries (aka hashmap)

### New empty dictionary using `hashmapCreate`
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

### New dictionary with some elements using `hashmapInit`
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

### get/set/count using `hashmapGet`, `hashmapSet` and `hashmapCount`

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
    
