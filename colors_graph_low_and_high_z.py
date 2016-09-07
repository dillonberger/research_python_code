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


# We change how matplotlib renders text in our plots
rcdefaults()
rc('font',**{'family':'serif','serif':['Computer Modern Roman']})
rc('text', usetex=False)


def rad_to_u(radius,percent,interp_list):
    ilist=interp_list[np.isclose(interp_list['R'],radius,atol=5e-1)]
    ilist=ilist[ilist['AGN%']==percent]
    return np.array(ilist['U'])[0]
    
#return an array of u's to add to the global dataframe
params2=pd.read_csv("/Users/dillonberger/Documents/research_python/hybrid_20_percent_agn_grid_model_rosetta.txt", 
                    delim_whitespace=True, usecols=["STOP_COLU"])

def append_u_and_col_den(df, interp_list):
    percent=df["%AGN"][0]
#    print("AGN% is ", percent)
    ulist=np.zeros(len(df['%AGN']))
    for i in range(len(df['%AGN'])):
        ith_row=df.iloc[[i]]
        radius=ith_row['radius'][i]
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
def append_cols(df,calling_df, new_df_label, calling_df_label):
    df[new_df_label]=calling_df[calling_df_label]

    

#labels on columns being read in from the .out file
columns=["%AGN", "model_num", "FW1", "FW2", "FW3",
"FW4", "FW60", "FW100", "W1-W2", "W2-W3", "F60nu", "F100nu", "F60/F100"]

#.out files are indexed by agn%
path1="/Users/dillonberger/Documents/research/low_z_out/alt_agn_"
path2="/Users/dillonberger/Documents/research/high_z_out/agn_"
ext="_percent.out"

dfs={}

#array of dataframes indexed by %AGN
#WHEN CHANGING FROM PATH 1 TO PATH 2 CHANGE UPPER BOUND ON ARANGE TO 90
for i in np.arange(0,100,10):
    dfs[i//10]=pd.read_csv(path1+str(i)+ext, delimiter="   ", 
        header=None, skiprows=1, names=columns, engine='python')
#csv read ins for jarrett box, and how parameters vary    
box=pd.read_csv("/Users/dillonberger/Documents/research_python/jarrettbox.csv", header=None)
params=pd.read_csv("/Users/dillonberger/Documents/research_python/model_order_dillon.csv")
interp=pd.read_csv("/Users/dillonberger/Documents/research_python/U.txt",delim_whitespace=True)

#tack on radius and gas density

for i in range(len(dfs)):
    append_cols(dfs[i],params,'radius','radius')
    append_cols(dfs[i],params,'n','n')
    append_u_and_col_den(dfs[i], interp)
    print(find_uniques(dfs[i], 'U'))

unique_coldens=np.unique(dfs[0]['column_den'])
print(unique_coldens)

#manually typing the unique ionization parameters for 0% AGN
us_for_0_percent=[-4.54,-3.54,-2.54,-1.54,-0.54]

def plot_W_colors(dfs=dfs,colden=19.0, us_for_0_percent=us_for_0_percent, delete_80=True,high_z=True):
#TURN ON DELETE_80=TRUE IF USING LOW_Z MODEL     
    if delete_80==True:
        for ix in range(len(us_for_0_percent)):
            #the number of models that have ionizatoin parameter us_for_0_percent[ix]
            #is the same for each agn% (i.e. each dataframe)
            #dfs[0] 
            upper_model_num=len(alt_fix_vals(dfs[0], col=colden, u=us_for_0_percent[ix]))
            print("number of models with u="+str(us_for_0_percent[ix])+" is ",upper_model_num)
            iloc_counter=0
            for iloc_model in range(upper_model_num):
#                print("iteration of iloc_model is ", iloc_counter)
                xs=[]
                ys=[]
                us=[]
                counter=0
                for df in dfs.values():
                    if df['%AGN'][0]==80.0:
                        continue
                    #loc_model IS CONSTANT THROUGHOUT THIS LOOP
                    unique_us=find_uniques(df,'U')
                    df=alt_fix_vals(df,col=colden,u=unique_us[ix])
#                    print("iteration of df is ", counter)
                    loc_model=int(np.array(df.iloc[[iloc_model]]['model_num'])[0])
                    #SPECIAL CONDITIONS FOR THE MIN AND MAX AGN PERCENTEGES 
                    if(np.array(df.iloc[[0]]['%AGN'])[0]==0):
                        plt.scatter(df.iloc[[iloc_model]]['W2-W3'],df.iloc[[iloc_model]]['W1-W2'],label='0 percent',facecolors='none', edgecolors='k')                      
                    if(np.array(df.iloc[[0]]['%AGN'])[0]==90.0):
                        plt.scatter(df.iloc[[iloc_model]]['W2-W3'],df.iloc[[iloc_model]]['W1-W2'],label='90 percent',facecolors='none', edgecolors='r')                                              
                    us.append(np.array(df.iloc[[iloc_model]]['U'])[0])
                    xs.append(np.array(df.iloc[[iloc_model]]['W2-W3'])[0])
                    ys.append(np.array(df.iloc[[iloc_model]]['W1-W2'])[0])
                    counter+=1
                    model_locs=np.unique(df['model_num'])
