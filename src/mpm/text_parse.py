def is_ascii(s: str) -> bool:
    if s == "":
        return False
    return all(ord(c) < 128 for c in s)


def is_first_alpha(s: str) -> bool:
    if s == "":
        return False
    return s[0].isalpha()
 
def is_first_ascii_alpha(s: str) -> bool:
    if s == "":
        return False
    return ord(s[0]) < 128 and s[0].isalpha()
