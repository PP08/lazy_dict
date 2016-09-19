import pymorphy2


inflect_word = "делан"
morph = pymorphy2.MorphAnalyzer()
info = morph.parse(inflect_word)[0]
j = 0
file = open('output1.txt', 'w')

for i in info.lexeme:
    print(i.tag.POS)
    j += 1
    file.write(str(i) + str(j) + '\n')

file.close()

inflect_word2 = "делан"
morph2 = pymorphy2.MorphAnalyzer()
info2 = morph2.parse(inflect_word2)[0]
j = 0
file2 = open('output2.txt', 'w')

for i in info2.lexeme:
    # print(i, j)
    j += 1
    file2.write(str(i) + str(j) +'\n')

file2.close()



    # print(str(i.tag))


# print(morph.parse('пойти')[0].inflect({'sing', 'impf'}).word)

