## strip version updater (3 digit only with default pattern)

import re

def update_version_string(string, version, version_pattern=None):
    """Update string with passed version on all occurence

    Args:
        string (str): the string to update
        version (str|int): version to apply (will get same padding as replaced string)
        version_pattern (str, optional): regex pattern for version
    """

    ## version match: lowercase 'v' followed by 3 digit.
    ## Anchors: 
    ##   - before: only if there is a separator before "-_/\" OR string start (can happen in output nodes).
    ##   - after : only with no subsequent digits (ex: v29400)
    default_pattern = r'(?:(?<=[-_./\\ ])|^)v(\d{3})(?![0-9])'

    ## Simpler anchoring (preventing only match with subsequent digit, don't care about previous)
    # default_pattern = r'v(\d{3})(?![0-9])'

    version_pattern = version_pattern or default_pattern
    re_version = re.compile(version_pattern)
    version = int(version)

    def replace(match):
        new = str(version).zfill(len(match.group(1)))
        offset = match.start()
        start, end = match.span(1)
        whole = match.group(0)
        return whole[:start - offset] + new + whole[end - offset:]

    return re_version.sub(replace, string)

print(update_version_string('v005/test-v255. also update v008 (but not this one maxv200, nor this one v20000)', 1))
# result:                >>> v001/test-v001. also update v001 (but not this one maxv200, nor this one v20000)
