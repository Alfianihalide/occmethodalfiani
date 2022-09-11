from preprocessing import kriteria_max,tblbaris,tabelgs
import pandas as pd
subk=tblbaris.nlargest(len(tblbaris),'entropy')
print("coba",subk['entropy'].max())
def subkritria(x,y,z,a):
    entmax=x['entropy'].max()
    for index, row in x.iterrows():
        if row['entropy']==0:
            maks=[row['RTSM'],row['RTM'],row['RTHM']]
            mv=maks.index(max(maks))
            if mv==0:
                mb='RTSM'
            if mv==1:
                mb='RTM'
            else:
                mb='RTHM'
            data=print(index,"-->",row['keterangan'],"-->",mb)
        else:
            if row['entropy']>=entmax:
                for index1, row1 in y.iterrows():
                    maks=[row1['RTSM'],row1['RTM'],row1['RTHM']]
                    mv=maks.index(max(maks))
                    if mv==0:
                        mb1='RTSM'
                    if mv==1:
                        mb1='RTM'
                    else:
                        mb1='RTHM'
                    data1=print(index,"-->",row['keterangan'],"-->",index1,"-->",row1['keterangan'],"-->",mb1)
            else:
                entmax=z['entropy'].max()
                for index2, row2 in z.iterrows():
                    if row2['entropy']==0:
                        maks=[row2['RTSM'],row2['RTM'],row2['RTHM']]
                        mv=maks.index(max(maks))
                        if mv==0:
                            mb2='RTSM'
                        if mv==1:
                            mb2='RTM'
                        else:
                            mb2='RTHM'
                        data2=print(index,"-->",row['keterangan'],"-->",index2,"-->",row2['keterangan'],"-->",mb2)
                    else:
                        if row2['entropy']>=entmax:
                            for index3,row3 in a.iterrows():
                                if row3['entropy']==0:
                                    maks=[row3['RTSM'],row3['RTM'],row3['RTHM']]
                                    mv=maks.index(max(maks))
                                    if mv==0:
                                        mb3='RTSM'
                                    if mv==1:
                                        mb3='RTM'
                                    else:
                                        mb3='RTHM'
                                    data3=print(index,"-->",row['keterangan'],"-->",index2,"-->",row2['keterangan'],"-->",index3,"-->",row3['keterangan'],"-->",mb3)
            
    return data,data1,data2,data3


from node1 import tblbaris_dic
item_nodes=tblbaris_dic.items()
for k,v in item_nodes:
    tblbaris=v
subk1=tblbaris.nlargest(len(tblbaris),'entropy')
subk2=pd.read_excel('.\subk2.xlsx',index_col=0)
subk21 = pd.read_excel('.\subk21.xlsx',index_col=0)
subkritria(subk,subk1,subk2,subk21)
