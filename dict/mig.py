import codecs
import pymorphy2

class MyMethod():
    def convert(s):
        base64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        decValue = 0
        slen = len(s)
        for i in range(slen):
            pos = base64.find(s[i])
            decValue += pow(64, slen - i - 1) * pos
        return decValue

class IndexFileReader(MyMethod):

    def __init__(self,filename):
        with codecs.open(filename,'r+b',encoding='utf-8',errors='ignore') as idx_file:
            self._content = idx_file.read()
            self._result = []
            self._tmp = []
            # print(self._content)
    def get_index_by_word(self,word_str):
        index = self._content.find(word_str) + 1
        start = index + len(word_str)
        step = True
        i = 0
        while(step):
            if(self._content[start + i] != '\n'):
                i = i + 1
            else:
                step = False
        line = self._content[index:start+i]
        self._tmp = str.split(line,'\t')
        self._result = [MyMethod.convert(self._tmp[1]),MyMethod.convert(self._tmp[2])]


class DictFileReader(IndexFileReader):
    def __init__(self, filename):
        self._file = open(filename,'rb')
        self._meaning = ""
    def get_meaning_by_index(self,offset,size):
        self._file.seek(offset)
        data = self._file.read(size)
        self._meaning = data.decode('utf-8')


class Normalize():
    def __init__(self,inflectWord):
        self._inflect_word = inflectWord
        self._normal_word = ""
    def normalize(self):
        morph = pymorphy2.MorphAnalyzer()
        info = morph.parse(self._inflect_word)
        self._normal_word = info[0][2]
        print(self._normal_word)


idx_file = "ngaviet.index"
dict_file = "ngaviet.dict"
idx_reader = IndexFileReader(idx_file)
dict_reader = DictFileReader(dict_file)


dictionaries = {}

def parse_word_from_idex_file():
    file = open(idx_file,'r')
    content = file.readlines()
    for line in content:
        space = line.find('\t')
        word = line[0:space]
        tmp = '\n' + line[0:space] + '\t'
        idx_reader.get_index_by_word(tmp)
        dict_reader.get_meaning_by_index(idx_reader._result[0],idx_reader._result[1])
        dictionaries[word] = dict_reader._meaning
    #print (dictionaries)
    #meaning.insert(INSERT, dict_reader._meaning)

parse_word_from_idex_file()

for k,v in dictionaries.items():
    q = Dictionary(word=k,definition=v)
    q.save()
