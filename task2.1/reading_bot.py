import os
from time import localtime, strftime, sleep
from smart_m3.m3_kp_api import *

TEXT_DIVIDER = None # split sep


def read_fragment(triple):
    fragment = str(triple[2])
    print(fragment, strftime("%H:%M:%S", localtime()))
    sleep(2)
    kp.load_rdf_remove(triple)


class ReadingBot_Handler:
    def __init__(self, kp=None):
        self.kp = kp

    def handle(self, added, removed):

        for added_triple in added:

            tr_subject, tr_predicate, tr_object = [
                str(x) for x in added_triple]

            if tr_predicate == 'has_fragment_to_read':
                read_fragment(added_triple)

        for removed_triple in removed:

            tr_subject, tr_predicate, tr_object = [
                str(x) for x in removed_triple]

            if tr_predicate == 'has_fragment_to_read':
                kp.load_query_rdf([
                    Triple(URI('reading_bot'), URI('has_text'), None),
                    Triple(URI('reading_bot'), URI(
                        'has_text_pointer'), None)]
                )

                text, text_pointer = [str(x[2]) for x in kp.result_rdf_query]
                divided_text = text.split(TEXT_DIVIDER)
                text_pointer = int(text_pointer) + 1
                text_fragment = divided_text[text_pointer]

                insert_triples = [
                    Triple(URI('reading_bot'), URI(
                        'has_fragment_to_read'), Literal(text_fragment)),
                    Triple(URI('reading_bot'), URI(
                        'has_text_pointer'), Literal((text_pointer) % len(divided_text)))
                ]

                kp.load_rdf_update(insert_triples, [kp.result_rdf_query[1]])


if __name__ == '__main__':
    kp = m3_kp_api()

    # Subscriptions
    bot_handler = ReadingBot_Handler(kp)
    read_text_triple = Triple(
        URI('reading_bot'), URI('has_fragment_to_read'), None)

    read_subscription = kp.load_subscribe_RDF(
        read_text_triple, bot_handler)

    # Check if I have fragment to read and find out the fragment if not
    kp.load_query_rdf(
        Triple(URI('reading_bot'), URI('has_fragment_to_read'), None)
    )
    current_text_fragment = kp.result_rdf_query
    if not current_text_fragment:
        kp.load_query_rdf(Triple(URI('reading_bot'), URI(
            'has_text_pointer'), None))

        text_pointer = 0
        # If text_pointer was left from previous session
        if kp.result_rdf_query:
            text_pointer = int(str(kp.result_rdf_query[0][2]))

        kp.load_query_rdf(Triple(URI('reading_bot'), URI('has_text'), None))

        text_fragment = str(kp.result_rdf_query[0][2]).split(
            TEXT_DIVIDER)[text_pointer]

        insert_triples = [
            Triple(URI('reading_bot'), URI(
                'has_fragment_to_read'), Literal(text_fragment)),
            Triple(URI('reading_bot'), URI(
                'has_text_pointer'), Literal(text_pointer))
        ]
        kp.load_rdf_insert(insert_triples)

    else:
        read_fragment(current_text_fragment[0])

    try:
        while True:
            pass

    except KeyboardInterrupt:
        pass

    kp.load_rdf_remove([
        Triple(URI('reading_bot'), URI('has_fragment_to_read'), None),
        Triple(URI('reading_bot'), URI(
            'has_text_pointer'), Literal(0))
    ])
    kp.load_unsubscribe(read_subscription)
    kp.leave()
    raise os._exit(0)
