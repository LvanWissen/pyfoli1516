import pickle
import simplekml

def calculate_statistics(lang, study, token_counter_total, lemma_counter_total, longest_sentences_total, entity_counter_total, n_filter, n_sent_total, id=None, filename=None):

    print()
    if id is not None:
        print("Statistics for thesis id %d (%s)" % (id, filename))
        print("\tStudy: %s" % study)
        print("\tLanguage %s" % lang)
        print()
    else:
        print("Statistics for filter lang=%s and study=%s" % (lang, study))

    n_wf = sum(token_counter_total.values())
    n_wf_avg = n_wf/n_filter
    n_wf_unq = len(token_counter_total)
    print("\tNumber of wordforms (average): %d (%d)" % (n_wf, n_wf_avg))

    n_lem = len(lemma_counter_total)
    n_lem_avg = n_lem/n_filter
    print("\tNumber of unique lemmas (average): %d (%d)" % (n_lem, n_lem_avg))

    n_sent_total_avg = n_sent_total/n_filter
    print("\tNumber of sentences (average): %d (%d)" % (n_sent_total, n_sent_total_avg))

    type_token_ratio = round(n_lem/n_wf_unq, 2)
    print("\tType:Token ratio:", type_token_ratio, "%d:%d" % (n_lem,n_wf_unq))
    print()

    print("\tMost frequent wordforms (wf, count):")
    for n, (item, count) in enumerate(token_counter_total.most_common(10)):
        print("\t",n+1,item, "(%d)" % count)
    print()

    print("\tMost frequent lemmas (lemma, count):")
    for n, (item, count) in enumerate(lemma_counter_total.most_common(10)):
        print("\t",n+1,item, "(%d)" % count)
    print()

    longest_sentences = sorted(longest_sentences_total, reverse=True)[:10]
    print("\t10 longest sentences (length in wf, sentence, sourcefile):")
    for n, (count, item, sourcefile) in enumerate(longest_sentences):
        wordlist = item.split()
        begin = " ".join(wordlist[:10])
        end = " ".join(wordlist[-10:])
        print("\t",n+1,end, "...", end, "(%d) %s" % (count,sourcefile))
    print()

    #ENTITIES
    entity_list = [(uri[0], count) for uri, count in entity_counter_total.most_common(10)]
    print("\tMost frequent entities:")
    for n, (item, count) in enumerate(entity_list):
        print("\t",n+1, item, "(%d)" % count)
    print()

    person_list = [(uri[0], count) for uri, count in entity_counter_total.most_common() if uri[1] == "person"][:10]
    print("\tMost frequent persons:")
    for n, (item, count) in enumerate(person_list):
        print("\t",n+1, item, "(%d)" % count)
    print()

    place_list = [(uri[0], count) for uri, count in entity_counter_total.most_common() if uri[1] == "place"][:10]
    print("\tMost frequent places:")
    for n, (item, count) in enumerate(place_list):
        print("\t",n+1, item, "(%d)" % count)
    print()


def make_kml(entity_counter_total, directory, study):
    """
    Outputs a kml file containing all the coordinates from entities from a study.

    This is done using the simplekml package. The coordinates are retrieved from a pickled defaultdict and are stored in order of (latitude, longitude). The simplekml module requires them the other way around.
    """

    kml_object = simplekml.Kml()
    cache_entities = pickle.load(open("cache_entities.bin", "rb"))

    for (uri,ent_type), count in entity_counter_total.items():
        coordinates = cache_entities[uri]

        if type(coordinates) == tuple:
            (lat, lon) = coordinates
            coords = (lon, lat)
            kml_object.newpoint(name=uri, coords=[coords])

    filename = directory + "_" + study + ".kml"
    kml_object.save(filename)
    print("Saved kml as", filename)








