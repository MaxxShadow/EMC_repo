import sys
import pandas as pd 

import Mod1_DefCols as DefCols

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QCheckBox, 
                             QPushButton, QMessageBox, QFileDialog, QLabel, QDialog)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

#InFileCSV = "PohlPoSpl_Data.csv"
#OutFileXLSX = "PohlPoSpl_Data.xlsx"
#OutFileCSV = "PohlPoSpl_DataMod.csv"

# Funkce konverze
def f_konv(DataInOrig):
    # Selekce columns
    DataInV1 = DataInOrig[DefCols.SelCSVcols]
    DataInV1 = DataInV1.rename(columns={
        'textbox142': 'Cust_ID',
        'textbox133': 'Cust_Name',
        'CustGroup': 'Cust_Group',
        'Balance01':'AMT_Remain', 
        'Balance022':'AMT_Aktual', 
        'Balance031':'AMT_1-30', 
        'Balance041':'AMT_31-60', 
        'Balance051':'AMT_61-90', 
        'Balance061':'AMT_91-179', 
        'Balance071':'AMT_previous',
        'Textbox48':'DAYS_Due',
        'TransDate':'DATE_Due',
        'Currency3': 'Currency',
        'Balance01Cur2':'AMTC_Remain', 
        'Balance02Cur2':'AMTC_Aktual', 
        'Balance03Cur2':'AMTC_1-30', 
        'Balance04Cur2':'AMTC_31-60', 
        'Balance05Cur2':'AMTC_61-90', 
        'Balance06Cur2':'AMTC_91-179', 
        'Balance07Cur2':'AMTC_previous'
    })    
    #
    DataInV1[DefCols.clean_cols] = DataInV1[DefCols.clean_cols].astype(str)
    DataInV1[DefCols.clean_cols] = DataInV1[DefCols.clean_cols].apply(lambda col: col.str.replace(' ', '', regex=False))
    DataInV1[DefCols.clean_cols] = DataInV1[DefCols.clean_cols].apply(lambda col: col.str.replace(' ', '', regex=False))
    #
    DataInV1 = DataInV1.astype(
               DefCols.convert_cols, 
               errors='ignore'
          )
    #
    DataInV1['MONTH_Due'] = (DataInV1['DAYS_Due']/365)*12
    #
    DataOUT = DataInV1[DefCols.SelOUTcols]    
    return DataOUT


class StatusDialog(QDialog):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("Stavová informace ...")
        self.setModal(True)  # Zastaví hlavní okno, dokud se dialog neuzavře

        layout = QVBoxLayout()
        self.label = QLabel(message)
        layout.addWidget(self.label)

        continue_button = QPushButton("Pokračuj")
        continue_button.clicked.connect(self.accept)  # Zavře dialog po stisknutí tlačítka
        layout.addWidget(continue_button)

        self.setLayout(layout)

    def update_message(self, message):
        self.label.setText(message)
        self.repaint()  # Aktualizuje zobrazení textu

