text = input()
symbols = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
letters = collections.Counter(text.upper())
length = len(text)
print('Length of message: {} characters'.format(length))
for letter, times in sorted(letters.items()):
    if letter not in symbols:
        continue
    percent = str(int((times / length) * 100)) + '%'
    print(('{:<5}'*3).format(letter, times, percent))
