# -*- coding: utf-8 -*-
from basic import Concurrent
from tqdm import tqdm
import pandas as pd
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt

def woe_binning(data, var_list, target, min_cnt=100, min_pct=0.05, min_iv=0.001, max_bins=10, weight=None, ascending=None, n_pro=30):
    def subtask(q_in, q_out, data, target, min_cnt, min_pct, min_iv, max_bins, ascending):
        while 1:
            try:
                var = q_in.get(timeout=1)
            except:
                continue
            data['value'] = data.eval(var)
            grouped = data.groupby(by='value',as_index=False)[['Total','Bad','Good']].sum()
            grouped['cutoff'] = (grouped['value'] + grouped['value'].shift(-1)) / 2
            intervals = []
            badrates = [grouped['Bad'].sum()/grouped['Total'].sum()]
            index = 0
            while index <= len(intervals):
                lbound = -np.inf if index == 0 else intervals[index-1]
                ubound = np.inf if index == len(intervals) else intervals[index]
                temp = grouped[(grouped['value'] > lbound) & (grouped['value'] < ubound)].sort_values(by='value',ascending=True)
                temp[['Total_1','Bad_1','Good_1']] = temp[['Total','Bad','Good']].cumsum()
                temp['Total_2'] = temp['Total'].sum() - temp['Total_1']
                temp['Bad_2'] = temp['Bad'].sum() - temp['Bad_1']
                temp['Good_2'] = temp['Good'].sum() - temp['Good_1']
                temp['PctTotal_1'] = temp['Total_1'] / grouped['Total'].sum()
                temp['PctTotal_2'] = temp['Total_2'] / grouped['Total'].sum()
                temp['PctBad_1'] = temp['Bad_1'] / grouped['Bad'].sum()
                temp['PctBad_2'] = temp['Bad_2'] / grouped['Bad'].sum()
                temp['PctGood_1'] = temp['Good_1'] / grouped['Good'].sum()
                temp['PctGood_2'] = temp['Good_2'] / grouped['Good'].sum()
                temp['Badrate_1'] = temp['Bad_1'] / temp['Total_1']
                temp['Badrate_2'] = temp['Bad_2'] / temp['Total_2']
                temp['IV_1'] = (temp['PctBad_1'] - temp['PctGood_1']) * (np.log(temp['PctBad_1']) - np.log(temp['PctGood_1']))
                temp['IV_2'] = (temp['PctBad_2'] - temp['PctGood_2']) * (np.log(temp['PctBad_2']) - np.log(temp['PctGood_2']))
                temp['IV_all'] = (temp['PctBad_1'].max() - temp['PctGood_1'].max()) * (np.log(temp['PctBad_1'].max()) - np.log(temp['PctGood_1'].max()))
                temp['IV_gain'] = temp['IV_1'] + temp['IV_2'] - temp['IV_all']
                temp = temp[(temp['Total_1'] >= min_cnt) & (temp['Total_2'] >= min_cnt)]
                temp = temp[(temp['PctTotal_1'] >= min_pct) & (temp['PctTotal_2'] >= min_pct)]
                temp = temp[(temp['IV_gain'] >= min_iv) & (temp['IV_gain'] < np.inf)]
                if ascending == True:
                    temp = temp[temp['Badrate_1'] <= temp['Badrate_2']]
                    if index > 0:
                        temp = temp[temp['Badrate_1'] >= badrates[index-1]]
                    if index < len(intervals):
                        temp = temp[temp['Badrate_2'] <= badrates[index+1]]
                elif ascending == False:
                    temp = temp[temp['Badrate_1'] >= temp['Badrate_2']]
                    if index > 0:
                        temp = temp[temp['Badrate_1'] <= badrates[index-1]]
                    if index < len(intervals):
                        temp = temp[temp['Badrate_2'] >= badrates[index+1]]
                if not temp.empty:
                    opt = temp.sort_values(by='IV_gain',ascending=False).iloc[0]
                    intervals.insert(index,opt['cutoff'])
                    badrates[index] = opt['Badrate_2']
                    badrates.insert(index,opt['Badrate_1'])
                else:
                    index += 1
            while len(intervals) + 1 > max_bins:
                iv_list = []
                for index, cutoff in enumerate(intervals):
                    lbound = -np.inf if index == 0 else intervals[index-1]
                    ubound = np.inf if index == len(intervals)-1 else intervals[index+1]
                    temp = grouped[(grouped['value'] > lbound) & (grouped['value'] < ubound)].copy()
                    temp1 = temp[temp['value'] < cutoff].copy()
                    temp2 = temp[temp['value'] > cutoff].copy()
                    values = {}
                    values['PctBad'] = temp['Bad'].sum() / grouped['Bad'].sum()
                    values['PctBad_1'] = temp1['Bad'].sum() / grouped['Bad'].sum()
                    values['PctBad_2'] = temp2['Bad'].sum() / grouped['Bad'].sum()
                    values['PctGood'] = temp['Good'].sum() / grouped['Good'].sum()
                    values['PctGood_1'] = temp1['Good'].sum() / grouped['Good'].sum()
                    values['PctGood_2'] = temp2['Good'].sum() / grouped['Good'].sum()
                    values['IV_all'] = (values['PctBad'] - values['PctGood']) * (np.log(values['PctBad']) - np.log(values['PctGood']))
                    values['IV_1'] = (values['PctBad_1'] - values['PctGood_1']) * (np.log(values['PctBad_1']) - np.log(values['PctGood_1']))
                    values['IV_2'] = (values['PctBad_2'] - values['PctGood_2']) * (np.log(values['PctBad_2']) - np.log(values['PctGood_2']))
                    iv_gain = values['IV_1'] + values['IV_2'] - values['IV_all']
                    iv_list.append(iv_gain)
                index = [i for i,iv in enumerate(iv_list) if iv == min(iv_list)][0]
                _ = intervals.pop(index)
            intervals.insert(0,-np.inf)
            intervals.append(np.inf)
            data['bucket'] = np.cut(data['value'], intervals, include_lowest=True).astype('str')
            result = data.groupby(by='bucket',as_index=False)[['Total','Bad','Good']].sum()
            result['PctTotal'] = result['Total'] / result['Total'].sum()
            result['PctBad'] = result['Bad'] / result['Bad'].sum()
            result['PctGood'] = result['Good'] / result['Good'].sum()
            result['Badrate'] = result['Bad'] / result['Total']
            result['WOE'] = np.log(result['PctBad']) - np.log(result['PctGood'])
            result['IV'] = (result['PctBad'] - result['PctGood']) * result['WOE']
            result['lbound'] = result['bucket'].apply(lambda x : round(float(x.split(',')[0].replace('(','').replace('[','')),3))
            result['ubound'] = result['bucket'].apply(lambda x : round(float(x.split(',')[1].replace(')','').replace(']','')),3))
            result['bucket'] = '(' + result['lbound'].astype('str') + ',' + result['ubound'].astype('str') + (')' if result['ubound'] == np.inf else ']')
            result['bin'] = result.index + 1
            result['var'] = var
            q_out.put(result)
    if weight:
        data['Total'] = (data[target] >= 0) * data[weight]
        data['Bad'] = (data[target] == 1) * data[weight]
    else:
        data['Total'] = (data[target] >= 0) * 1
        data['Bad'] = (data[target] == 1) * 1
    data['Good'] = data['Total'] - data['Bad']
    con = Concurrent(n_pro, subtask, data, target, min_cnt, min_pct, min_iv, max_bins, ascending)
    con.put(var_list)
    columns = ['var','bin','bucket','lbound','ubound','Total','Bad','Good','PctTotal','Badrate','WOE','IV']
    result = pd.DataFrame(columns=columns)
    for i in tqdm(var_list):
        output = con.get()
        result = result.append(output[columns],ignore_index=True)
    con.exit()
    iv_tbl = result.groupby(by='var',as_index=False)['IV'].agg({'bins':'count','IV':'sum'}).sort_values(by='IV',ascending=False)
    bin_tbl = iv_tbl.merge(result, how='inner', on='var', suffixes=('_tol',''))
    bin_tbl['order'] = bin_tbl['bins'] - bin_tbl['clus_num']
    bin_tbl = bin_tbl.sort_values(by=['IV_tol','order'],ascending=False)[columns].reset_index(drop=True)
    return iv_tbl, bin_tbl

