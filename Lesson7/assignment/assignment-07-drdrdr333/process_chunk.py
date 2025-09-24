''' Wrapper for MultiProcessing library '''

import multiprocessing

class ProcessChunk:
    ''' Process configurations '''
    def __init__(self, target_fn, *args_to_pass):
        self.target_fn = target_fn
        self.args_to_pass = args_to_pass
        self.process = None

    def start(self):
        ''' Start process '''
        self.process = multiprocessing.Process(
            target=self.target_fn,
            args=self.args_to_pass
        )
        self.process.start()
        return self

    def join(self):
        ''' Join to wait until completion of child '''
        self.process.join()
        return self
