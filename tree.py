from doctest import master
from turtle import pd
from unicodedata import category
from preprocessing import df4,masukkan_data
#import library
from sklearn.tree import DecisionTreeClassifier
import matplotlib.pyplot as plt
from operator import sub
import pandas as pd
import math
from sklearn import tree,metrics
import graphviz
import numpy as np
import pydotplus

from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
#membaca data
data50='.\datauji\datauji50.csv'
data40='.\datauji\datauji40.csv'
data30='.\datauji\datauji30.csv'
data20='.\datauji\datauji20.csv'
data10='.\datauji\datauji10.csv'
if masukkan_data=="data50":
    sized=0.5
    bat=150
    masukkan_data_uji="data50"
elif masukkan_data=="data60":
    sized=0.4
    bat=180
    masukkan_data_uji="data40"
elif masukkan_data=="data70":
    sized=0.3
    bat=210
    masukkan_data_uji="data30"
elif masukkan_data=="data80":
    sized=0.2
    bat=240
    masukkan_data_uji="data20"
elif masukkan_data=="data90":
    sized=0.1
    bat=270
    masukkan_data_uji="data10"
datay=vars()[masukkan_data_uji]
df = pd.read_csv(datay)
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
df2.to_excel('output6.xlsx', engine='xlsxwriter') 
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

le=LabelEncoder()
dataset=pd.concat([df4,df3])
writer = pd.ExcelWriter('df4.xlsx', engine='xlsxwriter')
df4.to_excel(writer, sheet_name='data 1', index=False)
writer.save()

for column in dataset:
    if dataset[column].dtypes == object:
        dataset[column] = le.fit_transform(dataset[column])
cat_columns=dataset.select_dtypes(['category']).columns
dataset[cat_columns] = dataset[cat_columns].apply(lambda x: x.cat.codes)
writer = pd.ExcelWriter('dataset.xlsx', engine='xlsxwriter')
dataset.to_excel(writer, sheet_name='data 1', index=False)
writer.save()
x_train=dataset.iloc[0:bat,:-1].values
x_test=dataset.iloc[bat:300,:-1].values
y_train=dataset.iloc[0:bat,-1].values
y_test=dataset.iloc[bat:300,-1].values
# x=dataset.iloc[:,:-1].values
# y=dataset.iloc[:,-1].values

# x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=sized,random_state=0)

model = DecisionTreeClassifier(ccp_alpha=0.0, class_weight=None, criterion='entropy',
                       max_depth=4, max_features=None, max_leaf_nodes=None,
                       min_impurity_decrease=0.0,
                       min_samples_leaf=1, min_samples_split=2,
                       min_weight_fraction_leaf=0.0,
                       random_state=1, splitter='best')
header=[]
header.extend(dataset.columns)
x_columns=header[0:-1]
y_columns=['RTSM','RTM','RTHM']
model=model.fit(x_train,y_train)
fig=plt.figure(figsize=(10,5))
tree.plot_tree(model,feature_names=x_columns,class_names=y_columns)
fig.show
figi = plt.figure(figsize=(15,10))
dot_data = tree.export_graphviz(model, out_file=None,feature_names=x_columns,class_names=y_columns,filled = True)
graph = graphviz.Source(dot_data)
graph.view()
hasilprediksi =  model.predict(x_test)
# Menghitung Akurasi
prediksiBenar = (hasilprediksi == y_test).sum()
prediksiSalah = (hasilprediksi != y_test).sum()
print("Prediksi Benar :", prediksiBenar, "data")
print("Prediksi Salah  :", prediksiSalah, "data")
Akurasi=prediksiBenar/(prediksiBenar+prediksiSalah) * 100
print("Akurasi :", Akurasi, "%")
print("Error :",100-Akurasi, "%")
actual=y_test
predicted=hasilprediksi
print(metrics.confusion_matrix(actual,  predicted))
print(metrics.classification_report(actual,predicted, digits=3))