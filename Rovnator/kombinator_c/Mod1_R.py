
import pandas as pd

# ----------------- Funkce R ----------------------------
# kombinatorická funkce pro vyrovnání stavu FO proti stavu ESA
#
def R(ES, FS):
     A = "A"
     L = "L"
     S = "S"
     Q = "Q"
     ES.columns = ["ID_Row", A, L, S, Q]
     FS.columns = ["ID_Row", A, L, S, Q]

     ES = ES.copy(); FS = FS.copy()
     ES["QX"] = 0 ; ES["QZ"] = 0 ; ES["SX"] = ""
     FS["QX"] = 0 ; FS["QZ"] = 0 ; FS["SX"] = ""

     OUT = pd.DataFrame(columns=["A", "LF", "SF", "LE", "SE", "Q"])  # Výstupní dataframe
     OUT = OUT.iloc[0:0]

     # Step 1 - FS equals ES
     for _, fs_row in FS.iterrows():
          match = pd.DataFrame
          match = ES[(ES["A"] == fs_row["A"]) & (ES["L"] == fs_row["L"]) & (ES["S"] == fs_row["S"])].copy()
          #print("FS ROW ...\n",pd.DataFrame([fs_row]))
          if not match.empty:
               es_row = match.iloc[0]
               #print("MATCH ROWS ...\n",match)
               #print("ES ROWS ...\n",pd.DataFrame([es_row]))
               #print(f"----------------------")
               if fs_row["Q"] <= es_row["Q"]:
                    OUT = pd.concat([OUT, pd.DataFrame([{ "A": fs_row["A"], "LF": fs_row["L"], "SF": fs_row["S"], "Q": fs_row["Q"] }])], ignore_index=True)
                    #print("OUT ...\n",OUT)
                    #print(f"----------------------")
                    FS.at[fs_row.name, "QX"] = fs_row["Q"]
                    FS.at[fs_row.name, "SX"] = "OK"
                    ES.at[es_row.name, "QX"] = fs_row["Q"]
                    ES.at[es_row.name, "QZ"] = es_row["Q"] - fs_row["Q"]
                    ES.at[es_row.name, "SX"] = "OK" if fs_row["Q"] == es_row["Q"] else "X"
                    #
               else:
                    OUT = pd.concat([OUT, pd.DataFrame([{ "A": es_row["A"], "LE": es_row["L"], "SE": es_row["S"], "Q": es_row["Q"] }])], ignore_index=True)
                    #print("OUT ...\n",OUT)
                    #print(f"----------------------")
                    FS.at[fs_row.name, "QX"] = es_row["Q"]
                    FS.at[fs_row.name, "QZ"] = fs_row["Q"] - es_row["Q"]
                    FS.at[fs_row.name, "SX"] = "X"
                    ES.at[es_row.name, "QX"] = es_row["Q"]
                    ES.at[es_row.name, "SX"] = "OK"
                    #
          else:
               pass
               #print("MATCH ROWS ...empty")
               #print(f"----------------------")  
     FS["QZ"] = FS["Q"] - FS["QX"]
     ES["QZ"] = ES["Q"] - ES["QX"]

     # Step 2 - FS not equals ES
     for _, fs_row in FS.iterrows():
          #print("FS ROWS ...\n", pd.DataFrame([fs_row]))
          #print(f"----------------------")
          if fs_row["SX"] != "OK":
               match2 = ES[(ES[A] == fs_row[A]) & (ES["SX"] != "OK")].copy()
               #print("MATCH2 ROWS ...\n", match2)
               #print(f"----------------------")
               if not match2.empty:
                    for _, es_row in match2.iterrows():
                         if fs_row["QZ"] > 0:
                              if es_row["QZ"] <= fs_row["QZ"]:
                                   OUT = pd.concat([OUT, pd.DataFrame([{ "A": fs_row["A"], 
                                                                           "LF": fs_row["L"], 
                                                                           "SF": fs_row["S"], 
                                                                           "LE": es_row["L"], 
                                                                           "SE": es_row["S"], 
                                                                           "Q": es_row["QZ"] }])], ignore_index=True)
                                   #print("OUT ...\n",OUT)
                                   #print(f"----------------------")
                                   FS.at[fs_row.name,"QZ"] -= es_row["QZ"]
                                   fs_row["QZ"] -= es_row["QZ"]
                                   FS.at[fs_row.name,"QX"] += es_row["QZ"]
                                   fs_row["QX"] += es_row["QZ"]
                                   FS.at[fs_row.name,"SX"] = "OK" if fs_row["QZ"] == 0 else "X"
                                   ES.at[es_row.name, "QX"] += es_row["QZ"]
                                   ES.at[es_row.name, "QZ"] = 0
                                   ES.at[es_row.name, "SX"] = "OK"
                              else:
                                   OUT = pd.concat([OUT, pd.DataFrame([{ "A": fs_row["A"], 
                                                                           "LF": fs_row["L"], 
                                                                           "SF": fs_row["S"], 
                                                                           "LE": es_row["L"], 
                                                                           "SE": es_row["S"], 
                                                                           "Q": fs_row["QZ"] }])], ignore_index=True)
                                   #print("OUT ...\n",OUT)
                                   #print(f"----------------------")
                                   FS.at[fs_row.name,"QX"] += fs_row["QZ"]
                                   ES.at[es_row.name, "QX"] += fs_row["QZ"]
                                   ES.at[es_row.name, "QZ"] -= fs_row["QZ"]
                                   ES.at[es_row.name, "SX"] = "X"
                                   FS.at[fs_row.name,"QZ"] = 0
                                   fs_row["QZ"] = 0
                                   FS.at[fs_row.name,"SX"] = "OK"
          else:
               pass
               #print("no MATCH2")
               #print(f"----------------------")
     return OUT, FS, ES




# Hlavní spuštění aplikace
def main():
    # Aplikace
    pass

if __name__ == '__main__':
     print("Module 1_R is being run directly")

