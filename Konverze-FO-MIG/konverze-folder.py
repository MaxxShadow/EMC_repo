import numpy as np
import pandas as pd
import string
import sys
import os
import argparse

def get_files_in_directory(directory, file_type):
    files = [f for f in os.listdir(directory) if f.endswith(file_type)]
    file_names = [os.path.splitext(f)[0] for f in files]
    data = {'INEXCELNAME': files, 'OUTCSVNAME': file_names}
    df = pd.DataFrame(data)
    return df

# Příklad použití
directoryXLS = '.\\XLS'
file_type = '.xlsx'
ListExcel = get_files_in_directory(directoryXLS, file_type)

SheetName = 'ECZ'
for l in ListExcel.index:
    InFileXls = '.\\XLS\\' + ListExcel.at[l, 'INEXCELNAME']
    OutFileCsv = '.\\CSV\\' + ListExcel.at[l, 'OUTCSVNAME']+'.csv'
    #SheetName = ListExcel.at[l, 'SHEETNAME']
    tabulka = pd.read_excel(InFileXls
                    , sheet_name=SheetName
                    , na_values='#N/A'
                    , index_col=None
                    , dtype = str
                    #, converters={'MAINACCOUNTID':str}
                    #, usecols="A,H,K:M,S"
                    #, usecols="A"
                    #, usecols=None
                  )
    tabulka.to_csv(OutFileCsv, sep='|', encoding='utf-16le', na_rep='', index=False)
