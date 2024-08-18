# -*- coding: utf-8 -*-
from basic import Concurrent
from tqdm import tqdm
import pandas as pd
import numpy as np


def cart_binning(data, var_list, target, min_cnt=100, min_pct=0.05, min_gain=0.001, max_bins=10, weight=None, ascending=None, n_pro=30):
    def subtask(q_in, q_out, data, min_cnt, min_pct, min_gain, max_bins, ascending):
        while 1:
            try:
                var = q_in.get(timeout=1)
            except:
                continue
            data['value'] = data.eval(var).round(3)
            mesh = pd.merge(data[['cnt','value']].drop_duplicates(), data[['cnt','target']].drop_duplicates(), how='inner', on='cnt')[['value','target']]
            grouped = mesh.merge(data.groupby(by=['value','target'],as_index=False)[['cnt','sum']].sum(), how='left', on=['value','target']).fillna(0)
            grouped.sort_values(by='value',ascending=True,inplace=True)
            grouped['cutoff'] = (grouped['value'] + grouped.groupby(by='target')['value'].shift(-1)) / 2
            temp = grouped.groupby(by='target',as_index=False)['cnt'].sum()
            temp['sqr'] = np.square(temp['cnt'])
            intervals = []
            gini_values = [1-temp['sqr'].sum()/np.square(temp['cnt'].sum())]
            mean_values = [grouped['sum'].sum()/grouped['cnt'].sum()]
            index = 0
            while index <= len(intervals):
                lbound = -np.inf if index == 0 else intervals[index-1]
                ubound = np.inf if index == len(intervals) else intervals[index]
                temp = grouped[(grouped['value'] > lbound) & (grouped['value'] < ubound)].copy()
                temp.sort_values(by='value',ascending=True,inplace=True)
                temp[['cnt_1','sum_1']] = temp.groupby(by='target')[['cnt','sum']].cumsum()
                temp['cnt_2'] = temp['cnt'].sum() - temp['cnt_1']
                temp['sum_2'] = temp['sum'].sum() - temp['sum_1']
                temp['sqr_1'] = np.square(temp['cnt_1'])
                temp['sqr_2'] = np.square(temp['cnt_2'])
                temp = temp.groupby(by='cutoff',as_index=False)[['cnt_1','cnt_2','sum_1','sum_2','sqr_1','sqr_2']].sum()
                temp['pct_1'] = temp['cnt_1'] / grouped['cnt'].sum()
                temp['pct_2'] = temp['cnt_2'] / grouped['cnt'].sum()
                temp['avg_1'] = temp['sum_1'] / temp['cnt_1']
                temp['avg_2'] = temp['sum_2'] / temp['cnt_2']
                temp['gini_1'] = 1 - temp['sum_1'] / np.square(temp['cnt_1'])
                temp['gini_2'] = 1 - temp['sum_2'] / np.square(temp['cnt_2'])
                temp['gini'] = (temp['gini_1'] * temp['cnt_1'] + temp['gini_2'] * temp['cnt_2']) / grouped['cnt'].sum()
                temp = temp[(temp['cnt_1'] >= min_cnt) & (temp['cnt_2'] >= min_cnt)]
                temp = temp[(temp['pct_1'] >= min_pct) & (temp['pct_2'] >= min_pct)]
                temp = temp[temp['gini'] <= gini_values[index]-min_gain]
                if ascending == True:
                    temp = temp[temp['avg_1'] <= temp['avg_2']]
                    if index > 0:
                        temp = temp[temp['avg_1'] >= mean_values[index-1]]
                    if index < len(intervals):
                        temp = temp[temp['avg_2'] <= mean_values[index+1]]
                elif ascending == False:
                    temp = temp[temp['avg_1'] >= temp['avg_2']]
                    if index > 0:
                        temp = temp[temp['avg_1'] <= mean_values[index-1]]
                    if index < len(intervals):
                        temp = temp[temp['avg_2'] >= mean_values[index+1]]
                if not temp.empty:
                    opt = temp.sort_values(by='gini',ascending=True).iloc[0]
                    intervals.insert(index, opt['cutoff'])
                    gini_values[index] = opt['gini_2']
                    gini_values.insert(index, opt['gini_1'])
                    mean_values[index] = opt['avg_2']
                    mean_values.insert(index, opt['avg_1'])
                else:
                    index += 1
            while len(intervals) + 1 > max_bins:
                gain_list = []
                for index,cutoff in enumerate(intervals):
                    lbound = -np.inf if index == 0 else intervals[index-1]
                    ubound = np.inf if index == len(intervals)-1 else intervals[index+1]
                    temp = grouped[(grouped['value'] > lbound) & (grouped['value'] < ubound)].copy()
                    temp1 = temp[temp['value'] < cutoff].groupby(by='target',as_index=False)['cnt'].sum()
                    temp1['sqr'] = np.square(temp1['cnt'])
                    temp2 = temp[temp['value'] < cutoff].groupby(by='target',as_index=False)['cnt'].sum()
                    temp2['sqr'] = np.square(temp2['cnt'])
                    gini_1 = 1 - temp1['sqr'].sum()/np.square(temp1['cnt'].sum())
                    gini_2 = 1 - temp2['sqr'].sum()/np.square(temp2['cnt'].sum())
                    gini = (gini_1 * temp1['cnt'] + gini_2 * temp2['cnt']) / grouped['cnt'].sum()
                    temp = temp.groupby(by='target',as_index=False)['cnt'].sum()
                    temp['sqr'] = np.square(temp['cnt'])
                    gini_m = (1 - temp['sqr'].sum()/np.square(temp['cnt'].sum())) * temp['cnt'].sum() / grouped['cnt'].sum()
                    gain = gini_m - gini
                    gain_list.append(gain)
                index = [i for i,gain in gain_list if i == max(gain_list)][0]
                _ = intervals.pop(index)
            intervals.insert(0,-np.inf)
            intervals.append(np.inf)
            data['bucket'] = np.cut(data['value'], intervals, include_lowest=True).astype('str')
            grouped = data.groupby(by=['bucket','target'],as_index=False)[['cnt','sum']].sum()
            grouped['sqr'] = np.square(grouped['cnt'])
            result = grouped.groupby(by='bucket',as_index=False)[['cnt','sum','sqr']].sum()
            result['pct'] = result['cnt'] / result['cnt'].sum()
            result['avg'] = result['sum'] / result['cnt']
            result['gini'] = (1 - result['sqr']/np.square(result['cnt'])) * result['cnt'] / result['cnt'].sum()
            result['lbound'] = result['bucket'].apply(lambda x : round(float(x.split(',')[0].strip('(')),3))
            result['ubound'] = result['bucket'].apply(lambda x : round(float(x.split(',')[1].strip(']')),3))
            result['bucket'] = '(' + result['lbound'].astype('str') + ',' + result['ubound'].astype('str') + (')' if result['ubound'] == np.inf else ']')
            result['bin'] = result.index + 1
            result['var'] = var
            q_out.put(result)
    if weight:
        if type(weight) == str:
            data['cnt'] = (data[target] >= 0) * data[weight]
            data['sum'] = (data[target] >= 0) * data[weight] * data[target]
        else:
            data['cnt'] = (data[target] >= 0) * data[weight[0]]
            data['sum'] = (data[target] >= 0) * data[weight[1]] * data[target]
    else:
        data['cnt'] = (data[target] >= 0) * 1
        data['sum'] = (data[target] >= 0) * data[target]
    data['target'] = data.eval(target).round(3)
    con = Concurrent(n_pro, subtask, data, min_cnt, min_pct, min_gain, max_bins, ascending)
    con.put(var_list)
    columns = ['var','bin','bucket','lbound','ubound','cnt','pct','avg','gini']
    result = pd.DataFrame(columns=columns)
    for i in tqdm(var_list):
        output = con.get()
        result = result.append(output[columns],ignore_index=True)
    con.exit()
    gini_tbl = result.groupby(by='var',as_index=False)['gini'].agg({'bins':'count','gini':'sum'}).sort_values(by='gini',ascending=True).reset_index(drop=True)
    bin_tbl = result.merge(gini_tbl, how='inner', on='var', suffixes=('','_tol')).sort_values(by=['gini_tol','bin'],ascending=True).reset_index(drop=True)
    return gini_tbl, bin_tbl



def bin_pref(data, bin_tbl, target_list):
    return






