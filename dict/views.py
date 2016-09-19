import re

from django.http import HttpResponse
from django.shortcuts import render

from .import_dict import DictFileReader
from .magic import Word, Noun, NounType2, Adjective_type1, Number, Adjective_type2
from .models import KeyWord


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
        if 'ё' in word._normal_word:
            word._normal_word = word._normal_word.replace("ё", "е")

        dict_reader = DictFileReader('tonghop.dict')
        contain = False

        pattern1 = '\s+\d+\s+\d+\s+' + search_query.group() + '\s'
        prog1 = re.compile(pattern1)

        pattern2 = '\s+\d+\s+\d+\s+' + word._normal_word + '\s'
        prog2 = re.compile(pattern2)
        # TODO rewrite new method for this searching...
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

        similar_words = {}
        if (not contain):
            similar_words = KeyWord.objects.filter(keyWord__icontains=search_query.group())
            print(similar_words)

        if classifier != None:
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

                if not ('Qual' in word.tag):
                    type = 1
                    adj = Adjective_type1(search_query.group())
                    adj.lookup_words()
                    context = adj._context
                    return render(request, 'dict/search_results.html',
                                  {'definition': dict_reader._meaning, 'query': q, 'similar_words': similar_words,
                                   'context': context, 'classifier': classifier, 'type': type, })
                elif 'Qual' in word.tag:
                    type = 2
                    adj = Adjective_type2(search_query.group())
                    adj.lookup_words()
                    adj.lookup_words_type2()
                    adj.lookup_comparison()
                    adj.lookup_shorten()
                    return render(request, 'dict/search_results.html',
                                  {'definition': dict_reader._meaning, 'query': q, 'similar_words': similar_words,
                                   'context': adj._context, 'context_comp': adj._context_for_comparison,
                                   'context_type2': adj._context_for_type2,
                                   'context_shorten': adj._context_for_shorten_adj, 'classifier': classifier,
                                   'type': type, })


            elif classifier in 'NUMR':
                num = Number(search_query.group())
                if len(num.info) > 40:
                    type = 1
                    num.lookup_words_num_type1()
                    num.lookup_words_a()
                    context = num._context
                    context_n = num._context_n
                    return render(request, 'dict/search_results.html',
                                  {'definition': dict_reader._meaning, 'query': q, 'similar_words': similar_words,
                                   'context': context, 'classifier': classifier, 'context_n': context_n, 'type': type, })
                else:
                    type = 2
                    num.lookup_words_num_type2()
                    num.lookup_words()
                    context = num._context
                    context_n = num._context_n
                    return render(request, 'dict/search_results.html',
                                  {'definition': dict_reader._meaning, 'query': q, 'similar_words': similar_words,
                                   'context': context, 'classifier': classifier, 'context_n': context_n, 'type': type})
        elif classifier == None:
            return render(request, 'dict/search_results.html',
                      {'definition': dict_reader._meaning, 'similar_words': similar_words})
    return render(request, 'dict/search_form.html', {'error_message': "Please submit the search form!", })


def import_dict(request):
    return render(request, 'dict/import_dict.html')


def report(request):
    """method for importing the database of the dictionary"""
    key_words = []
    file = open('tonghop.txt', 'r')
    # file.readline()
    content = file.readlines()
    context = "successful"
    error = "failure"
    for line in content:
        array = line.split()
        word = ''
        if (len(array) > 3):
            for i in range(2, len(array) - 1):
                word += word + array[i] + ' '
            word += array[-1]
        else:
            word = array[2]

        key_words.append(word)
    for word in key_words:
        q = KeyWord(keyWord=word)
        q.save()
    return render(request, 'dict/report.html', {'context': context, 'failure': error})
