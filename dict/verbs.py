from .magic import Word

class Verbs_imperfect(Word):

    """class for verbs"""
    # TODO: write this class...
    def __init__(self, input_word):
        Word.__init__(input_word)
        self._past = {}
        self._present = {}
        self._command = {}

    def classify(self,tag, tense, word):
        if '1per' in str(tag):
            if str(tag.number) == 'sing':
                self._present['i'] = word
            else:
                self._present['we'] = word
        elif '2per' in str(tag):
            if str(tag.number) == 'sing':
                self._present['you1'] = word
            else:
                self._present['you2'] = word
        elif '3per' in str(tag):
            if str(tag.number) == 'sing':
                self._present['hesheit'] = word
            else:
                self._present['they'] = word



