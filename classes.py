import os
from collections import Counter
from collections import defaultdict
from lxml import etree as ET

from functions import *

class RootDir():
    """
    By making this a class object, you can iterate over the thesises stored under them by calling next() onto it.
    """

    def __init__(self, path):
        """
        During the object initializion, the given folder is scanned for suitable files and they are converted to Objects. Displayed is how many files and studies there are found in the given folder.
        """
        self.path = path
        self.name = os.path.basename(path)
        self.index = -1 #used for iterating

        root, dirs, files = next(os.walk(self.path))
        fields = dirs

        self.thesises = []
        id = 0

        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith(".nohyphen") and os.path.getsize(os.path.join(root, file)) > 1:
                    filename = os.path.join(root, file)
                    language = os.path.dirname(filename).rsplit(os.sep,1)[1]
                    field = os.path.dirname(filename).rsplit(os.sep,2)[1]
                    self.thesises.append((id, filename, field, language))

                    id += 1 #counter

        # some statistics
        print("Found %d fields of study with a total of %d thesises inside folder %s." % (len(fields), len(self.thesises), self.name))

        for id, filename, field, language in self.thesises:
            name = "thesis%d" % id

            # create the class objects from the list
            globals()[name] = MasterThesis(id, filename, field, language)


    def __iter__(self, lang=None, study=None):
        object_list = []

        for i in range(len(self.thesises)):
            object_list.append(globals()["thesis" + str(i)])

        return iter(object_list)


    def __call__(self, lang=None, study=None):
        object_list = []

        # for i in range(len(self.thesises)):
        #     object_list.append(globals()["thesis" + str(i)])

        for id in self.list(lang=lang, study=study):
            object_list.append(globals()["thesis" + str(id)])

        return iter(object_list)


    def __next__(self):
        if self.index > len(self.thesises):
            raise StopIteration
        else:
            self.index += 1
            return globals()["thesis" + str(self.index)]


    def get_stats(self, lang=None, study=None):
        """
        Get statistics based on filter of studyfield and language.

        Possible filtering options are:
            lang= and study=

        The following is displayed:
            average number of tokens
            average number of types
            average number of sentences
            10 longest sentences
            frequency of each token
            frequency of each type
            the type token ratio
            the frequency of each entity
            the most frequent persons ('DBpedia:Person' in attribute 'type' of element 'entity')
            the most frequent locations ('DBpedia:Place' in attribute 'type' of element 'entity')


        """

        token_counter_total = Counter()
        lemma_counter_total = Counter()
        longest_sentences_total = []
        entity_counter_total = Counter()

        n_filter = 0 #used to calculate average
        n_sent_total = 0

        for thesis in self(lang=lang, study=study):
            n_filter += 1

            token_counter, lemma_counter, n_sent, longest_sentences, entity_counter = thesis.parse()

            token_counter_total.update(token_counter)
            lemma_counter_total.update(lemma_counter)
            n_sent_total += n_sent

            longest_sentences_total.extend(longest_sentences)
            entity_counter_total.update(entity_counter)

        #Calling the function!
        calculate_statistics(lang, study, token_counter_total, lemma_counter_total, longest_sentences_total, entity_counter_total, n_filter, n_sent_total)


    def get_stats_id(self, id):
        """
        Get statistics for a single file specified by id.

        Run the list() method to get an overview of avaiable ids and corresponding thesises.

        The following is displayed:
        average number of tokens
        average number of types
        average number of sentences
        10 longest sentences
        frequency of each token
        frequency of each type
        the type token ratio
        the frequency of each entity
        the most frequent persons ('DBpedia:Person' in attribute 'type' of element 'entity')
        the most frequent locations ('DBpedia:Place' in attribute 'type' of element 'entity')
        """

        n_filter = 1
        lang = globals()["thesis" + str(id)].language
        study = globals()["thesis" + str(id)].study
        filename = globals()["thesis" + str(id)].name

        token_counter, lemma_counter, n_sent, longest_sentences, entity_counter = globals()["thesis" + str(id)].parse()

        #Calling the function!
        calculate_statistics(lang, study, token_counter, lemma_counter, longest_sentences, entity_counter, n_filter, n_sent, id=id, filename=filename)


    def list(self, lang=None, study=None, verbose=False):
        """
        Gives a list of thesises with a possiblity to filter them.

        Returns a list of id's of thesises available as an object sorted on their id. It is possible to filter them using the following optional keywords:
                lang
                study
        """

        filterlist = []

        for id, filename, field, language in self.thesises:
            if (language == lang or lang is None) and (study == field or study is None):

                if verbose == True:
                    print("\t" + str(id), field, language, os.path.basename(filename))
                filterlist.append(id)

        return filterlist


    def get_kml(self, study):
        """
        Initializes a klm-generation based on a field of study. Provides the data needed. Uses function make_kml() to output the file.

        """

        entity_counter_total = Counter()

        for thesis in self(study=study):
            if thesis.entities == 0:
                thesis.parse()

            entity_counter_total.update(thesis.entities)

        #Run the function!
        make_kml(entity_counter_total, os.path.join(self.path, self.name), study)

