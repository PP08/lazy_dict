from django.http import HttpResponse
from django.shortcuts import render
from .models import Dictionary, KeyWord
from .magic import Word, Noun, NounType2, Adjective_type1
from .import_dict import DictFileReader
import re

def index(request):
    return HttpResponse("Hello, world.")


def search_form(request):
    return render(request, 'dict/search_form.html')


def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        pattern_input = "\w+-?\s?\w+"
        prog_input = re.compile(pattern_input)
        search_query = prog_input.search(q)
        word = Word(search_query.group())
        word.normalize()
        if('ё' in word._normal_word):
            word._normal_word = word._normal_word.replace("ё", "е")

        dict_reader = DictFileReader('tonghop.dict')
        # word._normal_word = ' ' + word._normal_word + '\n'
        line_contains_keyword = ''
        contain = False
        pattern = '\s+\d+\s+\d+\s+' + word._normal_word + '\s'
        prog = re.compile(pattern)
        # TODO rewrite new method for this searching...
        with open('tonghop.txt') as file:
            content = file.read()
            line = prog.search(content)
            if(line):
                array = line.group().split()
                contain = True
                offset = int(array[0])
                size = int(array[1])
                dict_reader.get_meaning_by_index(offset,size)

        classifier = word._pos

        similar_words = {}
        if (not contain):
            similar_words = KeyWord.objects.filter(keyWord__istartswith=q)

        if (classifier in ['NOUN', 'NPRO']):
            noun = Noun(search_query.group())
            noun.lookup_words()
            context = noun._context

            noun_type2 = NounType2(search_query.group())
            noun_type2.lookup_words()

            return render(request, 'dict/search_results.html',
                          {'definition': dict_reader._meaning, 'query': q, 'similar_words': similar_words,
                           'context': context, 'classifier': classifier, 'context2': noun_type2._context})
        elif classifier in 'ADJF':
            adj = Adjective_type1(q)
            adj.lookup_words()
            context = adj._context
            return render(request, 'dict/search_results.html',
                          {'definition': dict_reader._meaning, 'query': q, 'similar_words': similar_words,
                           'context': context, 'classifier': classifier,})

    return render(request, 'dict/search_form.html', {'error_message': "Please submit the search form!"})

def import_dict(request):
    return render(request, 'dict/import_dict.html')

def report(request):
    """method for importing the database of the dictionary"""
    key_words = []
    file = open('tonghop.txt','r')
    file.readline()
    content = file.readlines()
    context = "successful"
    error = "failure"
    for line in content:
        array = line.split()
        word = ''
        if(len(array) > 3):
            for i in range(2,len(array) - 1):
                word += word + array[i] + ' '
            word += array[-1]
        else:
            word = array[2]

        key_words.append(word)
    for word in key_words:
        q = KeyWord(keyWord=word)
        q.save()
    return render(request, 'dict/report.html', {'context': context, 'failure': error})


