import TEST
from Utils.ActionsRouter import ActionsRouter

def is_float(string):
    try:
        int(string)
    except:
        return False
    return True

def is_int(string):
    try:
        int(string)
    except:
        return False
    return True

def p(x):
    print (x)

def cycle(msg):
    if is_int(msg):
        TEST.cycle(1, int(msg))
    else:
        print("msg ({}) was not an int!".format(msg))
actions_router = ActionsRouter(actions={
    'morse': TEST.morse,
    'prnt': p,
    'cycle': cycle
})