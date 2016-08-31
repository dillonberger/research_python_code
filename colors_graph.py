# -*- coding: utf-8 -*-
"""
Created on Tue Aug 23 14:51:40 2016

@author: dillonberger
"""

from collections import OrderedDict

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import rc, rcdefaults
from matplotlib import colors
from matplotlib import cm

def rad_to_u(radius,percent,interp_list):
    ilist=interp_list[np.isclose(interp_list['R'],radius,atol=5e-1)]
    ilist=ilist[ilist['AGN%']==percent]
#    print("ilist is ", ilist)
#    print("u is ", np.array(ilist['U'])[0])
    return np.array(ilist['U'])[0]
    
#return an array of u's to add to the global dataframe
params2=pd.read_csv("hybrid_20_percent_agn_grid_model_rosetta.txt", delim_whitespace=True, usecols=["STOP_COLU"])

def get_ulist(df, interp_list):
    percent=df["%AGN"][0]
#    print("AGN% is ", percent)
    ulist=np.zeros(len(df['%AGN']))
    for i in range(len(df['%AGN'])):
        ith_row=df.iloc[[i]]
#        print(ith_row)
        radius=ith_row['radius'][i]
#        print("radius is ", radius)
        ulist[i]=rad_to_u(radius,percent,interp_list)
    df['U']=ulist
    df['column_den']=params2['STOP_COLU']
    return df

def fix_vals(df,col=19.000000,u=-4.54):
    return df[(df['U']==u) & (df['column_den']==col)]
    
def find_uniques(df,label):
    return np.unique(df[label])

def alt_fix_vals(df,col=19.000000,u=-4.54):
    return df[(df['U']==u) & (df['column_den']==col)]

def alt2_fix_vals(df,col=19.000000):
    return df[(df['column_den']==col)]
    
columns=["%AGN", "model_num", "FW1", "FW2", "FW3",
"FW4", "FW60", "FW100", "W1-W2", "W2-W3", "F60nu", "F100nu", "F60/F100"]

path1="/Users/dillonberger/Documents/research/low_z_out/alt_agn_"
path2="/Users/dillonberger/Documents/research/high_z_out/alt_agn_"
ext="_percent.out"

dfs={}

#array of dataframes indexed by %AGN

for i in np.arange(0,100,10):
    dfs[i//10]=pd.read_csv(path1+str(i)+ext, delimiter="   ", header=None, skiprows=1, names=columns)

params=pd.read_csv("/Users/dillonberger/Documents/research_python/model_order_dillon.csv")
interp=pd.read_csv("/Users/dillonberger/Documents/research_python/U.txt",delim_whitespace=True)
#print(interp)
for i in range(len(dfs)):
    dfs[i]['radius']=params['radius']


for i in range(0,100,10):
    get_ulist(dfs[i//10],interp)

for df in dfs.values():
    print(find_uniques(df,'U'))



#==============================================================================
# i=0
# for ix in range(5):
#     us=[]
#     for df in dfs.values():
#         unique_us=find_uniques(df,'U')
# #        print(unique_us[0])
#         df=fix_vals(df,u=unique_us[ix])
#         norm = colors.Normalize(vmin=np.min(df['model_num']), vmax=np.max(df['model_num']))
#         mapper = cm.ScalarMappable(norm=norm, cmap=cm.jet)
#     #    parsed_df=df['W1-W2','W2-W3','model_num']    
#     #    print(xs,ys)
#     #    print(df['U'])
#     #    exported=df[['%AGN','W1-W2','W2-W3','U']]
#     #    exported.to_csv("%agn_"+str(i)+"_"+"col_dens19.csv",index_label='model_num')
#         for j in range(len(df)):
#             us.append(unique_us[ix])
#             x=np.array(df.iloc[[j]]['W2-W3'])[0]
#             y=np.array(df.iloc[[j]]['W1-W2'])[0]
#             model_num=np.array(df.iloc[[j]]['model_num'])[0]
#             plt.scatter(x,y,label='model_num '+ str(model_num),color=mapper.to_rgba(model_num))
#         i=i+10
#     handles, labels = plt.gca().get_legend_handles_labels()
#     by_label = OrderedDict(zip(labels, handles))
#     lgd = plt.legend(by_label.values(), by_label.keys(),
#                     bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0)
#     #plt.legend()
#     plt.title('U$\in$['+str(us[0])+", "+str(us[-1])+"]")
#     plt.xlabel("W2-W3")
#     plt.ylabel("W1-W2")
#     plt.tight_layout()
#     plt.savefig(str(ix)+"plot.pdf",bbox_extra_artists=(lgd,), bbox_inches='tight')
#     plt.show()    
#  
#==============================================================================

#for df in dfs.values():
#    new_df=fix_vals(df,u=(0,1))
#    print(new_df)

#_____________________________________
# We want to take a model# and connect the W points for each AGN%
# We find the model number by 
#============
del dfs[8]
initial_us=[-4.54,-3.54,-2.54,-1.54,-0.54]
for ix in range(len(initial_us)):
    upper_model_num=len(alt_fix_vals(dfs[0], u=initial_us[ix]))
    print("upper model num is ", upper_model_num)
    iloc_counter=0
    for iloc_model in range(upper_model_num):
        print("iteration of iloc_model is ", iloc_counter)
        xs=[]
        ys=[]
        us=[]
#        model_locs=[]
        counter=0
        for df in dfs.values():
            unique_us=find_uniques(df,'U')
            df=alt_fix_vals(df,u=unique_us[ix])
            print("iteration of df is ", counter)
            loc_model=int(np.array(df.iloc[[iloc_model]]['model_num'])[0])
            print("loc model is ", loc_model)        
            us.append(np.array(df.iloc[[iloc_model]]['U'])[0])
            xs.append(np.array(df.iloc[[iloc_model]]['W2-W3'])[0])
            ys.append(np.array(df.iloc[[iloc_model]]['W1-W2'])[0])
            counter+=1
            model_locs=np.unique(df['model_num'])
        print("unique ionization params are ", np.unique(us))
        norm = colors.Normalize(vmin=min(model_locs), vmax=max(model_locs))
        mapper = cm.ScalarMappable(norm=norm, cmap=cm.jet)
        print("model locs are ", model_locs)
        plt.plot(xs,ys,label='model_num '+ str(loc_model),color=mapper.to_rgba(loc_model))
        iloc_counter+=1
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    lgd = plt.legend(by_label.values(), by_label.keys(),
                     bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0)
    plt.title('U$\in$['+str(us[0])+", "+str(us[-1])+"]")
    plt.xlabel("W2-W3")
    plt.ylabel("W1-W2")
    plt.tight_layout()
    plt.savefig(str(ix)+"plot.pdf",bbox_extra_artists=(lgd,), bbox_inches='tight')
    plt.show()    
  

#=========

  
