import pandas as pd
import math
from preprocessing import kriteria_max,subkriteria_max,df3,datakriteria,mgr,max_iterasi
#tabel baru
def coba(a,b,c,d,e):
    kriteria_max=a
    subkriteria_max=b
    df3=c
    datakriteria=d
    mgr=e
    df3=df3.loc[df3[kriteria_max[0]]==subkriteria_max[0]]
    #mencari  rtsm,rtm,rthm total
    RTSM=(df3['KLASIFIKASI RTM']=='RTSM').sum()
    RTM=(df3['KLASIFIKASI RTM']=='RTM').sum()
    RTHM=(df3['KLASIFIKASI RTM']=='RTHM').sum()
    #data kriteria baru
    datakriteria.pop(mgr)
    ket=[]
    krit=[]
    for i,a in enumerate(datakriteria):
        for key, value in a.items():
            ket.append(key)
            krit.append(i)
    header=[]
    df3.drop(kriteria_max[0], axis=1, inplace=True)
    header.extend(df3.columns.values.tolist())
    jumlahKasus=[]
    rtsm_list=[]
    rtm_list=[]
    rthm_list=[]
    kritbaru=[]
    entropy=[]
    for a in krit:
        kritbaru.append(header[a])
    for i,a in enumerate(ket):
        for j,b in enumerate(kritbaru):
            if i==j:
                rtsm_v=len(df3[(df3['KLASIFIKASI RTM']=='RTSM') & (df3[b]==a)])
                rtm_v=len(df3[(df3['KLASIFIKASI RTM']=='RTM') & (df3[b]==a)])
                rthm_v=len(df3[(df3['KLASIFIKASI RTM']=='RTHM') & (df3[b]==a)])
                jk=len(df3[(df3[b]==a)])
                jumlahKasus.append(jk)
                rtsm_list.append(rtsm_v)
                rtm_list.append(rtm_v)
                rthm_list.append(rthm_v)
    #menambahkan baris total pada list
    kritbaru.insert(0,"TOTAL")
    ket.insert(0,"")
    jumlahKasus.insert(0,len(df3))
    rtsm_list.insert(0,RTSM)
    rtm_list.insert(0,RTM)
    rthm_list.insert(0,RTHM)
    #entropy
    #proses
    #entropy
    entropy=[]
    def entropy_fc(a,b,c,n):
        return entropy.append(-(a/n)*math.log2(a/n)-(b/n)*math.log2(b/n)-(c/n)*math.log2(c/n))
    for w in range(len(jumlahKasus)):
        for x in range(len(rtsm_list)):
            for y in range(len(rtm_list)):
                for z in range(len(rthm_list)):
                    if w==x==y==z:
                        if jumlahKasus[w]==0 or rtsm_list[x]==0 or rtm_list[y]==0 or rthm_list[z]==0:
                            entropy.append(0)
                            break
                        else:
                            entropy_fc(rtsm_list[x],rtm_list[y],rthm_list[z],jumlahKasus[w])
    entropy=[round(item,2) for item in entropy]
     #membuat tabel nodes            
    tabelnodes=pd.DataFrame({'keterangan':ket,'jumlah kasus':jumlahKasus,'RTSM':rtsm_list,'RTM':rtm_list,'RTHM':rthm_list,'entropy':entropy},index=kritbaru)
    gain_list=[]
    list_sum=[]
    #mencari gain
    def gain(a,b,c,d):
        list_sum.append((b/c*d))
        jml=sum(map(float,list_sum))
        return round(a-jml,2)
    splitinfo_list=[]
    list_sum_si=[]
    #mencari splitinfo
    def splitinfo(a,b):
        if a==0:
            list_sum_si.append(0) 
        else:
            list_sum_si.append((a/b)*math.log2(a/b))   
        jml=sum(map(float,list_sum_si))
        return round(-(jml),2)
    splitinfo_list=[]
    list_sum_si=[]
    krit_set=set(krit)
    iheader=list(krit_set)
    def gs(n):
        for i,f in enumerate(krit):
            if f == n:
                x=gain(entropy[0],jumlahKasus[i+1],jumlahKasus[0],entropy[i+1])
                y=splitinfo(jumlahKasus[i+1],jumlahKasus[0])
        return gain_list.append(x),splitinfo_list.append(y)
    for n in iheader:
        list_sum_si=[]
        list_sum=[]
        gs(n)
    #mencari gain ratio
    gainratio_list=[]
    def gain_ratio_fct(a,b):
        return gainratio_list.append(round(a/b,2))
    for i,a in enumerate(gain_list):
        for j,b in enumerate(splitinfo_list):
            if i==j:
                if b==0:
                    gainratio_list.append(0)
                else:
                    gain_ratio_fct(a,b)
    #tabel gain, si, gainratio
    #membuat tabel nodes            
    #membuat tabel nodes            
    tabelgs=pd.DataFrame({'kriteria':header[0:len(gain_list)],'gain':gain_list,'split info':splitinfo_list, 'gain ratio': gainratio_list})
    #menemukan kriteria dari gain ratio maksimal
    max_gainratio=tabelgs[['gain ratio']].idxmax()
    kriteria_max=tabelgs['kriteria'].iloc[max_gainratio]
    mgr=max_gainratio.tolist()[0]
    #menemukan baris dengan kolom dengan kriteria tertinggi
    tblbaris=tabelnodes.loc[kriteria_max]
    #menemukan entropy tertinggi dari kriteria dengan gain ratio tertinggi
    entropy_max=tblbaris['entropy'].max()
    #menemukan entropy tertinggi kedua dari kriteria dengan gain ratio tertinggi
    entropy_maxs=tblbaris['entropy'].nlargest(2).tolist()[1]
    #menemukan subkriteria dengan entropy tertinggi dari kriteria dengan gain ratio tertinggi
    subkriteria_tbl=tblbaris.loc[tblbaris['entropy']==entropy_max]
    subkriteria_max=subkriteria_tbl['keterangan']
    #menemukan subkriteria dengan entropy tertinggi kedua dari kriteria dengan gain ratio tertinggi
    subkriteria_tbls=tblbaris.loc[tblbaris['entropy']==entropy_maxs]
    subkriteria_maxs=subkriteria_tbls['keterangan']
    #menjadikan list kriteria max
    kriteria_max=kriteria_max.tolist()
    #menjadikan list sub kriteria max
    subkriteria_max=subkriteria_max.tolist()
    #menjadikan list sub kriteria max kedua
    subkriteria_maxs=subkriteria_maxs.tolist()
    #menyimpan tabelnodes ke excel
    # writer = pd.ExcelWriter('tabel nodes.xlsx', engine='xlsxwriter')
    # tabelnodes.to_excel(writer, sheet_name='data 1', index=False)
    # tabelgs.to_excel(writer, sheet_name='data 2', index=False)
    # writer.save()
    return kriteria_max,subkriteria_max,df3,datakriteria,mgr,entropy_max,tabelnodes,tabelgs,tblbaris