class InputWindow(QWidget):
    def __init__(self):
        super().__init__()

        # Nastavení počátečních rozměrů
        # self.resize(500, 300)  # Šířka x Výška
        self.setGeometry(150, 150, 500, 400)  # Pozice (x, y) a rozměry (šířka, výška)

        self.setWindowTitle("KONVERTOR 369 - 1.0.1")

        # Layouty
        # Nastavení hlavního layoutu (vertikální)
        layout = QVBoxLayout()
        # Horizontální layout pro tlačítka
        button_layout = QHBoxLayout()

        # Nadpis
        title = QLabel("KONVERTOR 369")
        title_font = QFont()
        #title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(title, alignment=Qt.AlignCenter)

        layout.addSpacing(20)

        # Popisek a pole pro výběr souboru
        file_label = QLabel("Vstupní soubor XLSX:")
        file_label.setStyleSheet("font-size: 12px; font-weight: bold;")
        layout.addWidget(file_label)
        self.file_path = QLineEdit(self)
        self.file_path.setPlaceholderText("Vyberte soubor ...")
        self.file_path.setReadOnly(True)
        layout.addWidget(self.file_path)

        # Tlačítko pro výběr souboru
        file_button = QPushButton("Vybrat soubor CSV", self)
        file_button.clicked.connect(self.select_file)
        file_button.setFixedSize(150, 30)  # Nastaví tlačítku pevnou šířku a výšku
        file_button.move(50, 50)  # Nastaví pozici tlačítka (x, y)
        layout.addWidget(file_button)

        layout.addSpacing(20)

        # Popisky a vstupní pole
        self.check1 = QCheckBox("Závazky (Vendor report) ??? ", self)
        self.check1.setStyleSheet("font-size: 12px; font-weight: bold;")
        layout.addWidget(self.check1)
        #check1.stateChanged.connect(self.update_check1_state)

        layout.addSpacing(20)

        # Popisky a vstupní pole
        label1 = QLabel("Název výstupního CSV:")
        label1.setStyleSheet("font-size: 12px; font-weight: bold;")
        layout.addWidget(label1)
        self.input1 = QLineEdit(self)
        self.input1.setPlaceholderText("Zadejte název ...")
        layout.addWidget(self.input1)

        layout.addSpacing(20)

        # Tlačítka OK a Zrušit
        ok_button = QPushButton("OK", self)
        ok_button.setStyleSheet("font-size: 14px; font-weight: bold;")
        ok_button.clicked.connect(self.on_ok)
        #layout.addWidget(ok_button)

        cancel_button = QPushButton("Zrušit", self)
        cancel_button.setStyleSheet("font-size: 12px;font-style: italic;")
        cancel_button.clicked.connect(self.on_cancel)
        #layout.addWidget(cancel_button)

        # Přidání tlačítek do horizontálního layoutu
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        # Přidání horizontálního layoutu do hlavního vertikálního layoutu
        layout.addLayout(button_layout)

        layout.addStretch()

        # Copyright text
        copyright_label = QLabel("© 2025 Max Shadow")
        copyright_font = QFont()
        copyright_font.setItalic(True)
        copyright_label.setFont(copyright_font)
        layout.addWidget(copyright_label, alignment=Qt.AlignCenter)

        # Nastavení rozvržení okna
        self.setLayout(layout)


    def select_file(self):
        # Otevře dialog pro výběr souboru
        file_path, _ = QFileDialog.getOpenFileName(self, "Vyberte soubor")
        if file_path:
            self.file_path.setText(file_path)
 
    def on_ok(self):
        # Načte hodnoty ze vstupních polí a spustí vlastní funkci
        OutFileCSV = self.input1.text()
        InFileCSV = self.file_path.text()

        if self.check1.isChecked():
            Vend2Cust = "VENDOR"
        else:
            Vend2Cust = "CUSTOMER"
        #status_dialog = StatusDialog(f"V2C: {Vend2Cust}")
        #status_dialog.exec_()  # Čeká na stisknutí "Pokračuj"
        # Volá vlastní funkci s postupným zobrazením stavových oken
        self.run_custom_function(OutFileCSV, InFileCSV, Vend2Cust)
        #
        self.close()

    def on_cancel(self):
        # Zobrazení zprávy při stisku tlačítka Zrušit
        QMessageBox.information(self, "Zrušeno", "Nic se neprovedlo.")
        self.close()

    def run_custom_function(self, DFO, DFI, V2C):
        status_dialog = StatusDialog(f"Spouštím úlohu...{DFI} -> {DFO} -aka- {V2C}")
        status_dialog.exec_()  # Čeká na stisknutí "Pokračuj"

        # Konstanty
        #KOREKCNI_LIMIT = 1000000

        DFIN = pd.read_csv(
                    DFI
                    # dtype={'Balance01': 'str'}
                    )
        if V2C=="VENDOR":
            # Změna názvu sloupce
            DFIN = DFIN.rename(columns=DefCols.RenameV2Ccols)

        # Aplikace konverze
        DFOUT = f_konv(DFIN)
        #
        if V2C=="VENDOR":
            # Změna názvu sloupce pro Vendor
            DFOUT = DFOUT.rename(columns=DefCols.RenameOUTcols_V)
        else:
            # Změna názvu sloupce pro Customer
            DFOUT = DFOUT.rename(columns=DefCols.RenameOUTcols_C)
        #
        DFOUT.to_csv(DFO
               , index=False
               , sep='|'
               , quoting=1
               , decimal=','
               )

        status_dialog.update_message("Úloha dokončena.")
        status_dialog.exec_()  # Čeká na poslední stisknutí "Pokračuj"

# Hlavní spuštění aplikace
def main():
    # Aplikace
    app = QApplication(sys.argv)
    window = InputWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
     main()

