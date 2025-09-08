import os
import pandas as pd
import string
import sys
import argparse

parser = argparse.ArgumentParser(description="""STAV SKLADU ESA
                                                Konverzní skript pro transformaci XLS do CSV souboru.
                                                """)
parser.add_argument("-x", "--FileXls", help="Vstupní soubor XLS, např. '.\XLS\Stav skladu.xlsx'")
parser.add_argument("-c", "--FileCsv", help="Výstupní soubor CSV, např. '.\CSV\stav-skladu.csv'")

args = parser.parse_args()

if args.FileXls is None or args.FileCsv is None:
    parser.print_help()
    InFileXls = '.\Stavskladu.xlsx'
    OutFileCsv = '.\stavskladu.csv'
else:
    InFileXls = args.FileXls
    OutFileCsv = args.FileCsv

tabulka = pd.read_excel(InFileXls
                    , sheet_name='Stav skladu'
                    , na_values='#N/A'
                    , index_col=None
                    #, usecols="A,H,K:M,S"
                    #, usecols="A"
                    #, usecols=None
                  )
tabulka = tabulka.rename(columns=str.lower)

#tabulka.columns
cols = tabulka.columns.tolist()
tabulka = tabulka.rename(columns={
                         'pozice':'WarehousePosition',
                         "disponibilní množství v zmj":"Quantity",
                         "zmj":"UnitOfMeasure",
                         #"datum příjmu":"RD",
                         #"datum expirace":"ED",
                         "šarže":"LotNo",
                         "kód produktu":"No"
                         })


tabulka['oblast'] = tabulka['oblast'].apply(lambda x: x.translate(str.maketrans('ěščřžýáíé', 'escrzyaie', string.punctuation)))
tabulka['ED2dt'] = pd.to_datetime(tabulka['datum expirace'])
tabulka['ED'] = tabulka['ED2dt'].dt.strftime('%d.%m.%Y')
tabulka['RD2dt'] = pd.to_datetime(tabulka['datum příjmu'])
tabulka['RD'] = tabulka['RD2dt'].dt.strftime('%d.%m.%Y')


tab2 = tabulka[['oblast', 'WarehousePosition', 'No', 'Quantity', 'UnitOfMeasure', 'ED', 'RD', 'LotNo']]
tab2.sort_values(by="No").to_csv(OutFileCsv
          , sep='\t'
          , na_rep=''
          , index=False
          , index_label=False
          , header=False
          #, index_label=None
          , encoding='cp1250'
          , decimal=','
          )

