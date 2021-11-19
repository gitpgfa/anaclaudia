import pandas as pd
import numpy as np
from statsmodels.sandbox.stats.runs import runstest_1samp, runstest_2samp
from scipy.stats import kstest
from statsmodels.tools.validation import array_like
from scipy import stats
import math

#Micrometeorological data quality index (MDQI)
def consecutiveEqual(df : pd.DataFrame):
	return (df.diff() == 0).astype(int)
	
def gaps(df : pd.DataFrame, gap = -9999):
	df.fillna(gap, inplace = True)
	return (df == gap).astype(int)
	
def xSD(df : pd.DataFrame):
	std = df.std()
	mean = df.mean()
	out = (df - mean)/std
	out = out.abs()
	out = out.apply(np.ceil)
	return out

def summary(df : pd.DataFrame, gap = -9999, qtdXStd = 3, add_consecutive = True):
    consec = consecutiveEqual(df)
    if(not add_consecutive):
        consec.iloc[:] = 0
    gap = gaps(df)
    xsd = xSD(df)
    xsd = xsd > qtdXStd

    total = len(df)
    perc_consec = consec.sum()/total
    perc_gap = gap.sum()/total
    perc_outlier = xsd.sum()/total
    out = pd.concat([perc_consec,perc_gap, perc_outlier],axis = 1)
    out.rename(columns={0:'Consective',1:'Gaps',2:'Outlier'}, inplace = True)
    if(add_consecutive):
        out['MDQI'] = (out['Consective']+out['Gaps']+out['Outlier'])/3
    else:
        out['MDQI'] = (out['Gaps']+out['Outlier'])/2
    return out


if __name__ == "__main__":
	data = pd.read_csv('INMET/2018/INMET_CO_DF_A001_BRASILIA_01-01-2018_A_31-12-2018.CSV',sep=';',decimal=',',header = 8)
	x = summary(data.iloc[:,2:])
	print(x)
