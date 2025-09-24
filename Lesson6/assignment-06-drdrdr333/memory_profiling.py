'''
    Memory Profiling for assignment 6
'''

from memory_profiler import profile
import sys
import main

_f = open('memory_profiler_results.txt', 'a+')

@profile(stream=_f)
def mongo_load_users():
    a = main.load_users('test_accounts.csv')
    return a

@profile(stream=_f)
def mongo_load_status():
    b = main.load_status_updates('test_status.csv')
    return b

@profile(stream=_f)
def mongo_update_user():
    b = main.update_user('Danit.Berni57', 'test@test.com', 'test', 'test')
    return b

@profile(stream=_f)
def mongo_search_user():
    b = main.search_user('Danit.Berni57')
    return b

@profile(stream=_f)
def mongo_delete_user():
    b = main.delete_user('Danit.Berni57')
    return b

@profile(stream=_f)
def mongo_update_status():
    b = main.update_status('QuintillaWitty', 'Quintilla.Witty8', 'new new text')
    return b

@profile(stream=_f)
def mongo_search_status():
    b = main.search_status('QuintillaWitty')
    return b

@profile(stream=_f)
def mongo_delete_status():
    b = main.delete_status('QuintillaWitty')
    return b

####################### SQL LITE #########################
# @profile(stream=_f)
# def lite_load_users():
#     a = main.load_users('test_accounts.csv')
#     return a

# @profile(stream=_f)
# def lite_load_status():
#     b = main.load_status_updates('test_status.csv')
#     return b

# @profile(stream=_f)
# def lite_update_user():
#     b = main.update_user('Danit.Berni57', 'test@test.com', 'test', 'test')
#     return b

# @profile(stream=_f)
# def lite_search_user():
#     b = main.search_user('Danit.Berni57')
#     return b

# @profile(stream=_f)
# def lite_delete_user():
#     b = main.delete_user('Danit.Berni57')
#     return b

# @profile(stream=_f)
# def lite_update_status():
#     b = main.update_status('QuintillaWitty', 'Quintilla.Witty8', 'new new text')
#     return b

# @profile(stream=_f)
# def lite_search_status():
#     b = main.search_status('QuintillaWitty')
#     return b

# @profile(stream=_f)
# def lite_delete_status():
#     b = main.delete_status('QuintillaWitty')
#     return b

if __name__ == '__main__':
    mongo_load_users()
    mongo_load_status()
    mongo_update_user()
    mongo_search_user()
    mongo_delete_user()
    mongo_update_status()
    mongo_delete_status()
    mongo_delete_status()