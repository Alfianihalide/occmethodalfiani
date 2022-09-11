from operator import sub
import pandas as pd
import math
#membaca data
data50='.\datalatih\data50.csv'
data60='.\datalatih\data60.csv'
data70='.\datalatih\data70.csv'
data80='.\datalatih\data80.csv'
data90='.\datalatih\data90.csv'
data100='.\datalatih\data100.csv'
masukkan_data=input("Masukkan data: ")
datax=vars()[masukkan_data]
df = pd.read_csv(datax)
max_iterasi=int(input("Masukkan maksimal iterasi: "))
#mengelompokkan data numerik
#kriteria x1
df2=df.copy()
df2['PENDAPATAN KEPALA KELUARGA']=pd.cut(df['PENDAPATAN KEPALA KELUARGA'],
bins=[0,999999,2000000,100000000],
labels=['rendah','sedang','tinggi'])
#kriteria x3
df2['LUAS LAHAN TEMPAT TINGGAL (m2)']=pd.cut(df['LUAS LAHAN TEMPAT TINGGAL (m2)'],
bins=[14,150,286,422,558,694,830,966,1102,1238,1375],
labels=['k1','k2','k3','k4','k5','k6','k7','k8','k9','k10'])
#kriteria x4
df2['LUAS LANTAI (m2)']=pd.cut(df['LUAS LANTAI (m2)'],
bins=[5,99,193,287,381,475,569,663,757,851,945],
labels=['k1','k2','k3','k4','k5','k6','k7','k8','k9','k10'])
dfawal=df2.copy()
#transformasi data
datax1 = {'rendah':0,'sedang':0,'tinggi':1}
datax2 = {'milik orang lain':1, 'milik sendiri':0}
datax3 = {'k1':1,'k2':1,'k3':1,'k4':1,'k5':1,'k6':0,'k7':0,'k8':0,'k9':0,'k10':0}
datax4 = {'k1':1,'k2':1,'k3':1,'k4':1,'k5':1,'k6':0,'k7':0,'k8':0,'k9':0,'k10':0}
datax5 = {'kayu jerami':1, 'seng':1, 'genteng':0}
datax6 = {'kayu kualitas rendah':1,'kayu kualitas tinggi':1, 'beton':0}
datax7 = {'tanah':1, 'kayu':1, 'semen':1, 'tegel':0, 'keramik':0}
datax8 = {'SD': 1, 'SMP': 1, 'SMA':1, 'S1':0}
datax9 = {'tidak ada': 1, 'MCK umum':1, 'berkelompok bersama tetangga':1, 'sendiri':0}
datax10 = {'sungai': 1, 'jamban umum': 1, 'jamban bersama tetangga': 1, 'jamban sendiri':0}
datax11 = {'tidak ada':1, 'listrik non PLN':1, 'listrik PLN':0}
datax12 = {'air isi ulang':1, 'mata air':0}
datax13 = {'kayu bakar':1, 'minyak tanah':1, 'gas LPG':0}
datax14 = {'sawah':1, 'lubang ditanah':1,'instalasi pengelolaan limbah':0}
df3=df.copy()

datakriteria=[datax1,datax2,datax3,datax4,datax5,datax6,datax7,datax8,datax9,datax10,datax11,datax12,datax13,datax14]
df2.drop('KLASIFIKASI RTM', axis=1, inplace=True)
for i,a in enumerate(df2):
    for j,b in enumerate(datakriteria):
        if i==j:
            df2=df2.replace({a:b})

#klasifikasi Rumah tangga miskin
cat_columns=df2.select_dtypes(['category']).columns
df2[cat_columns] = df2[cat_columns].apply(lambda x: x.cat.codes)
#ganti data hasil codes
kode={0:1,1:0}
df2= df2.replace({"PENDAPATAN KEPALA KELUARGA":kode,"LUAS LAHAN TEMPAT TINGGAL (m2)":kode,"LUAS LANTAI (m2)":kode})
df2.to_excel('transformasi data.xlsx', engine='xlsxwriter')
df3=dfawal.copy()
bobot=[0.1,0.095,0.091,0.087,0.082,0.078,0.074,0.069,0.065,0.060,0.056,0.052,0.047,0.043]
c=0
for i,a in enumerate(df2):
    for j,b in enumerate(bobot):
        if i==j:
            c=c+df2[a]*b
            df3['KLASIFIKASI RTM']=round(c,2)
# df3.to_excel('output1.xlsx', engine='xlsxwriter') 
df3['KLASIFIKASI RTM']=pd.cut(df3['KLASIFIKASI RTM'],
bins=[0.00,0.59,0.79,1.00],
labels=['RTHM','RTM','RTSM'])
RTSM=(df3['KLASIFIKASI RTM']=='RTSM').sum()
RTM=(df3['KLASIFIKASI RTM']=='RTM').sum()
RTHM=(df3['KLASIFIKASI RTM']=='RTHM').sum()
#persiapan list untuk dimasukkan kedalam tabel nodes
ket=[]
krit=[]
for i,a in enumerate(datakriteria):
    for key, value in a.items():
        ket.append(key)
        krit.append(i)
header=[]
header.extend(df.columns.values.tolist())
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
df4=df3.copy()
writer = pd.ExcelWriter('data.xlsx', engine='xlsxwriter')
# tabelnodes.to_excel(writer, sheet_name='data 1', index=False)
df3.to_excel(writer, sheet_name='data', index=False)
writer.save()