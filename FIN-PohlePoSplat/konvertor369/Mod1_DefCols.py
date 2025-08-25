#
# Konstanty, seznamy a proměnné pro definici sloupců
#

#
OrigCSVcols = [
     'textbox12', 'textbox83', 'Textbox3', 'textbox142', 'textbox133',
       'CustGroup', 'Textbox18', 'Textbox24', 'Textbox28', 'Textbox36',
       'Textbox39', 'Textbox41', 'Textbox34', 'Textbox96', 'textbox195',
       'textbox194', 'textbox193', 'textbox192', 'textbox191', 'textbox177',
       'Textbox1563', 'textbox196', 'Textbox19', 'Textbox20', 'textbox230',
       'textbox231', 'textbox201', 'textbox200', 'textbox199', 'textbox198',
       'Textbox46', 'TransDate', 'Voucher', 'Balance01', 'Balance022',
       'Balance031', 'Balance041', 'Balance051', 'Balance061', 'Balance071',
       'Textbox48', 'Currency3', 'Balance01Cur2', 'Balance02Cur2',
       'Balance03Cur2', 'Balance04Cur2', 'Balance05Cur2', 'Balance06Cur2',
       'Balance07Cur2', 'Textbox50', 'Currency1', 'textbox260', 'textbox261',
       'textbox262', 'textbox263', 'textbox264', 'textbox265', 'textbox266',
       'Textbox43', 'textbox232', 'textbox238', 'textbox237', 'textbox236',
       'textbox235', 'textbox234', 'textbox233', 'textbox239', 'textbox240',
       'textbox241', 'textbox242', 'textbox243', 'textbox244', 'textbox245',
       'textbox246', 'textbox247', 'textbox253', 'textbox252', 'textbox251',
       'textbox250', 'textbox249', 'textbox248', 'textbox116', 'textbox254',
       'textbox255', 'textbox256', 'textbox257', 'textbox258', 'textbox259']
#
RenameV2Ccols = {
     'VendGroup':'CustGroup', 
     'Textbox45':'Textbox46', 
     'Textbox46':'Textbox48', 
     'CurrencyCode':'Currency3',
     'Textbox442':'Textbox50', 
     'CurrencyCode1':'Currency1', 
     'textbox124':'Textbox43'
}
#
SelCSVcols = [
     # 'textbox12', 
     # 'textbox83', 
     # 'Textbox3', 
     'textbox142', 
     'textbox133',
     'CustGroup', 
     #'Textbox18', 
     #'Textbox24', 
     #'Textbox28', 
     #'Textbox36',
     #'Textbox39', 
     #'Textbox41', 
     #'Textbox34', 
     #'Textbox96', 
     #'textbox195', 'textbox194', 'textbox193', 'textbox192', 'textbox191', 
     #'textbox177', 'Textbox1563', 'textbox196', 'Textbox19', 'Textbox20', 'textbox230', 'textbox231', 'textbox201', 'textbox200', 'textbox199', 'textbox198',
     #'Textbox46', 
     'TransDate', 'Voucher',
     'Balance01', 'Balance022', 'Balance031', 'Balance041', 'Balance051', 'Balance061', 'Balance071', # Hodnoty pohledávek
     'Textbox48', 
     'Currency3', 'Balance01Cur2', 'Balance02Cur2',
     'Balance03Cur2', 'Balance04Cur2', 'Balance05Cur2', 'Balance06Cur2',
     'Balance07Cur2', 
     #'Textbox50', 
     #'Currency1' 
     #'textbox260', 'textbox261', 'textbox262', 'textbox263', 'textbox264', 'textbox265', 'textbox266',
     #'Textbox43', 'textbox232', 'textbox238', 'textbox237', 'textbox236', 'textbox235', 'textbox234', 'textbox233', 'textbox239', 'textbox240', 'textbox241', 'textbox242', 'textbox243', 'textbox244', 'textbox245',
     #'textbox246', 'textbox247', 'textbox253', 'textbox252', 'textbox251', 'textbox250', 'textbox249', 'textbox248'
     #, 'textbox116', 'textbox254', 'textbox255', 'textbox256', 'textbox257', 'textbox258', 'textbox259'
]

