import textwrap


def dedent(text: str) -> str:
    return textwrap.dedent(text).strip("\n")


def dedent_and_replace(
    to_dedent: str, to_replace: str, new: str, dedent_new: bool = True
) -> str:
    if dedent_new:
        new = dedent(new)
    return dedent(to_dedent).replace(to_replace, new)
