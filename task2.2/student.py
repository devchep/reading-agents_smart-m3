import os
import time
from smart_m3.m3_kp_api import *


class Student_Handler:
    def __init__(self, queue_position, kp=None, student_name=None, reading_divider=' ', is_class_finished=False):
        self.kp = kp
        self.student_name = student_name
        self.reading_divider = reading_divider
        self.is_class_finished = is_class_finished
        self.queue_position = queue_position

    def handle(self, added, removed):

        for removed_triple in removed:

            tr_subject, tr_predicate, tr_object = [
                str(x) for x in removed_triple]

            # Check if someone left
            if tr_predicate == 'has_position':
                tr_object = int(tr_object)

                # Update my position if needed
                if tr_object < self.queue_position:
                    self.queue_position -= 1
                    update_triple = [Triple(URI(self.student_name), URI(
                        'has_position'), Literal(self.queue_position))]
                    delete_triple = [
                        Triple(URI(self.student_name), URI('has_position'), None)]
                    # Load update
                    kp.load_rdf_update(update_triple, delete_triple)



        for added_triple in added:

            tr_subject, tr_predicate, tr_object = [
                str(x) for x in added_triple]

            # Check if it's my turn to read
            if tr_predicate == 'reading_queue':
                reading_queue_position = int(tr_object)
                
                if reading_queue_position == self.queue_position:
                    # Get text to read
                    text_triples = [
                        Triple(
                            URI('reading_class'), URI('has_text'), None),
                        Triple(
                            URI('reading_class'), URI('text_pointer'), None),
                    ]
                    kp.load_query_rdf(text_triples)

                    # Read text
                    text, pointer = [str(x[2]) for x in kp.result_rdf_query]
                    pointer = int(pointer)
                    print(text.split(reading_divider)[pointer])
                    time.sleep(1)

                    update_triples = []
                    delete_triples = []
                    # Update text pointer
                    update_triples.append(Triple(URI('reading_class'), URI(
                        'text_pointer'), Literal(pointer+1)))
                    delete_triples.append(kp.result_rdf_query[1])

                    # Update reading queue
                    query_triples = [
                        Triple(None, URI('has_join'), URI('reading_class')),
                    ]
                    kp.load_query_rdf(query_triples)
                    queue_length = len(kp.result_rdf_query)

                    if queue_length == 1:  # Solo reader
                        kp.load_rdf_remove(Triple(URI('reading_class'), URI(
                            'reading_queue'), None))  # needs to be deleted, otherwise there will be no insertion in load_update

                    reading_queue_position = (
                        reading_queue_position + 1) % queue_length

                    update_triples.append(Triple(URI('reading_class'), URI(
                        'reading_queue'), Literal(reading_queue_position)))
                    delete_triples.append(added_triple)

                    # Load update
                    kp.load_rdf_update(update_triples, delete_triples)

            # Check if class is finished
            if tr_predicate == 'class_status' and tr_object == 'finished':
                self.is_class_finished = True



if __name__ == '__main__':
    STUDENT_NAME = input('Enter student\'s name\n')
    kp = m3_kp_api()

    # Join class
    kp.load_rdf_insert(
        Triple(URI(STUDENT_NAME), URI('has_join'), URI('reading_class')))

    query_triples = [
        Triple(None, URI('has_join'), URI('reading_class')),
        Triple(URI('reading_class'), URI('text_divider'), None)
    ]
    kp.load_query_rdf(query_triples)

    # Get position in reading queue and put it in the SIB
    queue_length = len(kp.result_rdf_query) - 1
    my_queue_position = queue_length - 1
    kp.load_rdf_insert(
        Triple(URI(STUDENT_NAME), URI('has_position'), Literal(my_queue_position)))

    # Get reading divider
    reading_divider = str(kp.result_rdf_query[-1][2])

    # Subscriptions
    student_handler = Student_Handler(
        my_queue_position, kp, STUDENT_NAME, reading_divider)

    reading_queue_triple = Triple(
        URI('reading_class'), URI('reading_queue'), None)
    class_status_triple = Triple(
        URI('reading_class'), URI('class_status'), None)
    student_positions_triple = Triple(None, URI('has_position'), None)
        

    queue_subscription = kp.load_subscribe_RDF(
        reading_queue_triple, student_handler)
    status_subscription = kp.load_subscribe_RDF(
        class_status_triple, student_handler)
    student_positions = kp.load_subscribe_RDF(
        student_positions_triple, student_handler)

    # Works until the class is end
    try:
        while not student_handler.is_class_finished:
            pass

    except KeyboardInterrupt:
        pass

    print('Goodbye!')
    kp.load_rdf_remove([
        Triple(URI(STUDENT_NAME), URI('has_join'), URI('reading_class')),
        Triple(URI(STUDENT_NAME), URI('has_position'),
               None)
    ])
    kp.load_unsubscribe(queue_subscription)
    kp.load_unsubscribe(status_subscription)
    kp.load_unsubscribe(student_positions)
    kp.leave()
    raise os._exit(0)
