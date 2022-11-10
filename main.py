import re
import string
import os
import traceback
import time
import random
import bltk
import helper
from bltk.langtools import Tokenizer
from bltk.langtools.banglachars import operators,punctuations, digits

DATASET_PATH = 'dataset'

POET_STAT_CSV_PATH = 'poet_stat.csv'
GLOBAL_STAT_CSV_PATH = 'global_stat.csv'

DATA_LIST = []
CONTENT_LIST = []
POET_STAT_LIST = []
GLOBAL_STAT_LIST = []


def import_dataset_from_raw_dataset():
    POEM_POET_SET = []
    poets_list = os.listdir(DATASET_PATH)

    poets_list.sort()

    for poet in poets_list:

        poems_list = os.listdir(DATASET_PATH + "/" + poet)
        poems_list.sort()

        for poem in poems_list:
            try:
                ### source
                source_meta = helper.getStringFromFile(DATASET_PATH + "/" + poet + "/" + poem + "/SOURCE.txt")
                source_url = source_meta.split('\n')[0]
                source_timestamp = source_meta.split('\n')[1]

                ### content
                poem_content = helper.getStringFromFile(DATASET_PATH + "/" + poet + "/" + poem + "/" + poem + ".txt")
                poem_word_count = helper.countWords(poem_content)
                poem_sentence_count = helper.sentenceCount(poem_content)

                # class
                class_poem = helper.getStringFromFile(DATASET_PATH + "/" + poet + "/" + poem + "/CLASS.txt")

                # PEOM_POET
                data = {
                    "poem": poem,
                    "poet": poet
                }

                POEM_POET_SET.append(data)

                ### DataSet
                data['source_url'] = source_url
                data['timestamp'] = source_timestamp
                data['word_count'] = poem_word_count
                data['sentence_count'] = poem_sentence_count

                DATA_LIST.append(data)

                data = {
                    "poem": poem,
                    "poet": poet,
                    "source": {
                        "url": source_url,
                        "timestamp": source_timestamp
                    },
                    'class': class_poem,
                    "content": poem_content
                }

                CONTENT_LIST.append(data)

            except Exception as ex:
                traceback.print_exc()
                print(poet + '->' + poem)


def print_stats():
    genjam_chars = ['|', '‘', '’', "'", '"', '…', '-', ' ', '“', '”', '`'] + digits + punctuations

    def clean_str(string):
        new_string = string
        for c in genjam_chars:
            new_string = new_string.strip(c)

        if (len(new_string) - len(string)) < 0:
            return clean_str(new_string)

        else:
            return new_string

    CLASS_DATA = []
    CLASS_STAT = {}
    WORD_STAT = {}
    MAX_WORD_LEN = 0
    LONGEST_WORD = ''

    for data in CONTENT_LIST:
        row_data = {
            'poem': data['content'],
            'genre': data['class'],
        }

        if data['class'] in CLASS_STAT.keys():
            CLASS_STAT[data['class']] += 1
        else:
            CLASS_STAT[data['class']] = 1

        words_poem = re.split('\n|।|\||,|_| +|!|॥|\.|\?|—|…|\]|\[|\(|\)|\{|\}|\*|\u00A0|\u0009', data['content'])

        for word in words_poem:
            word = word.strip()
            word = word.replace(' ', '')
            word = word.replace('\uFEFF', '')
            word = word.replace('\u200D', '')
            word = word.replace('\u200C', '')
            word = word.replace('\u00A0', '')
            word = word.replace('\u0009', '')

            word = clean_str(word)

            if word == '':
                continue

            if word in WORD_STAT.keys():
                WORD_STAT[word] += 1
            else:
                WORD_STAT[word] = 1

        CLASS_DATA.append(row_data)

    total_poems = 0
    total_classes = len(CLASS_STAT.keys())
    for x in CLASS_STAT.keys():
        print(x + ' -> ' + str(CLASS_STAT[x]))
        total_poems += CLASS_STAT[x]

    print('total class -> {}'.format(total_classes))
    print('total poems -> {}'.format(total_poems))

    total_words = len(WORD_STAT.keys())
    for x in WORD_STAT.keys():
        #print(x + ' -> ' + str(WORD_STAT[x]))

        if len(x) > MAX_WORD_LEN:
            MAX_WORD_LEN = len(x)
            LONGEST_WORD = x

    print('total unique words -> {}'.format(total_words))
    print('max word len -> {}'.format(MAX_WORD_LEN))
    print('longest word -> {}'.format(LONGEST_WORD))
    print('genres > {}'.format(CLASS_STAT.keys()))


def build_poet_stat():
    POET = {}

    for data in DATA_LIST:
        try:
            POET[data['poet']] = POET[data['poet']] + 1

        except Exception as e:
            POET[data['poet']] = 1

    for poet in POET.keys():
        data = {
            "poet": poet,
            "poem_count": POET[poet]
        }

        POET_STAT_LIST.append(data)


def build_global_stat():
    TOTAL_POEMS = 0
    TOTAL_POETS = 0
    TOTAL_WORDS = 0
    TOTAL_SENTENCES = 0
    AVG_POEMS_POET = 0.0
    AVG_WORDS_POET = 0.0
    AVG_SENTENCE_POET = 0.0
    AVG_WORDS_POEM = 0.0
    AVG_SENTENCE_POEM = 0.0
    AVG_WORDS_SENTENCE = 0.0

    for data in POET_STAT_LIST:
        TOTAL_POETS += 1
        TOTAL_POEMS += data['poem_count']

    AVG_POEMS_POET = TOTAL_POEMS / TOTAL_POETS

    for data in DATA_LIST:
        TOTAL_WORDS += data['word_count']
        TOTAL_SENTENCES += data['sentence_count']

    AVG_WORDS_POET = TOTAL_WORDS / TOTAL_POETS
    AVG_SENTENCE_POET = TOTAL_SENTENCES / TOTAL_POETS
    AVG_WORDS_POEM = TOTAL_WORDS / TOTAL_POEMS
    AVG_SENTENCE_POEM = TOTAL_SENTENCES / TOTAL_POEMS
    AVG_WORDS_SENTENCE = TOTAL_WORDS / TOTAL_SENTENCES

    data = {
        "total_poets": TOTAL_POETS,
        "total_poems": TOTAL_POEMS,
        "total_words": TOTAL_WORDS,
        "total_sentences": TOTAL_SENTENCES,
        "avg_poems/poet": AVG_POEMS_POET,
        "avg_words/poet": AVG_WORDS_POET,
        "avg_sentences/poet": AVG_SENTENCE_POET,
        "avg_words/poem": AVG_WORDS_POEM,
        "avg_sentences/poem": AVG_SENTENCE_POEM,
        "avg_words/sentence": AVG_WORDS_SENTENCE
    }

    GLOBAL_STAT_LIST.append(data)

if __name__ == '__main__':
    import_dataset_from_raw_dataset()

    #print_stats()

    build_poet_stat()
    # helper.writeDataToCsv(data=POET_STAT_LIST, filePath=POET_STAT_CSV_PATH)

    build_global_stat()
    helper.writeDataToCsv(data=GLOBAL_STAT_LIST, filePath=GLOBAL_STAT_CSV_PATH)