def raw2woe(raw_data, var_list, bin_tbl):
    woe_data = raw_data[var_list].copy()
    for var in tqdm(var_list):
        bin_var = bin_tbl[bin_tbl['var'] == var].copy()
        woe_data[var] = 0
        for i in range(bin_var.shape[0]):
            value = bin_var.iloc[i]
            woe_data[var] += (raw_data[var] > value['lbound']) * (raw_data[var] <= value['ubound']) * value['WOE']
    return woe_data

def fwd_select(data, var_list, target, var_initial=[], tol=0.05, var_max=20):
    current_formula = '%s ~ %s + 1' % (target, ' + '.join(var_initial))
    current_score = smf.logit(current_formula, data).fit().aic
    var_choice = var_initial
    var_remain = [var for var in var_list if var not in var_choice]
    while len(var_remain) > 0:
        score_list = []
        for var in var_remain:
            formula = '%s ~ %s + 1' % (target, ' + '.join(var_choice+[var]))
            try:
                lr_res = smf.logit(formula, data).fit(method='newton', maxiter=100, disp=0, tol=tol)
            except Exception as error:
                print('Skipped %s due to %s' % (var, error))
                continue
            score = lr_res.aic 
            converged = lr_res.mle_retvals['converged']
            if converged:
                score_list.append((var,score))
            else: 
                print('Skipped %s due to not converged' % var)
                continue
        if len(score_list) > 0:
            score_list.sort(ascending=True)
            best_var, best_score = score_list[0]
        else:
            break
        if best_score < current_score:
            var_choice.append(best_var)
            var_remain.remove(best_var)
            current_formula = '%s ~ %s + 1' % (target, ' + '.join(var_choice))
            current_score = best_score
            print('Added %s' % best_var)
            lr_res = smf.logit(current_formula, data).fit(method='newton', maxiter=100, disp=0, tol=tol)
            p_values = lr_res.pvalues
            p_over = p_values[p_values > tol]
            if p_over.shape[0] > 0:
                for name in p_over.index:
                    try:
                        var_choice.remove(name)
                        print('Removed %s due to PValue=%s' % (name, p_over[name]))
                    except ValueError:
                        continue
            model_params = lr_res.params
            negative = model_params[model_params < 0]
        else:
            break
        if len(var_choice) >= var_max:
            break
    formula = '%s ~ %s + 1' % (target, ' + '.join(var_choice))
    lr_res = smf.logit(formula, data).fit(method='newton', maxiter=100, disp=0, tol=tol)
    return lr_res

