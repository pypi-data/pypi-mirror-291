# -*- coding: utf-8 -*-
from basic import Concurrent
from tqdm import tqdm
import pandas as pd
import numpy as np

def calc_ks_auc(data, var_list, target_list, weight=None, bins=None, partition=None, ascending=None, n_pro=30):
    def subtask(q_in, q_out, data, index_list, target_list, bins, partition, ascending):
        ascending_list = [ascending] if ascending else [True,False]
        while 1:
            try:
                var = q_in.get(timeout=1)
            except:
                continue
            if bins:
                data['value'] = np.qcut(data.eval(var), bins=bins, duplicates='drop')
            else:
                data['value'] = np.eval(var).round(3)
            columns = ['ks_%s' % target for target in target_list] + ['auc_%s' % target for target in target_list]
            if partition:
                grouped = data.groupby(by=partition+['value'],as_index=False)[index_list].sum()
                result = pd.DataFrame()
                for ascending in ascending_list:
                    temp = grouped.sort_values(by='value',ascending=ascending)
                    temp[['Cum%s' % index for index in index_list]] = temp.groupby(by=partition)[index_list].cumsum()
                    for target in target_list:
                        temp['PctCumBad_%s' % target] = temp['CumBad_%s' % target] / temp['Bad_%s' % target].sum()
                        temp['PctCumGood_%s' % target] = temp['CumGood_%s' % target] / temp['good_%s' % target].sum()
                        temp['ks_%s' % target] = temp['PctCumBad_%s' % target] - temp['PctCumGood_%s' % target]
                        temp['auc_%s' % target] = (temp['PctCumBad_%s' % target] + temp.groupby(by=partition)['PctCumBad_%s' % target].shift(1).fillna(0)) * (temp['PctCumGood_%s' % target] - temp.groupby(by=partition)['PctCumGood_%s' % target].shift(1).fillna(0)) / 2
                    temp = pd.merge(temp.groupby(by=partition,as_index=False)[['ks_%s' % target for target in target_list]].max(), temp.groupby(by=partition,as_index=False)[['auc_%s' % target for target in target_list]].sum(), how='inner', on=partition)
                    result = result.append(temp,ignore_index=True)
                result = result.groupby(by=partition,as_index=False)[columns].max()
            else:
                grouped = data.groupby(by='value',as_index=False)[index_list].sum()
                result = []
                for ascending in ascending_list:
                    temp = grouped.sort_values(by='value',ascending=ascending)
                    temp[['Cum%s' % index for index in index_list]] = temp[index_list].cumsum()
                    for target in target_list:
                        temp['PctCumBad_%s' % target] = temp['CumBad_%s' % target] / temp['Bad_%s' % target].sum()
                        temp['PctCumGood_%s' % target] = temp['CumGood_%s' % target] / temp['good_%s' % target].sum()
                        temp['ks_%s' % target] = temp['PctCumBad_%s' % target] - temp['PctCumGood_%s' % target]
                        temp['auc_%s' % target] = (temp['PctCumBad_%s' % target] + temp['PctCumBad_%s' % target].shift(1).fillna(0)) * (temp['PctCumGood_%s' % target] - temp['PctCumGood_%s' % target].shift(1).fillna(0)) / 2
                    result.append(list(temp[['ks_%s' % target for target in target_list]].max())+list(temp[['auc_%s' % target for target in target_list]].sum()))
                result = pd.DataFrame(columns=columns, data=result)[columns].max()
            result['var'] = var
            q_out.put(result)
    if partition and type(partition) == str:
        partition = [partition]
    index_list = []
    for target in target_list:
        if weight:
            data['Total_%s' % target] = (data[target] >= 0) * data[weight]
            data['Bad_%s' % target] = (data[target] == 1) * data[weight]
            data['Good_%s' % target] = data['Total_%s' % target] - data['Bad_%s' % target]
        else:
            data['Total_%s' % target] = (data[target] >= 0) * 1
            data['Bad_%s' % target] = (data[target] == 1) * 1
            data['Good_%s' % target] = data['Total_%s' % target] - data['Bad_%s' % target]
        index_list += ['Bad_%s' % target, 'Good_%s' % target]
    con = Concurrent(n_pro, subtask, data, index_list, target_list, bins, partition, ascending)
    con.put(var_list)
    result = pd.DataFrame()
    for i in tqdm(var_list):
        output = con.get()
        result = result.append(output,ignore_index=True)
    con.exit()
    return result




