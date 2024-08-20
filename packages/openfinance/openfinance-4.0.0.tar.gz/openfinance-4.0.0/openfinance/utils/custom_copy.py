import copy

UNCOPABLE = [
    "websocket",
    "callback_manager"
]

def custom_copy(
    obj
):
    if isinstance(obj, dict):
        uniq_objs = {}
        for k in UNCOPABLE:
            if k in obj:
                uniq_objs[k] = obj.pop(k)
        new_obj = copy.deepcopy(obj)
        new_obj.update(uniq_objs)
        return new_obj
    return copy.deepcopy(obj)