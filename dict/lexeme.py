import pymorphy2

from pymorphy2 import tokenizers

morph = pymorphy2.MorphAnalyzer()


text = " this-is a test ! "

print(tokenizers.simple_word_tokenize(text))
