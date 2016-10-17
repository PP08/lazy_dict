class DictFileReader():
    def __init__(self, filename):
        self._file = open(filename,'rb')
        self._meaning = ""
    def get_meaning_by_index(self,offset,size):
        self._file.seek(offset)
        data = self._file.read(size)
        self._meaning = data.decode('utf-8')

