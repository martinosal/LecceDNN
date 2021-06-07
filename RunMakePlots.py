#!/usr/bin/env python
# coding: utf-8
import sys
sys.path.append('/afs/le.infn.it/user/c/centonze/private/DiBosonAnalysis/LecceDNN')

import pandas as pd
import numpy as np
import matplotlib as plt
import argparse, configparser
import re
import ast
import random
from Functions import checkCreateDir, ShufflingData
import os
from Functions import *


import makeplots as mkplots

def plot_var(list_var,samples,var_str,plt_str,path,directory):
    fig=plt.figure(figsize=(16,8))
    #for l in range(0,len(list_var)):
    plt.hist(list_var,label=samples,bins=100,stacked=True,alpha=0.8)

    plt.title(directory)
    plt.yscale('log')
    plt.xlabel(var_str)
    plt.legend()
    plt.savefig(path+directory+'/'+var_str+'_'+plt_str+'.pdf')
    plt.close(fig)
#    plt.show()
    

analysis='resolved'
channel='ggF'
PreselectionCuts=''
samples=['Zjets','Wjets','stop','Diboson','ttbar','Radion','VBFRSG','RSG','VBFRadion','VBFHVTWZ']

### Reading from config file
config = configparser.ConfigParser()
config.read('MyConfig.txt')
inputFiles = ast.literal_eval(config.get('config', 'inputFiles'))
dataType = ast.literal_eval(config.get('config', 'dataType'))
rootBranchSubSample = ast.literal_eval(config.get('config', 'rootBranchSubSample'))
dfPath = config.get('config', 'dfPath')

#list of files under dfPath
files=os.listdir(dfPath)
#InputFeaturesResolved for 'resolved' analysis --> make it dyn
dataVariables=ast.literal_eval(config.get('config', 'InputFeaturesResolved'))



path='./plots/'
directory=analysis+'_'+channel+''+PreselectionCuts
mkplots.check_dir(path,directory)


mixed_data=pd.read_pickle(dfPath+'MixData_PD_'+analysis+'_'+channel+'.pkl')
pd_name='MixData_PD_'+analysis+'_'+channel

print(dataVariables)

for var_str in dataVariables:
    print(var_str)
    l_var_df=mkplots.list_var_df(mixed_data,var_str,samples)

    x_size=np.array([])
    x_l_var=np.array(l_var_df)
    for i in range(0,len(x_l_var)):
        x_size=np.append(x_size,x_l_var[i].shape[0])

    l_var_df=x_l_var[np.argsort(x_size)]
    plot_var(l_var_df,np.array(samples)[np.argsort(x_size)],var_str,pd_name,path,directory)

