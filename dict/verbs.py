from .magic import Word


class Verbs_imperfect(Word):
    """class for verbs"""

    def __init__(self, input_word):
        Word.__init__(self, input_word)
        self._past = {}
        self._present = {}
        self._command_type1 = {}
        self._command_type2 = {}

    def classify_present(self, tag, tense, word):
        if '1per' in str(tag):
            if str(tag.number) == 'sing':
                tense['i'] = word
            else:
                tense['we'] = word
        elif '2per' in str(tag):
            if str(tag.number) == 'sing':
                tense['you1'] = word
            else:
                tense['you2'] = word
        elif '3per' in str(tag):
            if str(tag.number) == 'sing':
                tense['hesheit'] = word
            else:
                tense['they'] = word

    def classify_past(self, tag, tense, word):
        if str(tag.gender) == 'masc':
            tense['ihe'] = word
        elif str(tag.gender) == 'femn':
            tense['she'] = word
        elif str(tag.gender) == 'neut':
            tense['it'] = word
        elif str(tag.number) == 'plur':
            tense['they'] = word

    def classify_command(self, tag, tense, word):
        if str(tag.number) == 'sing':
            tense['sing'] = word
        if str(tag.number) == 'plur':
            tense['plur'] = word

    def look_up(self):
        for i in self.info:
            if 'indc' in str(i.tag):
                if not ('past' in str(i.tag)):
                    self.classify_present(i.tag, self._present, i.word)
                else:
                    self.classify_past(i.tag, self._past, i.word)
            elif 'excl' in str(i.tag):
                self.classify_command(i.tag, self._command_type1, i.word)
            elif 'incl' in str(i.tag):
                self.classify_command(i.tag, self._command_type2, i.word)


class Verb_perfect(Verbs_imperfect):
    """class for perfect verbs"""

    # TODO: write this class
    def __init__(self, input_word):
        Verbs_imperfect.__init__(self, input_word)
        self._future = {}

    def classify_future(self, tag, tense, word):
        if '1per' in str(tag):
            if str(tag.number) == 'sing':
                tense['i'] = word
            else:
                tense['we'] = word
        elif '2per' in str(tag):
            if str(tag.number) == 'sing':
                tense['you1'] = word
            else:
                tense['you2'] = word
        elif '3per' in str(tag):
            if str(tag.number) == 'sing':
                tense['hesheit'] = word
            else:
                tense['they'] = word

    def look_up(self):
        for i in self.info:
            if 'indc' in str(i.tag):
                if not ('past' in str(i.tag)):
                    self.classify_future(i.tag, self._future, i.word)
                else:
                    self.classify_past(i.tag, self._past, i.word)
            elif 'excl' in str(i.tag):
                self.classify_command(i.tag, self._command_type1, i.word)
            elif 'incl' in str(i.tag):
                self.classify_command(i.tag, self._command_type2, i.word)
