import pandas as pd
import numpy as np
import matplotlib as plt
import argparse, configparser
import re
import ast
import random
import os.path
from Functions import *

def find_var(var_str):
    for i in range(0,len(dataVariables)):
        if var_str in dataVariables[i]:
            return i
            
def list_files(files,samples):
    list_f=list()
    for i in range(0,len(samples)):
        f_n=np.array([])
        for j in range(0,len(files)):
            f=re.search(samples[i]+'(.+?).pkl', files[j])
            if f:
                f_n=np.append(f_n,f.group(0))

        list_f.append(f_n.copy())
    return list_f

def list_var(dataVariables,var,samples,list_f):
    
    list_var=list()
    Nvar=len(samples)
    for k in range(0,Nvar):
        print('Sampling',dataVariables[var],'in',samples[k])
        var_np=np.array([])
        for f in list_f[k]:
            print('reading ',f)
            df = pd.read_pickle(dfPath+f)
            var_np=np.append(var_np,np.array(df[dataVariables[var]]))

        list_var.append(var_np.copy())
        print('Created ',dataVariables[var],' array for ', samples[k], 'collection')
    print('Done')
    return list_var
    
def list_var_df(df,var_str,samples):
#    var_str='lep1_pt'
#    var=find_var(var_str)

    list_var=list()
    Nvar=len(samples)
    for k in range(0,Nvar):
        print('Sampling',var_str,'in',samples[k])
        var_np=np.array([])
        x=np.array(df.query('origin.str.contains("'+samples[k]+'")', engine='python')[var_str])
        var_np=np.append(var_np,x)

        list_var.append(var_np.copy())
        print('Created ',var_str,' array for ', samples[k], 'collection')
    print('Done')
    return list_var

    
def check_dir(path,directory):
#    path='./plots/'
    mode=0o666
#    directory=analysis+'_'+channel+''+PreselectionCuts
    if not(os.path.exists(path+directory)):
        os.mkdir(path+directory,mode)
    else:
        print('already existing')
        
def plot_var(list_var,samples,var_str,plt_str,path,directory):
    fig=plt.figure(figsize=(16,8))
    #for l in range(0,len(list_var)):
    plt.hist(list_var,label=samples,bins=100,stacked=True,alpha=0.8)

    plt.title(directory)
    plt.yscale('log')
    plt.xlabel(var_str)
    plt.legend()
    plt.savefig(path+directory+'/'+var_str+'_'+plt_str+'.pdf')
#    plt.show()
    plt.close(fig)
    
    
def find(str_jets,df):
    n=0
    for i in df['origin']==str_jets:
        if i==True:
            n+=1
    return n
    
    
def composition_plot(df,samples,plt_str,path,directory):
    x=np.array([])
    for var in samples:
        x=np.append(x,find(var,df))

    fig=plt.figure(1,figsize=(18,6))
    plt.bar(samples,x)
    #plt.text(3, 80, analysis+' '+channel , fontsize=12,horizontalalignment='center',verticalalignment='center')
    plt.suptitle(plt_str+' composition')
    plt.yscale('log')
    plt.savefig(path+directory+'/'+'composition_'+plt_str+'.pdf')
#    plt.show()
    plt.close(fig)
