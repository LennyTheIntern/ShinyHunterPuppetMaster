from enum import Enum
from tracemalloc import start

eventCypher = {}


def subscribe_event_type_to_action(event_type:str,fn):
    if event_type not in eventCypher:
        eventCypher[event_type] = []
    eventCypher[event_type].append(fn)

def post_event(event_type:str,data):
    # if the event does not worrent a action, do nothing
    if event_type not in eventCypher:
        return
    # if the event worrents a action, perform the action
    for fn in eventCypher[event_type]:
        fn(data) # note that fn might post another event