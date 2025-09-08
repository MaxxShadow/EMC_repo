#
# Konverzní procedura, dávkově, seznam v List4conv.csv, v.1.1
#

import numpy as np
import pandas as pd
import string
import sys
import argparse

InListExcel = 'List4conv.csv'
ListExcel = pd.read_csv(InListExcel
                    , na_values='#N/A'
                    , index_col=None
                    , sep=';'
                    #, sheet_name=SheetName
                    #, usecols="A,H,K:M,S"
                    #, usecols="A"
                    #, usecols=None
                  )

for l in ListExcel.index:
    InFileXls = '.\\XLS\\' + ListExcel.at[l, 'INEXCELNAME']
    OutFileCsv = '.\\CSV\\' + ListExcel.at[l, 'OUTCSVNAME']+'.csv'
    SheetName = ListExcel.at[l, 'SHEETNAME']
    tabulka = pd.read_excel(InFileXls
                    , sheet_name=SheetName
                    , na_values='#N/A'
                    , index_col=None
                    , dtype = str
                    #, usecols="A,H,K:M,S"
                    #, usecols="A"
                    #, usecols=None
                  )
    tabulka.to_csv(OutFileCsv, sep='|', encoding='utf-16le', na_rep='', index=False)
