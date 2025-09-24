'''
    Cprof profiling for assignment 6
'''

# pylint: disable=W1514,C0200
import cProfile
import main

# Name replace of file, mongo | lite
with open("cprofile_stats_mongo.txt", "a+") as f_:
    fn_calls = [{"Load status":
                 cProfile.run("main.load_status_updates('test_status.csv')")}] 
    ###     # Second call below this line, the return is None,
            # therefore, copy paste of output to text file to
            # match function name
    ###
    #[{"Load users": cProfile.run("main.load_users('test_accounts.csv')")}]

    for x in fn_calls:
        for key,val in x.items():
            f_.write(f"""\n *****{key.capitalize()}*****"\n{val}""")
    f_.close()
