__version__ = "0.1.2"

def version()->str:
    """Return the version of the lib

    Parameters
    ----------
    
    Returns
    -------
    str
        The string with version
    """
    return __version__

# str functions
from .str import quotedStr, dblQuotedStr, strToIntDef

__all__ = [version, quotedStr, dblQuotedStr, strToIntDef]