#
SelOUTcols = [
     'Cust_ID', 
     'Cust_Name', 
     'Cust_Group',
     'Voucher', 
     'DATE_Due', 
     'DAYS_Due',
     'MONTH_Due',
     'Currency',
     'AMT_Remain', 
     'AMT_Aktual', 
     'AMT_1-30', 
     'AMT_31-60', 
     'AMT_61-90',
     'AMT_91-179', 
     'AMT_previous', 
     'AMTC_Remain',
     'AMTC_Aktual', 
     'AMTC_1-30', 
     'AMTC_31-60', 
     'AMTC_61-90', 
     'AMTC_91-179',
     'AMTC_previous']

clean_cols = [
               'AMT_Remain', 
               'AMT_Aktual', 
               'AMT_1-30', 
               'AMT_31-60', 
               'AMT_61-90',
               'AMT_91-179', 
               'AMT_previous',
               'AMTC_Remain',
               'AMTC_Aktual', 
               'AMTC_1-30', 
               'AMTC_31-60', 
               'AMTC_61-90', 
               'AMTC_91-179', 
               'AMTC_previous'
               ]

convert_cols = {
               'AMT_Remain':'float64', 
               'AMT_Aktual':'float64', 
               'AMT_1-30':'float64', 
               'AMT_31-60':'float64', 
               'AMT_61-90':'float64',
               'AMT_91-179':'float64', 
               'AMT_previous':'float64',
               'AMTC_Remain':'float64',
               'AMTC_Aktual':'float64', 
               'AMTC_1-30':'float64', 
               'AMTC_31-60':'float64', 
               'AMTC_61-90':'float64', 
               'AMTC_91-179':'float64', 
               'AMTC_previous':'float64',
               'DAYS_Due':'float64'
               }

RenameOUTcols_C = {
     'Cust_ID':'Zákazník_ID', 
     'Cust_Name':'Zákazník_Název', 
     'Cust_Group':'Zákazník_Skupina',
     'Voucher':'Faktura', 
     'DATE_Due':'Splatnost', 
     'DAYS_Due':'Dny_po_splatnosti',
     'MONTH_Due':'Měsíce_po_splatnosti',
     'Currency':'Měna',
     'AMT_Remain':'Zůstatek', 
     'AMT_Aktual':'AMT_Aktual', 
     'AMT_1-30':'AMT_1-30', 
     'AMT_31-60':'AMT_31-60', 
     'AMT_61-90':'AMT_61-90',
     'AMT_91-179':'AMT_91-179', 
     'AMT_previous':'AMT_previous', 
     'AMTC_Remain':'Zůstatek_Měna',
     'AMTC_Aktual':'AMTC_Aktual', 
     'AMTC_1-30':'AMTC_1-30', 
     'AMTC_31-60':'AMTC_31-60', 
     'AMTC_61-90':'AMTC_61-90', 
     'AMTC_91-179':'AMTC_91-179',
     'AMTC_previous':'AMTC_previous'
}
#

RenameOUTcols_V = {
     'Cust_ID':'Dodavatel_ID', 
     'Cust_Name':'Dodavatel_Název', 
     'Cust_Group':'Dodavatel_Skupina',
     'Voucher':'Faktura', 
     'DATE_Due':'Splatnost', 
     'DAYS_Due':'Dny_po_splatnosti',
     'MONTH_Due':'Měsíce_po_splatnosti',
     'Currency':'Měna',
     'AMT_Remain':'Zůstatek', 
     'AMT_Aktual':'AMT_Aktual', 
     'AMT_1-30':'AMT_1-30', 
     'AMT_31-60':'AMT_31-60', 
     'AMT_61-90':'AMT_61-90',
     'AMT_91-179':'AMT_91-179', 
     'AMT_previous':'AMT_previous', 
     'AMTC_Remain':'Zůstatek_Měna',
     'AMTC_Aktual':'AMTC_Aktual', 
     'AMTC_1-30':'AMTC_1-30', 
     'AMTC_31-60':'AMTC_31-60', 
     'AMTC_61-90':'AMTC_61-90', 
     'AMTC_91-179':'AMTC_91-179',
     'AMTC_previous':'AMTC_previous'
}
#