nodes_dic={}
gs_dic={}
tblbaris_dic={}
for val in range(1,max_iterasi):
    kriteria_max,subkriteria_max,df3,datakriteria,mgr,entropy_max,tabelnodes,tabelgs,tblbaris=coba(kriteria_max,subkriteria_max,df3,datakriteria,mgr)
    nodes_dic["iterasi {}".format(val)]=tabelnodes
    gs_dic["iterasi {}".format(val)]=tabelgs
    tblbaris_dic["iterasi {}".format(val)]=tblbaris
    if entropy_max==0:
        break
    else:
        kriteria_max=kriteria_max
        subkriteria_max=subkriteria_max
        df3=df3
        datakriteria=datakriteria
        mgr=mgr
        kriteria_max,subkriteria_max,df3,datakriteria,mgr,entropy_max,tabelnodes,tabelgs,tblbaris=coba(kriteria_max,subkriteria_max,df3,datakriteria,mgr)
        nodes_dic["iterasi {}".format(val+1)]=tabelnodes
        gs_dic["iterasi {}".format(val+1)]=tabelgs
        tblbaris_dic["iterasi {}".format(val)]=tblbaris
        
item_gs=gs_dic.items()
for k,v in item_gs:
    print('{0}\n{1}'.format(k,v))
item_nodes=nodes_dic.items()
for k,v in item_nodes:
    print('{0}\n{1}'.format(k,v))

