import os

from smart_m3.m3_kp_api import *

class KP_Handler:
    def __init__(self, kp=None):
        self.kp = kp

    def handle(self, added, removed):

        for triple in added:
            if (int(str(triple[2])) % 2 == 0):
                print('Agent_Y:')
                print('stop adding even numbers!')
                kp.load_rdf_remove(triple)
                

if __name__ == '__main__':
    kp = m3_kp_api(KP_name='Agent_Y')
    
    subscription_triple = Triple(URI('Agent_X'), URI('has_item'), None)
    handler = KP_Handler(kp)
    handler_subscription = kp.load_subscribe_RDF(subscription_triple, handler)

    try:
        while 'alive':
            pass

    except KeyboardInterrupt:
        pass

    kp.load_unsubscribe(handler_subscription)

    kp.clean_sib

    kp.leave()

    raise os._exit(0)