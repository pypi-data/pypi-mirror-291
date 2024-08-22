# pybrastr Readme 📜
Brainstorming package to manage string

# Installation ⚡
Opérating system :  Windows, MacOS & Linux :

```sh
pip install pybrainutils
```

# Available function/class 📑
    quotedStr       :   Add simple quote at begin and end of string.
    dblQuotedStr    :   Add double quote at begin and end of string.
    strToIntDef     :   Convert str value to integer with default value if str is not an integer.

# How to use 📰
    impport pybrastr

    txt = 'BRAIN'
    txt2 = pybrastr.quotedStr(txt)
    txt3 = pybrastr.dblQuotedStr(txt2)
    int1 = pybrastr.strToIntDef(txt, 10)

    print(txt3 + ' ' + txt2 + ' ' + str(int1))
    print(pybrastr.version())

## Meta 💬
Brainstorming – Support.erp@brainstorming.eu

Distributed under the MIT license. See ``LICENSE`` for more information.