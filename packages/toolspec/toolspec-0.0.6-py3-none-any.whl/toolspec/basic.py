# -*- coding: utf-8 -*-
from multiprocessing import Process, Queue
from tqdm import tqdm
import numpy as np

class Concurrent:
    def __init__(self, n_pro, func, *args):
        self.n_pro = n_pro
        self.q_in = Queue(maxsize=-1)
        self.q_out = Queue(maxsize=-1)
        self.counter = 0
        self.p_list = []
        for i in range(self.n_pro):
            p = Process(func, self.q_in, self.q_out, *args, daemon=True)
            self.p_list.append(p)
            p.start()
    def put(self, input_list):
        for input in input_list:
            self.q_in.put(input)
            self.counter += 1
    def get(self):
        while self.check():
            try:
                output = self.q_out.get(timeout=1)
                self.counter -= 1
                return output
            except:
                continue
    def check(self):
        if sum([0 if p.alive() else 1 for p in self.p_list]) > 0:
            self.exit()
            raise('RuntimeError')
        return True
    def empty(self):
        return True if self.counter == 0 else False
    def overload(self):
        return True if self.counter >= self.n_pro else False
    def exit(self):
        self.q_out.close()
        for p in self.p_list:
            p.terminate()
            p.join()
    def __del__(self):
        self.exit()

def feature_processing(data, var_list , min_value=-np.inf, max_value=np.inf, fill_else=-9999, decimal=3):
    def limit(x):
        return x if x >= min_value and x <= max_value else fill_else
    for var in tqdm(var_list):
        data[var] = data[var].astype('float').apply(limit).round(decimal)

def target_processing(data, target_region, fill_na=0, fill_else=np.nan):
    for target in tqdm(list(target_region.keys())):
        data[target].fillna(fill_na,inplace=True)
        data.loc[~data.query(target_region[target]).index, target] = fill_else




