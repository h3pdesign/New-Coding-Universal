def left_pad(s, l):
    return ' ' * (l - len(s)) + s

if _name_ == "_main_":
    print left_pad('a', 2)
