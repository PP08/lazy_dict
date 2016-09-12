import pymorphy2

inflect_word = "час"

morph = pymorphy2.MorphAnalyzer()
info = morph.parse(inflect_word)[0]
j = 0
for i in info.lexeme:
    print(i, j)
    j += 1
    # print(str(i.tag))


# print(morph.parse('пойти')[0].inflect({'sing', 'impf'}).word)

