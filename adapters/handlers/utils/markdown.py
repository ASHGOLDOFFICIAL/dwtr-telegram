def bold(s: str) -> str:
    """
    Makes text bold.
    :param s: string to make bold.
    :rtype: str bold string.
    """
    return "**" + s + "**"


def italic(s: str) -> str:
    """
    Makes string italic.
    :param s: string to make italic.
    :return: italic string.
    """
    return "*" + s + "*"


def link(text: str, link_: str) -> str:
    """
    Makes link.
    :param text: link label.
    :param link_: link itself.
    :return: link element.
    """
    return f"[{text}]({link_})"


def h1(s: str) -> str:
    """
    Makes level 1 heading
    :param s: string to make heading from.
    :return: heading.
    """
    return "# " + s

def h2(s: str) -> str:
    """
    Makes level 2 heading
    :param s: string to make heading from.
    :return: heading.
    """
    return "## " + s

HORIZONTAL_RULE: str = "\n***\n"