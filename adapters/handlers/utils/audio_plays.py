from typing import Sequence

from adapters.handlers.utils.markdown import italic, link
from api.model.audio_play import CastMember
from api.model.person import Person


def make_written_by(writers: Sequence[Person]) -> str | None:
    """
    Makes "Written by ..." line based on given writers.
    :param writers: writers of an audio play.
    :return: line or None if no writers are found.
    """
    if not writers:
        return None
    names = [w.name for w in writers]
    first_part = ", ".join(names[:-1])
    return "Written by " + " & ".join(
        italic(x) for x in (first_part, names[-1]) if x
    )


def make_starring(cast: Sequence[CastMember]) -> str | None:
    """
    Makes "Starring ..." line based on main cast.
    :param cast: cast of an audio play.
    :return: line or None if no member of main cast is found.
    """
    mains = [c for c in cast if c.main]
    if not mains:
        return None
    names = [c.actor.name for c in mains]
    first_part = ", ".join(names[:-1])
    return "Starring " + " & ".join(
        italic(x) for x in (first_part, names[-1]) if x
    )
