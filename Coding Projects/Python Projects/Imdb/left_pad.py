def left_pad(s, l):
    return ' ' * (l - len(s)) + s

if __name__ == "__main__":
    print(left_pad('a', 2))

# Note: If pipreqs fails with SyntaxWarning for invalid escape sequences (e.g., \d),
# check for regex patterns in this file that might not use raw strings (r'\d').
# Full file content or specific lines (e.g., 545, 547, 549, 552) are needed for further fixes.
