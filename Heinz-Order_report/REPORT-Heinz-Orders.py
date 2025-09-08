import sys
import string

try:
    import collections.abc as collections_abc # only works on python 3.3+
except ImportError:
    import collections as collections_abc

from os import getenv
import pymssql as pms
import pandas as pd
import numpy as np

from zipfile import ZipFile, ZIP_DEFLATED
#  Při použití knihovny zipfile v Pythonu můžete ovlivnit míru komprimace nastavením parametru compression při vytváření instance ZipFile. 
# Tento parametr určuje, jaký algoritmus komprese se použije. 
# Knihovna zipfile podporuje několik různých algoritmů komprese, 
#     včetně ZIP_STORED (bez komprese), 
#     ZIP_DEFLATED (standardní algoritmus DEFLATE) 
#     a dalších.
def zip_file(file_path, zip_path):
    with ZipFile(zip_path, 'w', compression=ZIP_DEFLATED) as myzip:
        myzip.write(file_path)
        
import _Query4data as QD
import base64

decoded_string = base64.b64decode(QD.cCONN).decode('utf-8')
print('Decoded ...')
decoded_list = decoded_string.split('|')

host=decoded_list[0]
user=decoded_list[1]
password=decoded_list[2]

db_query1= decoded_list[3]
query1 = QD.qOrders

print('Start generator, please wait ...')

conn = pms.connect(
    host,
    user,
    password,
    database=db_query1
)

cursor = conn.cursor()
cursor.execute(query1)
i = 0
for row in cursor:
    #print('row = %r' % (row,))
    #print(row[0], ' ', row[1])
    i += 1
    if i==1 :
        d1 = pd.DataFrame([row])
        result = d1
    else:
        d1 = pd.DataFrame([row])
        #result = result.append(d1, ignore_index=True, sort=False) #PY 3.10+ >> deprec version
        result = pd.concat([result, d1]) #new version
    
print(' --- ')
print('Pocet recs = %r' %i)

conn.close()

result.columns = QD.cnameOrders

#result ROWS
OutputResult = result.sort_values("Document-No_")
OutputResult["Sell-Cust-Name"] = OutputResult["Sell-Cust-Name"].apply(lambda x: x.translate(str.maketrans('øČÈěščřžýáíé', 'stsrzCCescrzyaie', string.punctuation)))
OutputResult["Bill-Cust-Name"] = OutputResult["Bill-Cust-Name"].apply(lambda x: x.translate(str.maketrans('øČÈěščřžýáíé', 'stsrzCCescrzyaie', string.punctuation)))

EntityName = 'Report-ROWS'
ListName = 'Heinz-Orders'
OutFileCsv = '.\\' + EntityName + '-'  + ListName +'.csv'
OutFileZip = '.\\' + EntityName + '-'  + ListName +'.zip'
OutputResult.to_csv(OutFileCsv, sep='|', encoding='utf-8', index=False)
# volání komprimace
zip_file(OutFileCsv, OutFileZip)
print(' --- ')
print('Výstupní soubor řádků => %r' %OutFileCsv)

#result LIST ORDERS
ListOrdersVersion = OutputResult.groupby("Document-No_").agg({"Version-No_": 'max'}).reset_index()

EntityName = 'Report-LIST'
ListName = 'Heinz-Orders'
OutFileCsv = '.\\' + EntityName + '-'  + ListName +'.csv'
OutFileZip = '.\\' + EntityName + '-'  + ListName +'.zip'
ListOrdersVersion.to_csv(OutFileCsv, sep='|', encoding='utf-8', index=False)
# volání komprimace
zip_file(OutFileCsv, OutFileZip)
print(' --- ')
print('Výstupní soubor objednávek => %r' %OutFileCsv)
print(' --- ')
print('--------------- End generator ---------------------------------------------')