class MasterThesis():

    def __init__(self, id, filename, field, language):
        self.path = filename
        self.name = os.path.basename(filename)
        self.id = id
        self.study = field
        self.language = language
        self.entities = 0

    def __call__(self):
        RootDir.get_stats_id(self, self.id)

    def __getattr__(self, name):
        self.__dict__[name] = MasterThesis()
        return self.__dict__[name]

    def parse(self):
        """
        Method responsible for parsing the thesis and preparing the data for calculating the statistics.
        """

        print("\t", self.id, self.name)

        # reading and parsing the NAF
        with open(self.path, encoding='UTF-8') as infile:
            xml = ET.parse(infile)

        root = xml.getroot()
        wf_gen = root.iterfind('text/wf')
        lem_gen = root.iterfind('terms/term')
        sent_gen = root.iterfind('text/wf')
        ent_gen = root.iterfind('entities/entity')

        #TOKENS
        token_list = []

        for wf_el in wf_gen:
            token = wf_el.text
            token_list.append(token)

        n_wf = len(token_list)
        token_counter = Counter(token_list)

        #LEMMAS
        lem_list = []

        for term_el in lem_gen:
            lemma = term_el.get('lemma')
            lem_list.append(lemma)

        n_lem = len(set(lem_list))
        lemma_counter = Counter(lem_list)


        #SENTENCES
        sent_counter = Counter()

        for wf_el in sent_gen:
            sent = [int(wf_el.get('sent'))]
            word = wf_el.text
            sent_counter.update(sent)

        n_sent = max(sent_counter)

        def find_sentence_by_number(n):
            wordlist = []
            wf_in_sentence = root.xpath("//wf[@sent=" + str(n) + "]")

            for wf_el in wf_in_sentence:
                wordlist.append(wf_el.text)

            return " ".join(wordlist)

        longest_sentences_n = sent_counter.most_common(10)
        longest_sentences = []

        for n, length in longest_sentences_n:
            longest_sentences.append((length, find_sentence_by_number(n), self.name))

        #ENTITIES
        entity_list = []

        for ent_el in ent_gen:
            entity_uri = ent_el.xpath('externalReferences/externalRef/@reference')[0]
            entity_types = ent_el.get('type')

            if "DBpedia:Person" in entity_types:
                entity_type = "person"
            elif "DBpedia:Place" in entity_types:
                entity_type = "place"
            else:
                entity_type = ""

            entity_list.append((entity_uri,entity_type))

        entity_counter = Counter(entity_list)

        #for future use with the kml-creation
        self.entities = entity_counter

        return(token_counter, lemma_counter, n_sent, longest_sentences, entity_counter)





