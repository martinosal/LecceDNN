import os
import re
import numpy as np

SAMPLE='TCC'

SIGNAL=[]
BKG=[]
INPUT_FILE=[]
dataType=[]

modelPath='../Models/'
rootBranchSubSample=['DSID', 'lep1_m', 'lep1_pt', 'lep1_eta', 'lep1_phi', 'lep2_m', 'lep2_pt', 'lep2_eta', 'lep2_phi', 'fatjet_m', 'fatjet_pt', 'fatjet_eta', 'fatjet_phi', 'fatjet_D2', 'NJets', 'weight', 'Zcand_m', 'Zcand_pt', 'Pass_MergHP_GGF_ZZ_Tag_SR', 'Pass_MergHP_GGF_ZZ_Untag_SR', 'Pass_MergLP_GGF_ZZ_Tag_SR', 'Pass_MergLP_GGF_ZZ_Untag_SR', 'Pass_MergHP_GGF_ZZ_Tag_ZCR', 'Pass_MergHP_GGF_ZZ_Untag_ZCR', 'Pass_MergLP_GGF_ZZ_Tag_ZCR', 'Pass_MergLP_GGF_ZZ_Untag_ZCR', 'Pass_isVBF', 'Wdijet_m', 'Wdijet_pt', 'Wdijet_eta', 'Wdijet_phi', 'Zdijet_m', 'Zdijet_pt', 'Zdijet_eta', 'Zdijet_phi', 'sigWJ1_m', 'sigWJ1_pt', 'sigWJ1_eta', 'sigWJ1_phi', 'sigWJ2_m', 'sigWJ2_pt', 'sigWJ2_eta', 'sigWJ2_phi', 'sigZJ1_m', 'sigZJ1_pt', 'sigZJ1_eta', 'sigZJ1_phi', 'sigZJ2_m', 'sigZJ2_pt', 'sigZJ2_eta', 'sigZJ2_phi']
InputFeaturesMerged=['lep1_m', 'lep1_pt', 'lep1_eta', 'lep1_phi', 'lep2_m', 'lep2_pt', 'lep2_eta', 'lep2_phi', 'fatjet_m', 'fatjet_pt', 'fatjet_eta', 'fatjet_phi', 'fatjet_D2', 'NJets', 'Zcand_m', 'Zcand_pt', 'DSID']
InputFeaturesResolved=['lep1_m', 'lep1_pt', 'lep1_eta', 'lep1_phi', 'lep2_m', 'lep2_pt', 'lep2_eta', 'lep2_phi', 'Zcand_m', 'Zcand_pt', 'Wdijet_m', 'Wdijet_pt', 'Wdijet_eta', 'Wdijet_phi', 'Zdijet_m', 'Zdijet_pt', 'Zdijet_eta', 'Zdijet_phi', 'sigWJ1_m', 'sigWJ1_pt', 'sigWJ1_eta', 'sigWJ1_phi', 'sigWJ2_m', 'sigWJ2_pt', 'sigWJ2_eta', 'sigWJ2_phi', 'sigZJ1_m', 'sigZJ1_pt', 'sigZJ1_eta', 'sigZJ1_phi', 'sigZJ2_m', 'sigZJ2_pt', 'sigZJ2_eta', 'sigZJ2_phi', 'NJets', 'DSID']

if SAMPLE=='TCC':
    dfPath='/nfs/kloe/einstein4/HDBS/NN_InputDataFrames/TCC_DataFrames/'
    PATH_signal='/nfs/kloe/einstein4/HDBS/CxAODReader_output/TCC/out_ZV2Lep_TCC_EMTopo_SIGNAL/fetch/data-MVATree/'
    PATH_bkg='/nfs/kloe/einstein4/HDBS/CxAODReader_output/TCC/out_ZV2Lep_TCC_EMTopo_BKG/fetch/data-MVATree/'

SIGNAL_files=os.listdir(PATH_signal)
for file_str in SIGNAL_files:
    obj_str=re.search('(.+?).root', file_str).group(1)
    SIGNAL.append(obj_str)


BKG_files=os.listdir(PATH_bkg)
for file_str in BKG_files:
    obj_str=re.search('(.+?).root', file_str).group(1)
    if re.search('data(.+?)',obj_str)==None:
        #print(re.search('data(.+?)',obj_str).group(0))
        BKG.append(obj_str)
        INPUT_FILE.append(obj_str)
        dataType.append('bkg')


SIGNAL_np=np.array(SIGNAL)


for signal in SIGNAL_np:
    INPUT_FILE.append(signal)
    dataType.append('sig')

INPUT_PATH='/nfs/kloe/einstein4/HDBS/CxAODReader_output/TCC/INPUT/'
if not(os.path.exists(INPUT_PATH)):
    os.mkdir(INPUT_PATH)

with open("MyConfig.txt", "w") as text_file:
    text_file.write('[config]\n')
    text_file.write("ntuplePath = %s" % INPUT_PATH)
    text_file.write('\n')
    text_file.write('dfPath = %s' % dfPath)
    text_file.write('\n')
    text_file.write('modelPath = %s' % modelPath)
    text_file.write('\n')
    text_file.write('inputFiles = %s' % INPUT_FILE)
    text_file.write('\n')
    text_file.write('dataType   = %s' % dataType)
    text_file.write('\n')
    text_file.write('rootBranchSubSample = %s' %rootBranchSubSample)
    text_file.write('\n')
    text_file.write('InputFeaturesMerged = %s' %InputFeaturesMerged)
    text_file.write('\n')
    text_file.write('InputFeaturesResolved = %s' %InputFeaturesResolved)
    text_file.write('\n')
