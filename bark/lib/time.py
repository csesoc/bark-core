__all__ = ['parse_time']

from datetime import datetime
import iso8601

def parse_time(raw):
    """
    Parses given string using one of many possibilities defined by ISO8601.
    """

    parsed = None

    try:
        parsed = iso8601.parse_date(raw)
    except (ValueError, TypeError), e:
        # iso8601 raises TypeError if something does not conform to its regex.
        raise ValueError('Date %r does not parse: %s'
            % (raw, e.args[0] if e.args else 'wtf'))

    return parsed
