import regex

def pattern_has_uppercase_char(pattern: str):
    cleaned_pattern = regex.sub(r'\\.', '', pattern)

    return bool(regex.search('[[:upper:]]', cleaned_pattern))


def pattern_matches_strings_with_leading_dot(pattern: str):
    return pattern.startswith(r'^\.')
