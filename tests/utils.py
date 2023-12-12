import textwrap

def dedent(text: str) -> str:
    """Dedent an indented string by the miniumum indentation level.

    Args:
        text: String to dedent 

    Returns:
        dedented string
        
    """
    return textwrap.dedent(text).strip("\n")


def dedent_and_replace(
    to_dedent: str, to_replace: str, new: str, dedent_new: bool = True
) -> str:
    """Dedent and replace a string.

    Args:
        to_dedent: String to dedent 
        to_replace: String to replace
        new: String to replace with
        dedent_new: Bool that is true if `new` should also be dedented.

    Returns:
        
    """
    if dedent_new:
        new = dedent(new)
    return dedent(to_dedent).replace(to_replace, new)
