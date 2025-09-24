''' For assignment 7 leverage data chunking  '''

# pylint: disable=W1514,W1309,W0611
import timeit
import pandas as pd
import main
from process_chunk import ProcessChunk
from exceptions import NonFileExtension

def profile_largest():
    ''' larger profile chunk size - 200 '''
    with open('time_it_profile.txt', 'a+', newline='\n') as _f:
        res_accounts_larger = timeit.timeit(f"import_csv_in_chunks('test_accounts.csv', size=100)",
                                            globals=globals(), number=1)
        _f.seek(0)
        _f.write(f"\n chunk size 10 accounts \n\n results: {res_accounts_larger}")
        res_status_larger = timeit.timeit(f"import_csv_in_chunks('test_status.csv', size=100)",
        globals=globals(), number=1)
        _f.seek(0)
        _f.write(f"\n chunk size 30 status \n\n results: {res_status_larger}")
    _f.close()

def profile_larger():
    '''timer/profile for larger chunk size - 50'''
    with open('time_it_profile.txt', 'a+', newline='\n') as _f:
        res_accounts_larger = timeit.timeit(f"import_csv_in_chunks('test_accounts.csv', size=50)",
                                            globals=globals(), number=1)
        _f.seek(0)
        _f.write(f"\n chunk size 10 accounts \n\n results: {res_accounts_larger}")
        res_status_larger = timeit.timeit(f"import_csv_in_chunks('test_status.csv', size=50)",
                                          globals=globals(), number=1)
        _f.seek(0)
        _f.write(f"\n chunk size 30 status \n\n results: {res_status_larger}")
    _f.close()

def profile():
    ''' timer for differnet chunk size - 10 '''
    with open('time_it_profile.txt', 'a+', newline='\n') as _f:
        _f.write(" This example is only using around 1000 records for baseline... \n")
        res_accounts = timeit.timeit(f"import_csv_in_chunks('test_accounts.csv')",
                                     globals=globals(), number=1)
        _f.seek(0)
        _f.write(f"\n chunk size 10 accounts \n\n results: {res_accounts}")
        res_status = timeit.timeit(f"import_csv_in_chunks('test_status.csv')",
                                   globals=globals(), number=1)
        _f.seek(0)
        _f.write(f"\n chunk size 10 status \n\n results: {res_status}")
    _f.close()

active_process = []

def check_process(amt_to_check):
    ''' Allows us not to join unless all processes have started '''
    if amt_to_check == len(active_process):
        for proc in active_process:
            proc.join()
        return True
    return False
        

def import_csv_in_chunks(filename, amt_to_kick_off, size=10):
    '''
    Imports CSV file in chunks of a defined size
    '''
    if 'account' in filename:
        for chunk in pd.read_csv(filename, chunksize=size, iterator=True):
            proc = ProcessChunk(main.load_users, chunk)
            proc.start()
            active_process.append(proc)
            check_process(amt_to_kick_off)
    elif 'status' in filename:
        for chunk in pd.read_csv(filename, chunksize=size, iterator=True):
            proc = ProcessChunk(main.load_status_updates, chunk)
            proc.start()
            active_process.append(proc)
            check_process(amt_to_kick_off)
