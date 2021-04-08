#!/usr/bin/env python
# coding: utf-8


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from tree_importer import tree_importer
import gc
from matplotlib.backends.backend_pdf import PdfPages
from quality_cuts import quality_cuts
import matplotlib as mpl



"""
 All the nonesences ( $\chi$2 < 0), inf and nan were deleted. Also applied
 quality cuts based on detector geometry. Full description could be found in
 https://docs.google.com/document/d/11f0ZKPW8ftTVhTxeWiog1g6qdsGgN1mlIE3vd5FHLbc/edit?usp=sharing

"""


df_original = tree_importer('/home/olha/CBM/dataset/10k_events_PFSimplePlainTree.root',
                     'PlainTree')

gc.collect()


new_labels= ['chi2geo', 'chi2primneg', 'chi2primpos', 'chi2topo', 'cosineneg',
       'cosinepos', 'cosinetopo', 'distance', 'eta', 'l', 'ldl',
       'mass', 'p', 'pT', 'phi', 'px', 'py', 'pz', 'rapidity',
             'x', 'y', 'z', 'daughter1id', 'daughter2id', 'isfrompv', 'pid', 'issignal']


df_original.columns = new_labels


sgnal = df_original[df_original['issignal']==1]
bg = df_original[df_original['issignal']==0]


signal = quality_cuts(sgnal)
background = quality_cuts(bg)

mpl.rc('figure', max_open_warning = 0)

def hist_variables(df_s, df_b, feature, pdf_key):

    fig, ax = plt.subplots(figsize=(20, 10))

    plt.hist(df_s[feature], label = 'signal', bins = 500, alpha = 0.4, color = 'green')
    plt.hist(df_b[feature], label = 'background', bins = 500, alpha = 0.2, color = 'magenta')
    plt.legend(shadow=True,title = 'B/S='+ str(round(len(df_b)/len(df_s), 3)) + '\n inf, nan was deleted \n $\chi^2$>0 '+
              '\n mass > 1.077 Gev/c , pz >0'+
               '\n z > 0, z<80, l > 0, l < 80, ldl > 0, |x|,|y|<50'+
               '\n cosinepos, cosineneg > 0' +
               '\n distance > 0, distance <100'
               '\n S samples:  '+str(df_s.shape[0]) + '\n B samples: '+ str(df_b.shape[0])
               , title_fontsize=20, fontsize =20)


    ax.xaxis.set_tick_params(labelsize=25)
    ax.yaxis.set_tick_params(labelsize=25)

    plt.title(feature + ' MC ', fontsize = 25)
    ax.set_xlabel(feature, fontsize = 25)


    ax.set_yscale('log')

    fig.tight_layout()

    plt.savefig(pdf_key,format='pdf')


non_log_x = ['cosineneg', 'cosinepos', 'cosinetopo',  'mass', 'pT', 'rapidity', 'phi', 'eta', 'x', 'y',
            'px', 'py', 'pz', 'l', 'ldl']

log_x = ['chi2geo', 'chi2primneg', 'chi2primpos', 'chi2topo', 'distance', 'z']

new_log_x = []

for feat in log_x:
    signal[feat+'_log'] = np.log(signal[feat])
    background[feat+'_log'] = np.log(background[feat])

    new_log_x.append(feat+'_log')


features = non_log_x + new_log_x




pdf_cuts = PdfPages('dist_cuts.pdf')
for feat in features:
    hist_variables(signal, background, feat, pdf_cuts)

pdf_cuts.close()