def bkwd_select(data, var_list, target, threshold=5):
    var_choice = var_list.copy()
    while 1:
        vif = [variance_inflation_factor(data[var_choice].values,i) for i in range(len(var_choice))]
        if max(vif) > threshold:
            var_drop = [var_choice[i] for i,value in enumerate(vif) if value == max(vif)][0]
            print('Removed %s' % var_drop)
            var_choice.drop(var_drop)
        else:
            break
    formula = '%s ~ %s + 1' % (target, ' + '.join(var_choice))
    lr_res = smf.logit(formula, data).fit()
    return lr_res

def createcard(lr_res, bin_tbl, score0=660, odds0=1/15, pdo=15, ascending=False):
    B = pdo / np.log(2) * (-1 if ascending == True else 1)
    A = score0 + B * np.log(odds0)
    model_params = lr_res.params
    model_vars = [var for var in model_params.index if var != 'Intercept']
    scorecard = pd.DataFrame()
    for var in model_vars:
        bin_var = bin_tbl[bin_tbl['var'] == var].copy()
        bin_var['score'] = - B * model_params[var] * bin_var['WOE']
        scorecard = scorecard.append(bin_var,ignore_index=True)
    min_score = scorecard.groupby(by='var',as_index=False)['score'].min()
    score_basic = A - B * model_params['Intercept']
    score_amort = (score_basic + min_score['score'].sum()) / min_score.shape[0]
    scorecard = scorecard.merge(min_score, how='inner', on='var', suffixes=('_org','_min'))
    scorecard['score'] = scorecard.eval('score_org - score_min + %f' % score_amort).round(0)
    return scorecard

def raw2score(raw_data, scorecard):
    raw_data['score'] = 0
    for i in range(scorecard.shape[0]):
        value = scorecard.iloc[i]
        raw_data['score'] += (raw_data[value['var']] > value['lbound']) * (raw_data[value['var']] <= value['ubound']) * value['score']
    return raw_data['score']

def scorebucket(X, y, lr_res, bins=20):
    model_params = lr_res.params
    ln_odds = (X * model_params).sum(axis=1)
    prob = 1 / (np.exp(-ln_odds)+1)
    prob.name = 'Prob'
    prob = pd.DataFrame(prob)
    prob['Target'] = y 
    prob.sort_values(by='Prob', ascending=False, inplace=True)
    prob['Rank'] = 1
    prob.Rank = prob.Rank.cumsum()
    prob['Bucket'] = pd.qcut(prob.Rank, bins)
    return prob

def ksdistance(prob):
    bucket = prob.groupby('Bucket',as_index=False)['Target'].agg({'Total':'count','Bad':'sum','BadRate':'mean'})
    bucket.drop('Bucket', axis=1, inplace=True)
    bucket.eval('Good = Total - Bad', inplace=True)
    bucket['CumTotal'] =bucket['Total'].cumsum()
    bucket['CumBad'] = bucket['Bad'].cumsum()
    bucket['CumGood'] = bucket['Good'].cumsum()
    bucket['PctCumTotal'] = bucket['CumTotal'] / bucket['CumTotal'].max()
    bucket['PctCumBad'] = bucket['CumBad'] / bucket['CumBad'].max()
    bucket['PctCumGood'] = bucket['CumGood'] / bucket['CumGood'].max()
    bucket['KS'] = bucket['PctCumBad'] - bucket['PctCumGood']
    bucket.eval('Lift = PctCumBad/PctCumTotal', inplace=True)
    metric_ks = bucket['KS'].max()
    bucket[['PctCumBad','PctCumGood','KS','Lift']].plot(style=['r','b','g','y'], xlim=[0,bucket.shape[0]], ylim=[0,1], title='KS Distance = %.4f' % metric_ks)
    plt.xlabel('Score Buckets')
    plt.ylabel('Pct Distribution')
    plt.show() 
    return metric_ks, bucket




