import os
import random
import time

from smart_m3.m3_kp_api import *

class KP_Handler:
    def __init__(self, kp=None):
        self.kp = kp

    def handle(self, added, removed):
        print('Agent_X:')

        if removed:
            print("I'm really sorry!")
            return

        print(added, ' added')

if __name__ == '__main__':
    kp = m3_kp_api(KP_name='Agent_X')

    subscription_triple = Triple(URI('Agent_X'), URI('has_item'), None)
    handler = KP_Handler(kp)
    handler_subscription = kp.load_subscribe_RDF(subscription_triple, handler)
    
    try:
        while 'alive':
            insert_triple = Triple(URI('Agent_X'), URI('has_item'), Literal(random.randint(0, 100000)))
            kp.load_rdf_insert(insert_triple)
            time.sleep(3)

    except KeyboardInterrupt:
        pass

    kp.clean_sib

    kp.leave()

    raise os._exit(0)