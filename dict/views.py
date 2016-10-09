import re
import json

from django.http import HttpResponse
from django.shortcuts import render

from .import_dict import DictFileReader
from .magic import Word, Noun, NounType2, Adjective_type1, Number, Adjective_type2
from .models import KeyWord
from .verbs import Verbs_imperfect

def index(request):
    return render(request, 'dict/base.html')

def search(request):
    if request.POST.get('query'):
        response_data = {}

        q = request.POST.get('query')
        pattern_input = "\w+-?\s?\w+"
        prog_input = re.compile(pattern_input)
        search_query = prog_input.search(q)
        word = Word(search_query.group())
        word.normalize()

        if 'ё' in word._normal_word:
            word._normal_word = word._normal_word.replace("ё", "е")

        dict_reader = DictFileReader('tonghop.dict')


        pattern1 = '\s+\d+\s+\d+\s+' + search_query.group() + '\s'
        prog1 = re.compile(pattern1)

        pattern2 = '\s+\d+\s+\d+\s+' + word._normal_word + '\s'
        prog2 = re.compile(pattern2)

        contain = False
        with open('tonghop.txt') as file:
            content = file.read()
            line1 = prog1.search(content)
            if (line1):
                array = line1.group().split()
                contain = True
                offset = int(array[0])
                size = int(array[1])
                dict_reader.get_meaning_by_index(offset, size)
            else:
                line2 = prog2.search(content)
                if (line2):
                    array = line2.group().split()
                    contain = True
                    offset = int(array[0])
                    size = int(array[1])
                    dict_reader.get_meaning_by_index(offset, size)

        classifier = word._pos

        response_data['classifier'] = classifier


        similar_words = {}

        if (not contain):
            similar_words = KeyWord.objects.filter(keyWord__icontains=search_query.group())
            # print(similar_words)

        response_data['similar'] = similar_words

        if classifier != None:
            if classifier in ['NOUN', 'NPRO']:
                noun = Noun(search_query.group())
                noun.lookup_words()
                context = noun._context

                noun_type2 = NounType2(search_query.group())
                noun_type2.lookup_words()

                response_data['context'] = context
                response_data['query'] = q
                response_data['context2'] = noun_type2._context

                return HttpResponse(
                    json.dumps(response_data),
                    content_type="application/json"
                )




        response_data['test'] = "successful"
        response_data['input'] = request.POST.get('query')

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
