## fuzzy match two strings similatiry using a matching ratio

def fuzzy_match(s1, s2, tol=0.8, case_sensitive=False):
    '''Tell if two strings are similar using a similarity ratio (0 to 1) value passed as third arg'''
    from difflib import SequenceMatcher
    # can also use difflib.get_close_matches(word, possibilities, n=3, cutoff=0.6)
    if case_sensitive:
        similarity = SequenceMatcher(None, s1, s2)
    else:
        similarity = SequenceMatcher(None, s1.lower(), s2.lower())
    return similarity.ratio() > tol

def fuzzy_match_ratio(s1, s2, case_sensitive=False):
    '''Tell how much two passed strings are similar 1.0 being exactly similar'''
    from difflib import SequenceMatcher
    if case_sensitive:
        similarity = SequenceMatcher(None, s1, s2)
    else:
        similarity = SequenceMatcher(None, s1.lower(), s2.lower())
    return similarity.ratio()
