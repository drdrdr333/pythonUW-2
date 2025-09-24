'''
    Timeit Profiling for assingment 6
'''

# pylint: disable=W1514,C0200
import timeit
### Imported and used both modules for profiling... ###
# import mongo_connect
# import socialnetwork_model

SETUP_MONGO = """
from mock import Mock
import menu
"""

MAIN_MONGO = ["""
print('load users into Mongo DB from csv')
menu.load_users()
""",
"""
print('load status into Mongo DB from csv')
menu.load_status_updates()
""",
"""
print('update user Mongo')
menu.update_user()
""",
"""
print('search user Mongo')
menu.search_user()
""",
"""
print('delete user Mongo')
menu.delete_user()
""",
"""
print('update status Mongo')
menu.delete_user()
""",
"""
print('search status Mongo')
menu.delete_user()
""",
"""
print('delete status Mongo')
menu.delete_user = Mock(return_value=True)
"""
]


### CAN ADJUST AMT OF TIMES RUN VIA KWARG "number" in lines 54, 90
for x in range(len(MAIN_MONGO)):
    with open('timeit_profile_stats.txt', 'a+', newline="\n") as fi:
        res = timeit.timeit(MAIN_MONGO[x], SETUP_MONGO, number=1)
        funct = MAIN_MONGO[x]
        fi.seek(0)
        fi.write(f"\n***** FUNCTION CALLED*****\n call: {funct} \n time taken: {str(res)}")
    fi.close()

SETUP_LITE = """
import menu
"""

MAIN_LITE = ["""
print('load users into Sqlite DB from csv')
menu.load_users()
""",
"""
print('load status into Sqlite DB from csv')
menu.load_status_updates()
""",
"""
print('update user Sqlite')
menu.update_user()
""",
"""
print('search user Sqlite')
menu.search_user()
""",
"""
print('delete user Sqlite')
menu.delete_user()
"""
]



for x in range(len(MAIN_LITE)):
    with open('timeit_profile_stats.txt', 'a+', newline="\n") as fi:
        res = timeit.timeit(MAIN_LITE[x], SETUP_LITE, number=1)
        funct = MAIN_LITE[x]
        fi.seek(0)
        fi.write(f"\n***** FUNCTION CALLED*****\n call: {funct} \n time taken: {str(res)}")
    fi.close()
