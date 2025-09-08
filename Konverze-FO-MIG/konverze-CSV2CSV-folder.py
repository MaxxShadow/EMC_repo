import numpy as np
import pandas as pd
import string
import sys
import os
import argparse

def get_files_in_directory(directory, file_type):
    files = [f for f in os.listdir(directory) if f.endswith(file_type)]
    file_names = [os.path.splitext(f)[0] for f in files]
    data = {'INFILENAME': files, 'OUTFILENAME': file_names}
    df = pd.DataFrame(data)
    return df

directoryCSVin = '.\\CSV'
file_type = '.csv'
ListCSVFiles = get_files_in_directory(directoryCSVin, file_type)

for l in ListCSVFiles.index:
    InFileCsv = '.\\CSV\\' + ListCSVFiles.at[l, 'INFILENAME']
    OutFileCsv = '.\\2CSV\\' + ListCSVFiles.at[l, 'OUTFILENAME']+'.csv'
    column_name1 = 'BARCODE',
    column_name2 = 'ITEMNUMBER'
    colstype = {column_name1: str,
                column_name2: str}
    tabulka = pd.read_csv(InFileCsv
                    #, sheet_name=SheetName
                    #, na_values='#N/A'
                    #, index_col=None
                    #, usecols="A,H,K:M,S"
                    #, usecols="A"
                    #, usecols=None
                    , sep='|'
                    , encoding_errors='ignore'
                    , dtype=str
                    #, dtype=colstype
                    #
                    # -------nastavení kódování na vstupu - VŽDY PRÁVĚ JEN JENDO -------
                    #, encoding='utf-16le'
                    , encoding='ansi'
                    #, encoding='ascii'
                    #, encoding='utf-8'
                    #, encoding='latin1'
                    #, encoding='iso-8859-1'
                    #, encoding='cp1252'
                  )
    tabulka.to_csv(OutFileCsv, sep='|', encoding='utf-16le', index=False)
