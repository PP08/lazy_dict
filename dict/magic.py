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
        if ('sing' in str(tag.number)) and (not('Patr' in str(tag))) and (not('Fixd' in str(tag))) and (not('V-be') in str(tag)):
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

    def classify(self, tag, case, word):
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
                self.classify(i.tag, self._case1, i.word)

            if str(i.tag.case) == 'gent':
                self.classify(i.tag, self._case2, i.word)

            if (str(i.tag.case) == 'datv'):
                self.classify(i.tag, self._case3, i.word)

            if (str(i.tag.case) == 'nomn'):
                self.classify(i.tag, self._case4, i.word)

            if (str(i.tag.case) == 'accs'):
                self.classify(i.tag, self._case5, i.word)

            if (str(i.tag.case) == 'loct'):
                self.classify(i.tag, self._case6, i.word)

        for i in (self._case1, self._case2, self._case3, self._case4, self._case5, self._case6):
            self._context.append(i)


class Adjective_type2(Adjective_type1):
    """class for type 2 of adjectives"""
    # TODO: write this class,




class Number(Adjective_type1):
    """class for number"""
    def __init__(self, input_word):
        Adjective_type1.__init__(self, input_word)
        self._case1_n = {}
        self._case1_n['name'] = 'именительный'
        self._case2_n = {}
        self._case2_n['name'] = 'родительный'
        self._case3_n = {}
        self._case3_n['name'] = 'дательный'
        self._case4_n = {}
        self._case4_n['name'] = 'винительный (неодушевленное)'
        self._case4_n_s = {}
        self._case4_n['name'] = 'винительный'
        self._case5_n = {}
        self._case5_n['name'] = 'творительный'
        self._case6_n = {}
        self._case6_n['name'] = 'предложный'
        self._case4_n_2 = {}
        self._case4_n_2['name'] = 'винительный (одушевлённое)'
        self._context_n = []


    def classify_num(self, tag, case, word):
        if 'NUMR masc' in str(tag.POS) or 'masc' in str(tag.gender):
            case['male'] = word
        elif 'NUMR femn' in str(tag.POS) or 'femn' in str(tag.gender):
            case['female'] = word
        elif 'NUMR neut' in str(tag.POS) or 'neut' in str(tag.gender):
            case['neuter'] = word

    def lookup_words_num_type1(self):
        for i in self.info:
            if (str(i.tag.case) == 'nomn'):
                self.classify_num(i.tag, self._case1_n, i.word)

            elif (str(i.tag.case) == 'gent'):
                self.classify_num(i.tag, self._case2_n, i.word)

            elif (str(i.tag.case) == 'datv'):
                self.classify_num(i.tag, self._case3_n, i.word)

            elif (str(i.tag.case) == 'accs') and ('NUMR inan' in str(i.tag)):
                self.classify_num(i.tag, self._case4_n, i.word)

            elif(str(i.tag.case) == 'accs') and ('NUMR anim' in str(i.tag)):
                self.classify_num(i.tag, self._case4_n_2, i.word)

            elif (str(i.tag.case) == 'ablt'):
                self.classify(i.tag, self._case5_n, i.word)

            elif (str(i.tag.case) == 'loct'):
                self.classify(i.tag, self._case6_n, i.word)

        for i in (self._case1_n, self._case2_n, self._case3_n, self._case4_n, self._case4_n_2, self._case5_n, self._case6_n):
            self._context_n.append(i)

    def lookup_words_num_type2(self):
        for i in self.info:
            if 'NUMR nomn' in str(i.tag):
                self._case1_n['inflection'] = i.word

            if 'NUMR gent' in str(i.tag):
                self._case2_n['inflection'] = i.word

            if 'NUMR datv' in str(i.tag):
                self._case3_n['inflection'] = i.word

            if ('accs' in str(i.tag.case) or 'NUMR accs' in str(i.tag)) and str(i.tag.POS) == 'NUMR':
                if 'NUMR inan' in str(i.tag):
                    self._case4_n['inflection'] = i.word
                elif 'NUMR anim' in str(i.tag):
                    self._case4_n_2['inflection'] = i.word
                else:
                    self._case4_n_s['inflection'] = i.word

            if 'NUMR ablt' in str(i.tag):
                self._case5_n['inflection'] = i.word

            if 'NUMR loct' in str(i.tag):
                self._case6_n['inflection'] = i.word

        for i in (self._case1_n, self._case2_n, self._case3_n, self._case4_n, self._case4_n_2, self._case4_n_s, self._case5_n, self._case6_n):
            if len(i.values()) == 2:
                self._context_n.append(i)


    def lookup_words_a(self):
        for i in self.info:
            if str(i.tag.case) == 'nomn' and (str(i.tag.POS) == 'ADJF'):
                self.classify(i.tag, self._case1, i.word)

            if str(i.tag.case) == 'gent' and (str(i.tag.POS) == 'ADJF'):
                self.classify(i.tag, self._case2, i.word)

            if (str(i.tag.case) == 'datv') and (str(i.tag.POS) == 'ADJF'):
                self.classify(i.tag, self._case3, i.word)

            if (str(i.tag.case) == 'nomn') and (str(i.tag.POS) == 'ADJF'):
                self.classify(i.tag, self._case4, i.word)

            if (str(i.tag.case) == 'ablt') and (str(i.tag.POS) == 'ADJF') and not('V-ey' in str(i.tag)):
                self.classify(i.tag, self._case5, i.word)

            if (str(i.tag.case) == 'loct') and (str(i.tag.POS) == 'ADJF'):
                self.classify(i.tag, self._case6, i.word)

        for i in (self._case1, self._case2, self._case3, self._case4, self._case5, self._case6):
            self._context.append(i)


# print(noun.info)


# print (noun._table_inflection)
