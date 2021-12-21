import os

from smart_m3.m3_kp_api import *

def new_memories(triples):
    new_triples = []
    for triple in triples:
        new_triples.append(Triple(triple[0], triple[1], Literal('NO')))
    return new_triples

if __name__ == '__main__':
    kp = m3_kp_api()

    # insert some triples (X has secret, Y knows his secret, Z doesn't know)
    insert_list = [
        Triple(URI('Agent_X'), URI('secret'), Literal('secret_knowledge_i_dont_tell')),
        Triple(URI('Agent_X'), URI('know_secret'), Literal('YES')),
        Triple(URI('Agent_Y'), URI('know_secret'), Literal('YES')),
        Triple(URI('Agent_Z'), URI('know_secret'), Literal('YES')),
        Triple(URI('Agent_W'), URI('know_secret'), Literal('NO')),
        Triple(URI('Agent_Y'), URI('send_secret'), URI('Agent_Z')),
    ]
    kp.load_rdf_insert(insert_list)

    # wc query (get info if someone knows secret)
    kp.load_query_rdf(Triple(None, URI('know_secret'), Literal('YES')))
    print('Who knows the secret? \n{}'.format(kp.result_rdf_query))

    # erase(update) memories of everyone except X
    kp.load_query_rdf(Triple(None, URI('know_secret'), Literal('YES')))
    remove_list = list(filter(lambda triple: triple[0] != URI('Agent_X'), kp.result_rdf_query))
    new_triple = new_memories(remove_list)
    kp.load_rdf_update(new_triple, remove_list)

    # remove the evidence
    kp.load_rdf_remove(Triple(None, URI('send_secret'), None))

    # query (who know secret now?)
    kp.load_query_rdf(Triple(None, URI('know_secret'), Literal('YES')))
    print('The knowledge of secret after erasing memories? \n{}'.format(kp.result_rdf_query))

    kp.clean_sib

    kp.leave()

    raise os._exit(0)