import pymorphy2


inflect_word = "стратифицированный"
# перестановочный
# алоэ
# вычислительных
# Дешифрирование
# стратифицированный
morph = pymorphy2.MorphAnalyzer()
info = morph.parse(inflect_word)[0]
j = 0
file = open('output1.txt', 'w')

for i in info.lexeme:
    print(i, j)
    j += 1
    file.write(str(i) + '\n')

file.close()


    # print(str(i.tag))


# print(morph.parse('пойти')[0].inflect({'sing', 'impf'}).word)

