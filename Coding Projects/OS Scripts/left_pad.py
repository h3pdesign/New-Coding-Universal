def left_pad(s, l):
    return ' ' * (l - len(s)) + s

if __name__ == "__main__":
    print(left_pad('a', 2))