#                print("unique ionization params are ", np.unique(us))
                norm = colors.Normalize(vmin=min(model_locs), vmax=max(model_locs))
                mapper = cm.ScalarMappable(norm=norm, cmap=cm.jet)
#                print("model locs are ", model_locs)
                label='Radius = '+ str(np.array(dfs[0].loc[[loc_model]]['radius'])[0])+'  n = '+str(np.array(dfs[0].loc[[loc_model]]['n'])[0])        
                color=mapper.to_rgba(loc_model)
                plt.plot(xs,ys,label=label,color=color)
                iloc_counter+=1
            handles, labels = plt.gca().get_legend_handles_labels()
            by_label = OrderedDict(zip(labels, handles))
            lgd = plt.legend(by_label.values(), by_label.keys(),
                             bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0)
            plt.plot(box[0],box[1],'--',color='k')
            if high_z==True:
                zlabel='high_z'
            else:
                zlabel='low_z'            
            plt.title('U$\in$['+str(us[0])+", "+str(us[-1])+"], column density=  "+str(colden)+"  "+zlabel)
            plt.xlabel("W2-W3")
            plt.ylabel("W1-W2")   
            plt.tight_layout()
            bbox_inches='tight'
            plt.savefig(zlabel+"_"+str(ix)+"column_den_"+str(colden)+"_plot.pdf",bbox_extra_artists=(lgd,),bbox_inches=bbox_inches)
            plt.show()  
    else: 
        for ix in range(len(us_for_0_percent)):
            upper_model_num=len(alt_fix_vals(dfs[0],col=colden, u=us_for_0_percent[ix]))
#            print("upper model num is ", upper_model_num)
            iloc_counter=0
            for iloc_model in range(upper_model_num):
                print("iteration of iloc_model is ", iloc_counter)
                xs=[]
                ys=[]
                us=[]
                counter=0
                for df in dfs.values():
                    #loc_model IS CONSTANT THROUGHOUT THIS LOOP 
                    unique_us=find_uniques(df,'U')
                    df=alt_fix_vals(df,col=colden,u=unique_us[ix])
                    print("iteration of df is ", counter)
                    loc_model=int(np.array(df.iloc[[iloc_model]]['model_num'])[0])
                    #SPECIAL CONDITIONS FOR THE MIN AND MAX AGN PERCENTEGES                       
                    if(np.array(df.iloc[[0]]['%AGN'])[0]==0):
                        plt.scatter(df.iloc[[iloc_model]]['W2-W3'],df.iloc[[iloc_model]]['W1-W2'],label='0 percent',facecolors='none', edgecolors='k')   
                    if(np.array(df.iloc[[0]]['%AGN'])[0]==80.0):
                        plt.scatter(df.iloc[[iloc_model]]['W2-W3'],df.iloc[[iloc_model]]['W1-W2'],label='80 percent',facecolors='none', edgecolors='r')
                    us.append(np.array(df.iloc[[iloc_model]]['U'])[0])
                    xs.append(np.array(df.iloc[[iloc_model]]['W2-W3'])[0])
                    ys.append(np.array(df.iloc[[iloc_model]]['W1-W2'])[0])
                    counter+=1
                    model_locs=np.unique(df['model_num'])
                norm = colors.Normalize(vmin=min(model_locs), vmax=max(model_locs))
                mapper = cm.ScalarMappable(norm=norm, cmap=cm.jet)
#                print("model locs are ", model_locs)
                label='Radius = '+ str(np.array(dfs[0].loc[[loc_model]]['radius'])[0])+'  n = '+str(np.array(dfs[0].loc[[loc_model]]['n'])[0])        
                color=mapper.to_rgba(loc_model)
                plt.plot(xs,ys,label=label,color=color)
                iloc_counter+=1
            handles, labels = plt.gca().get_legend_handles_labels()
            by_label = OrderedDict(zip(labels, handles))
            lgd = plt.legend(by_label.values(), by_label.keys(),
                             bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0)
            plt.plot(box[0],box[1],'--',color='k') 
            if high_z==True:
                zlabel='high_z'
            else:
                zlabel='low_z'            
            plt.title('U$\in$['+str(us[0])+", "+str(us[-1])+"], column density=  "+str(colden)+"  "+zlabel)
            plt.xlabel("W2-W3")
            plt.ylabel("W1-W2")   
            plt.tight_layout()
            bbox_inches='tight'
            plt.savefig(zlabel+"_"+str(ix)+"column_den_"+str(colden)+"_plot.pdf",bbox_extra_artists=(lgd,),bbox_inches=bbox_inches)
            plt.show()    
i=0
for val in unique_coldens:
    print('iteration is ', i)
    plot_W_colors(colden=val,delete_80=True,high_z=False)
    i+=1


  
