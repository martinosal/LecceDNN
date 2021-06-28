#!/usr/bin/env python
# coding: utf-8

# In[1]:


#import data_preprocess_functions as dp_f
import argparse, configparser
import re
import ast
import random

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import gridspec
import os

from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.utils import shuffle

from tensorflow.keras.utils import to_categorical

from tensorflow.keras import Model
from tensorflow.keras import models
from tensorflow.keras import layers
from tensorflow.keras.models import Sequential


# In[2]:


import makeplots as mkplots

def find(str_jets,df):
    n=0
    for i in df['origin']==str_jets:
        if i==True:
            n+=1
    return n
    
    

def composition_plot(df,directory,signal,analysis,channel,PreselectionCuts):
    x=np.array([])
    samples=list(set(df['origin']))
    for var in samples:
        x=np.append(x,find(var,df))

    plt.figure(1,figsize=(18,6))
    plt.bar(samples,x)
    #plt.text(3, 80, analysis+' '+channel , fontsize=12,horizontalalignment='center',verticalalignment='center')
#    plt.suptitle(analysis+' '+channel+' composition')
    plt.yscale('log')
    plt.savefig(directory+'/'+signal+'_'+analysis+'_'+channel+'_'+PreselectionCuts+'_composition.pdf')
#    plt.show()
    return x,samples
    


# In[3]:


analysis='merged'
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
if analysis == 'merged':
    dataVariables = ast.literal_eval(config.get('config', 'InputFeaturesMerged'))
elif analysis == 'resolved':
    dataVariables = ast.literal_eval(config.get('config', 'InputFeaturesResolved'))

#DSID must not be included in the configfile! #
#It's important the order here ! 
dataVariables.append('isSignal')
dataVariables.append('origin')
dfPath = config.get('config', 'dfPath')


data=pd.read_pickle(dfPath+'MixData_PD_'+analysis+'_'+channel+'__p4.pkl')
data=data[dataVariables]


def LoadData(dfPath,file_name):
    dfInput = dfPath + file_name
    df = pd.read_pickle(dfInput)
    columns=df.columns
    X = df.values
    y = np.array(df['isSignal'])
    return X, y, columns, df



for i in range(1,6):
    signal=samples[-i]

    outdir=dfPath+'outDF/'+str(signal)+'_'+analysis+'_'+channel+'_'+PreselectionCuts+'/'
    if not os.path.isdir(outdir):
        os.mkdir(outdir)
        print('created: ',outdir)
    else:
        print(outdir,'already exists')
        
#    print(signal)
    training_samples=samples[:5]
    training_samples.append(signal)
    print(training_samples)
    q_string=''
    for k in range(0,len(training_samples)):
        q_string+='origin.str.match("'+training_samples[k]+'") or '
    q_string=q_string[:-4]
#    print(q_string)
    data_set=data.query(q_string, engine='python')
#    data_set=data_set.drop('origin',1)
    data_set.to_pickle(outdir+ signal+'Data_' + analysis + '_' + channel + '_' + PreselectionCuts+'_p4.pkl')
    print(outdir+ signal+'Data_' + analysis + '_' + channel + '_' + PreselectionCuts+'_p4.pkl','saved')
    #directory='outDF/'+signal+ '_' + analysis+ '_' + channel+ '_' + PreselectionCuts+'/'
    


for i in range(1,6):
    
    signal=samples[-i]
    outdir=dfPath+'outDF/'+str(signal)+'_'+analysis+'_'+channel+'_'+PreselectionCuts+'/'
    if not os.path.isdir(outdir):
        os.mkdir(outdir)
        print('created: ',outdir)
    else:
        print(outdir,'already exists')

    signal=samples[-i]

    file_name=signal+'Data_' + analysis + '_' + channel + '_' + PreselectionCuts+'_p4.pkl'
    X,y,columns,df=LoadData(outdir, file_name)
    composition=composition_plot(df, outdir, signal, analysis, channel, PreselectionCuts)
    print(composition)

    
    test_frac=0.2
    #X, y = shuffle(X, y, random_state=0)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_frac)


    #masses=np.sort(np.array(list(set(list(X_train[:,-3].flatten())))))
    #print(masses)

    #scaler_train = RobustScaler().fit(X_train[:,:-1])
    scaler_train = StandardScaler().fit(X_train[:,:-2])
    X_train_scaled=np.array(scaler_train.transform(X_train[:,:-2]), dtype=object)
    X_test_scaled=np.array(scaler_train.transform(X_test[:,:-2]), dtype=object)

    y_train_cat=to_categorical(y_train)
    y_test_cat=to_categorical(y_test)

    print('train: ',X_train_scaled.mean(),X_train_scaled.std())
    print('test: ',X_test_scaled.mean(),X_test_scaled.std())

    X_train_scaled_m=np.insert(X_train_scaled, X_train_scaled.shape[1], X_train[:,-2], axis=1)
    X_test_scaled_m=np.insert(X_test_scaled, X_test_scaled.shape[1], X_test[:,-2], axis=1)


    np.savetxt(outdir+"X_train.csv",X_train,delimiter=',',fmt='%s')
    np.savetxt(outdir+"X_train_scaled.csv",X_train_scaled,delimiter=',')
    np.savetxt(outdir+"X_train_scaled_m.csv",X_train_scaled_m,delimiter=',',fmt='%s')
    np.savetxt(outdir+"X_test.csv",X_test,delimiter=',',fmt='%s')
    np.savetxt(outdir+"X_test_scaled.csv",X_test_scaled,delimiter=',')
    np.savetxt(outdir+"X_test_scaled_m.csv",X_test_scaled_m,delimiter=',',fmt='%s')
    np.savetxt(outdir+"y_train.csv",y_train,delimiter=',')
    np.savetxt(outdir+"y_train_cat.csv",y_train_cat,delimiter=',')
    np.savetxt(outdir+"y_test.csv",y_test,delimiter=',')
    np.savetxt(outdir+"y_test_cat.csv",y_test_cat,delimiter=',')


