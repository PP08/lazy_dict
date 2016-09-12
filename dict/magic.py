import pymorphy2


class Word:
    def __init__(self, inputWord):
        self._input_word = inputWord
        self._normal_word = ""
        self._morph = pymorphy2.MorphAnalyzer()
        self.info = self._morph.parse(inputWord)[0].lexeme
        self._pos = self._morph.parse(inputWord)[0].tag.POS
        self._case1 = {}
        self._case2 = {}
        self._case3 = {}
        self._case4 = {}
        self._case5 = {}
        self._case6 = {}

        self._context = []

    def normalize(self):
        info = self._morph.parse(self._input_word)
        self._normal_word = info[0][2]
        # print(self._normal_word)


class Noun(Word):
    def __init__(self, inputWord):
        Word.__init__(self, inputWord)
        # self._case1 = {}
        self._case1['explaination'] = 'Кто? Что?'
        self._case1['example'] = 'хомяк ест'
        # self._case2 = {}
        self._case2['explaination'] = 'Кого? Чего?'
        self._case2['example'] = 'у нас нет хомяка'
        # self._case3 = {}
        self._case3['explaination'] = 'Кому? Чему?'
        self._case3['example'] = 'сказать хомяку спасибо'
        # self._case4 = {}
        self._case4['explaination'] = 'Кого? Что?'
        self._case4['example'] = 'хомяк читает книгу'
        # self._case5 = {}
        self._case5['explaination'] = 'Кем? Чем?'
        self._case5['example'] = 'зерно съедено хомяком'
        # self._case6 = {}
        self._case6['explaination'] = 'О ком? О чём? '
        self._case6['example'] = 'хомяка несут в корзинке'
        # self._inflected_words = []

    def classify(self, tag, case, word):
        """method for words classifier"""
        if ('sing' in str(tag.number)) and (not('Patr' in str(tag))) and (not('Fixd' in str(tag))):
            case['sing'] = word
        elif ('plur' in str(tag.number)) and (not('Patr' in str(tag))) and (not('Fixd' in str(tag))):
            case['plur'] = word

    def lookup_words(self):
        # TODO check the case when input word is 'hour'
        for i in self.info:
            if (str(i.tag.case) == 'nomn'):
                self.classify(i.tag, self._case1, i.word)

            elif (str(i.tag.case) == 'gent'):
                self.classify(i.tag, self._case2, i.word)

            elif (str(i.tag.case) == 'datv'):
                self.classify(i.tag, self._case3, i.word)

            elif (str(i.tag.case) == 'accs'):
                self.classify(i.tag, self._case4, i.word)

            elif (str(i.tag.case) == 'ablt' and not ('V-oy' in i.tag)):
                self.classify(i.tag, self._case5, i.word)

            elif (str(i.tag.case) == 'loct'):
                self.classify(i.tag, self._case6, i.word)

        for i in (self._case1, self._case2, self._case3, self._case4, self._case5, self._case6):
            self._context.append(i)


class NounType2(Noun):
    """class for parsing type 2 of nouns"""

    def classify(self, tag, case, word):
        if ('Patr sing' in str(tag)) and (str(tag.gender) == 'femn'):
            case['sing'] = word
        if ('Patr plur' in str(tag)) and (str(tag.gender) == 'femn'):
            case['plur'] = word


class Adjective_type1(Word):
    """class for parsing adjective"""

    def classify(self, tag, word, case):
        if 'sing' in str(tag.number) and not ('Supr' in str(tag)):
            # if 'ADJF macs' in str(tag) or 'masc' in str(tag) or 'Qual masc' in str(tag):
            if str(tag.gender) == 'masc':
                case['male'] = word
            if str(tag.gender) == 'femn':
                case['female'] = word
            if str(tag.gender) == 'neut':
                case['neuter'] = word
        if 'plur' in str(tag.number) and not ('Supr' in str(tag)):
            case['plur'] = word

    def lookup_words(self):
        for i in self.info:
            if str(i.tag.case) == 'nomn':
                self.classify(i.tag, i.word, self._case1)

            if str(i.tag.case) == 'gent':
                self.classify(i.tag, i.word, self._case2)

            if (str(i.tag.case) == 'datv'):
                self.classify(i.tag, i.word, self._case3)

            if (str(i.tag.case) == 'nomn'):
                self.classify(i.tag, i.word, self._case4)

            if (str(i.tag.case) == 'accs'):
                self.classify(i.tag, i.word, self._case5)

            if (str(i.tag.case) == 'loct'):
                self.classify(i.tag, i.word, self._case6)

        for i in (self._case1, self._case2, self._case3, self._case4, self._case5, self._case6):
            self._context.append(i)


class Adjective_type2(Adjective_type1):
    """class for type 2 of adjectives"""


adj = Adjective_type1('классический')

adj.lookup_words()

for i in adj._context:
    print(i)

# print(noun.info)


# print (noun._table_inflection)
