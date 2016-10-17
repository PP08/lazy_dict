import re
import json
import os
from pymorphy2 import tokenizers

from django.http import HttpResponse
from django.shortcuts import render

from .import_dict import DictFileReader
from .magic import Word, Noun, NounType2, Adjective_type1, Number, Adjective_type2
from .verbs import Verbs_imperfect, Verb_perfect

path1 = os.path.abspath('data/tonghop.dict')
path2 = os.path.abspath('data/tonghop.txt')

dict_reader = DictFileReader(path1)
file = open(path2, 'r')
content = file.read()

def index(request):
    return render(request, 'dict/base.html')

def search(request):
    if request.POST.get('query'):
        response_data = {}

        q = request.POST.get('query')

        temp = tokenizers.simple_word_tokenize(q)

        query = ''

        for i in range(len(temp) - 1):
            if temp[i + 1] not in ['!','.']:
                query += temp[i] + ' '
            else:
                query += temp[i]
        query += temp[-1]

        word = Word(query)

        word.normalize()

        print(word._normal_word)

        if 'ё' in word._normal_word:
            word._normal_word = word._normal_word.replace("ё", "е")

        pattern1 = '\s+\d+\s+\d+\s+' + query + '\s'

        prog1 = re.compile(pattern1)

        pattern2 = '\s+\d+\s+\d+\s+' + word._normal_word + '\s'
        prog2 = re.compile(pattern2)

        contain = False

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
        response_data['search_query'] = query

        if contain:
            response_data['classifier'] = classifier
            response_data['wdefinition'] = dict_reader._meaning

        else:
            response_data['not_found'] = "<h5>Not found...</h5>"

        if classifier is not None:
            if classifier in ['NOUN', 'NPRO']:

                noun = Noun(query)
                noun.lookup_words()
                context = noun._context

                noun_type2 = NounType2(query)
                noun_type2.lookup_words()

                response_data['context'] = context
                response_data['context2'] = noun_type2._context

            elif classifier in 'ADJF':
                if not ('Qual' in word.tag):
                    type = 0
                    adj = Adjective_type1(query)
                    adj.lookup_words()
                    context = adj._context
                    response_data['context'] = context
                    response_data['type'] = type

                elif 'Qual' in word.tag:
                    type = 2
                    adj = Adjective_type2(query)
                    adj.lookup_words()
                    adj.lookup_words_type2()
                    adj.lookup_comparison()
                    adj.lookup_shorten()

                    response_data['context'] = adj._context
                    response_data['context_comp'] = adj._context_for_comparison
                    response_data['context_shorten'] = adj._context_for_shorten_adj
                    response_data['type'] = type

            elif classifier in 'NUMR':
                num = Number(query)
                num.lookup_words_num_type2()
                num.lookup_words()
                context = num._context
                context_n = num._context_n
                response_data['context'] = context
                response_data['context_n'] = context_n


            elif classifier in ['INFN', 'VERB']:


                if 'impf' in word.tag:

                    verb = Verbs_imperfect(query)
                    verb.look_up()

                    response_data['context'] = verb._present
                    response_data['context_for_past'] = verb._past
                    response_data['context_for_command_type1'] = verb._command_type1
                    response_data['context_for_command_type2'] = verb._command_type2
                elif 'perf' in word.tag:

                    verb = Verb_perfect(query)
                    verb.look_up()
                    response_data['context'] = verb._future
                    response_data['context_for_past'] = verb._past
                    response_data['context_for_command_type1'] = verb._command_type1
                    response_data['context_for_command_type2'] = verb._command_type2

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        response_data = {}
        response_data['error'] = "blah blah blah"
        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )