patterns=[
    {
        "name":"nested_plus",
        "pattern":"(a+)+b",
        "generate":lambda n:"a"*n+"c"
    },
    {
        "name":"ambiguous_alternation",
        "pattern":"(a|aa)*b",
        "generate":lambda n:"a"*n+"c"
    }
]