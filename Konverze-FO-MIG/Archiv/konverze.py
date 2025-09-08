#
# Konverzní procedura, jednotlivé soubory, parametry v args, v.1.3
#

import numpy as np
import pandas as pd
import string
import sys
import argparse

parser = argparse.ArgumentParser(description="""
                                             Konverzní skript pro transformaci XLS do CSV souboru.
                                             """)
parser.add_argument("-x", "--FileXls", help="Vstupní soubor XLS, např. 'InFile.xlsx'")
parser.add_argument("-c", "--FileCsv", help="Výstupní soubor CSV, např. 'OutFile.csv'")
parser.add_argument("-l", "--ListTab", help="List dat, např. 'List1'")

args = parser.parse_args()

if args.FileXls is None or args.FileCsv is None or args.ListTab is None:
    parser.print_help()
    InFileXls = 'Sešit1.xlsx'
    OutFileCsv = 'sesit1.csv'
    SheetName = 'List1'
else:
    InFileXls = args.FileXls
    OutFileCsv = args.FileCsv
    SheetName = args.ListTab

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
