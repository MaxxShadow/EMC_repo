# Kombinátor - verze 3.0.3
# Autor: Marcel Breda
#
# Kombajn pro kombinaci položek skladu, k vyrovnání stavu FO proti stavu ESA, podklad pro deník záměn
#

import pandas as pd
from sys import argv
from Mod1_R import R


# ----------------- MAIN ----------------------------
# Hlavní spuštění aplikace
def main():
    # Main funf
     TxtIN = "Data-Vstup_podklad01.xlsx"
     TxtOUT = "Data-Podklad_output01.xlsx"
     if len(argv) > 1:
          if "-h" in argv:
               hlp(TxtIN, TxtOUT)
               exit()
          print(f"KOMBINATOR - 3.0.3 --------------------")
          print(f"Vstupní soubor: {argv[1]}")
          print(f"Výstupní soubor: {argv[2]}")
          print(f"----------------------")
          filename_XLSinput = argv[1]
          filename_XLS_OutData = argv[2]
     else:
          filename_XLSinput = TxtIN
          filename_XLS_OutData = TxtOUT
          print(f"KOMBINATOR - 3.0.3 --------------------")
          print(f"Vstupní soubor: {filename_XLSinput}")
          print(f"Výstupní soubor: {filename_XLS_OutData}")
          

     sheetname_ESA = "ESA"
     sheetname_FO = "FO"
     sheetname_Data = "Data"

     # struktura dat df : [ID_Row, ID_Art, ID_Lot, ID_State, Amt]
     A = "ID_Art"
     L = "ID_Lot"
     S = "ID_State"
     Q = "Amt"

     df_e = pd.read_excel(filename_XLSinput, sheet_name=sheetname_ESA)
     df_f = pd.read_excel(filename_XLSinput, sheet_name=sheetname_FO)

     unique_values = pd.concat([df_e[A], df_f[A]]).unique()
     L = pd.DataFrame({"AL": unique_values})
     L["S"] = L["AL"].apply(lambda x: "IP" if x in df_e[A].values and x not in df_f[A].values else 
                                   "IM" if x in df_f[A].values and x not in df_e[A].values else "X")
     L["QE"] = L["AL"].apply(lambda x: df_e.loc[df_e[A] == x, Q].sum())
     L["QF"] = L["AL"].apply(lambda x: df_f.loc[df_f[A] == x, Q].sum())
     L = L.sort_values(by="AL").reset_index(drop=True)

     # Inicializace 
     OL = pd.DataFrame()
     O = pd.DataFrame()
     EO = pd.DataFrame()
     FO = pd.DataFrame()
     EL = pd.DataFrame()
     FL = pd.DataFrame()

     # Iterace mimo IP a IM
     for _, row in L[L["S"] == "X"].iterrows():
          AL_value = row["AL"]
          ES = df_e[df_e[A] == AL_value]
          FS = df_f[df_f[A] == AL_value]
          #
          print(f"Hodnota AL: {AL_value}")
          #print(ES)
          #print(FS)
          print(f"----------------------")
          #
          O = O.iloc[0:0]
          EO = EO.iloc[0:0]
          FO = FO.iloc[0:0]
          O,FO,EO = R(ES, FS)
          #print(f"----------------------")
          # Přidání výsledku do OL
          OL = pd.concat([OL, O], ignore_index=True)
          FL = pd.concat([FL, FO], ignore_index=True)
          EL = pd.concat([EL, EO], ignore_index=True)
          
     # Kontrolní Výstup
     # print(OL)

     # Výstup dat
     print(f"----------------------")
     print(f"Export ...")
     with pd.ExcelWriter(filename_XLS_OutData) as writer:
          df_f.to_excel(writer, sheet_name="FO_podklad", index=False)
          df_e.to_excel(writer, sheet_name="ESA_podklad", index=False)
          L.to_excel(writer, sheet_name="List_ART", index=False)
          FL.to_excel(writer, sheet_name="FO_L", index=False)
          EL.to_excel(writer, sheet_name="ESA_L", index=False)
          OL.to_excel(writer, sheet_name="OUT_List", index=False)

     print(f"----------------------")
     print("Hotovo - konec")
     pass

def hlp(
          txtIN="Data-Vstup_podklad01.xlsx", 
          txtOUT="Data-Podklad_output01.xlsx"):
     print(f"KOMBINATOR - 3.0.3 ")
     print(f"Autor: Marcel Breda")
     print(f"----------------------")
     print(f"Desc:")
     print(f"Kombajn pro kombinaci položek skladu, k vyrovnání stavu FO proti stavu ESA, podklad pro deník záměn")
     print(f"----------------------")
     print(f"Parms:")
     print(f"KOMBINATOR <filename_XLSinput> <filename_XLS_OutData>")
     print(f"----------------------")
     print(f"Def values:")
     print(f"Vstupní soubor: {txtIN}")
     print(f"Výstupní soubor: {txtOUT}")
     print(f"----------------------EOF")

# Spuštění hlavní funkce
if __name__ == "__main__":
     main()        
else:
     print(f"KOMBINATOR - 3.0.3 --------------------")
     print(f"... Loaded ... \n")