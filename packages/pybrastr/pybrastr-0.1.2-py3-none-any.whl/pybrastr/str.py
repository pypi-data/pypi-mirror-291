"""

    PyBrainUtils -- Copyright (C) 2024 Brainstorming S.A.
    List of function to manipulate strings
    
"""
import re

def quotedStr(aStr : str)->str:
    """QuotedStr Add simple quote at begin and end of string

    Parameters
    ----------
    aStr : str
        The string to add quotes

    Returns
    -------
    str
        The string with quotes
    """
    return '\''+ aStr + '\''

def dblQuotedStr(aStr : str)->str:
    """dblQuotedStr Add double quote at begin and end of string

    Parameters
    ----------
    aStr : str
        The string to add double quotes

    Returns
    -------
    str
        The string with double quotes
    """
    value = ''
    if aStr[0] == "'":
        value = aStr.replace("'", '"')
    else:
        value =  ''.join(['"', aStr, '"'])

    return value

def strToIntDef(aStr : str, defValue : int = 0)->int:
    """strToIntDef convert str value to integer with default value if str is not an integer

    Parameters
    ----------
    aStr : str
        A number in string
    defValue : int
        The default value if convert failed

    Returns
    -------
    int
        The number
    """
    value = 0
    try:
        value = int(aStr)
    except:
        value = defValue
    finally:
        return value