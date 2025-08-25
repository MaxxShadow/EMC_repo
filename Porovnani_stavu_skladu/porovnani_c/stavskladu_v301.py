import sys
import pandas as pd 

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QPushButton, QMessageBox, QFileDialog, QLabel, QDialog)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

# Doplnění chybějících artiklů do SKUT a FO
def dopln_chybejici_artikly(FO, SKUT, ARTIKL, default_lot, default_status):
    # Doplnění chybějících artiklů do SKUT
    chybne_skut = ARTIKL[~ARTIKL['Artikl'].isin(SKUT['Artikl'])]
    for _, row in chybne_skut.iterrows():
        SKUT = pd.concat([SKUT, pd.DataFrame({"Artikl": [row['Artikl']], "Mnozstvi": [0]})], ignore_index=True)
    
    # Doplnění chybějících artiklů do FO
    chybne_fo = ARTIKL[~ARTIKL['Artikl'].isin(FO['Artikl'])]
    for _, row in chybne_fo.iterrows():
        FO = pd.concat([FO, pd.DataFrame({
            "Artikl": [row['Artikl']],
            "Lot": [default_lot],
            "Status": [default_status],
            "Mnozstvi": [0],
            "Mnozstvi_KOR": [0],
            "Modifikovano": [2]
        })], ignore_index=True)
    
    return FO, SKUT

# Funkce pro úpravu sloupce Mnozstvi v FO na celočíselné hodnoty
def oprav_mnozstvi(FO, SKUT, limit, default_lot, default_status):
    FO['Mnozstvi_KOR'] = FO['Mnozstvi']  # Kopie původního množství
    FO['Modifikovano'] = FO.get('Modifikovano', 0)  # Nový sloupec pro označení změn, defaultně 0
    
    # Procházení každého artiklu ve SKUT
    for _, row in SKUT.iterrows():
        artikl = row['Artikl']
        skut_mnozstvi = row['Mnozstvi']
        
        # Vyber řádky s daným artiklem v FO
        mask = FO['Artikl'] == artikl
        fo_rows = FO[mask].copy()  # Vytvoření kopie pro práci s korekcí
        
        # Současný součet množství v FO pro daný artikl
        current_sum = fo_rows['Mnozstvi'].sum()
        rozdil = skut_mnozstvi - current_sum
        
        # Korekce, pokud je rozdíl nenulový
        if rozdil != 0:
            for idx in fo_rows.index:
                aktualni_mnozstvi = FO.loc[idx, 'Mnozstvi_KOR']
                
                # Zjistíme korekci pro aktuální řádek v rámci limitu
                if abs(rozdil) <= limit:
                    korekce = rozdil
                else:
                    korekce = limit if rozdil > 0 else -limit
                
                # Aplikujeme korekci na aktuální množství a aktualizujeme rozdíl
                nova_hodnota = aktualni_mnozstvi + korekce
                FO.loc[idx, 'Mnozstvi_KOR'] = nova_hodnota
                if korekce != 0:  # Zaznamenáme změnu, pokud byla hodnota upravena
                    FO.loc[idx, 'Modifikovano'] = 1
                rozdil -= korekce
                
                # Pokud jsme rozdíl vyrovnali, můžeme zastavit
                if rozdil == 0:
                    break

            # Pokud stále zbývá rozdíl, přidáme nový řádek s chybějícím množstvím
            if rozdil != 0:
                FO = pd.concat([FO, pd.DataFrame({
                    "Artikl": [artikl],
                    "Lot": [default_lot],
                    "Status": [default_status],
                    "Mnozstvi": [0],
                    "Mnozstvi_KOR": [rozdil],
                    "Modifikovano": [2]
                })], ignore_index=True)
    
    return FO


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

        self.setWindowTitle("Stav skladu - srovnání počtů")

        # Layouty
        # Nastavení hlavního layoutu (vertikální)
        layout = QVBoxLayout()
        # Horizontální layout pro tlačítka
        button_layout = QHBoxLayout()

        # Nadpis
        title = QLabel("Definice parametrů pro srovnání počtů")
        title_font = QFont()
        #title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(title, alignment=Qt.AlignCenter)

        layout.addSpacing(20)

        # Popisek a pole pro výběr souboru
        file_label = QLabel("Vybraný soubor XLSX:")
        file_label.setStyleSheet("font-size: 12px; font-weight: bold;")
        layout.addWidget(file_label)
        self.file_path = QLineEdit(self)
        self.file_path.setPlaceholderText("Vyberte soubor ...")
        self.file_path.setReadOnly(True)
        layout.addWidget(self.file_path)

        # Tlačítko pro výběr souboru
        file_button = QPushButton("Vybrat soubor XLSX", self)
        file_button.clicked.connect(self.select_file)
        file_button.setFixedSize(150, 30)  # Nastaví tlačítku pevnou šířku a výšku
        file_button.move(50, 50)  # Nastaví pozici tlačítka (x, y)
        layout.addWidget(file_button)

        layout.addSpacing(20)

        # Popisky a vstupní pole
        label1 = QLabel("List FO:")
        label1.setStyleSheet("font-size: 12px; font-weight: bold;")
        layout.addWidget(label1)
        self.input1 = QLineEdit(self)
        self.input1.setPlaceholderText("Zadejte název listu FO ...")
        layout.addWidget(self.input1)

        label2 = QLabel("List SKUT:")
        label2.setStyleSheet("font-size: 12px; font-weight: bold;")
        layout.addWidget(label2)
        self.input2 = QLineEdit(self)
        self.input2.setPlaceholderText("Zadejte název listu SKUT ...")
        layout.addWidget(self.input2)

        label3 = QLabel("List KAT:")
        label3.setStyleSheet("font-size: 12px; font-weight: bold;")
        layout.addWidget(label3)
        self.input3 = QLineEdit(self)
        self.input3.setPlaceholderText("Zadejte název listu KAT ...")
        layout.addWidget(self.input3)

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
        copyright_label = QLabel("© 2024 Max Shadow")
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
        ListFO = self.input1.text()
        ListSKUT = self.input2.text()
        ListKAT = self.input3.text()
        InFileXls = self.file_path.text()
        # Volá vlastní funkci s postupným zobrazením stavových oken
        self.run_custom_function(ListFO, ListSKUT, ListKAT, InFileXls)
        #
        self.close()

    def on_cancel(self):
        # Zobrazení zprávy při stisku tlačítka Zrušit
        QMessageBox.information(self, "Zrušeno", "Nic se neprovedlo.")
        self.close()

    def run_custom_function(self, value1, value2, value3, file):
        # value1 = ListFO
        # value2 = ListSKUT
        # value3 = ListKAT
        # file   = InFileXls
        # 
        status_dialog = StatusDialog("Spouštím úlohu...")
        status_dialog.exec_()  # Čeká na stisknutí "Pokračuj"

        # Konstanty
        DEFAULT_LOT = "_Z_"
        DEFAULT_STATUS = "XNEW"
        KOREKCNI_LIMIT = 1000000

        FO = pd.read_excel(file,value1)
        SKUT = pd.read_excel(file,value2)
        ARTIKL = pd.read_excel(file,value3)

        # Aplikace doplnění chybějících artiklů
        FO, SKUT = dopln_chybejici_artikly(FO, SKUT, ARTIKL, DEFAULT_LOT, DEFAULT_STATUS)

        # Použití funkce s daným limitem
        FO = oprav_mnozstvi(FO, SKUT, KOREKCNI_LIMIT, DEFAULT_LOT, DEFAULT_STATUS)

        # Seřazení dataframe FO podle sloupce Artikl
        FO = FO.sort_values(by="Artikl").reset_index(drop=True)

        FO.to_excel("Output.xlsx","data-FO-kor")

        status_dialog.update_message("Úloha dokončena.")
        status_dialog.exec_()  # Čeká na poslední stisknutí "Pokračuj"


# Hlavní spuštění aplikace
def main():
    # Spuštění aplikace
    app = QApplication(sys.argv)
    window = InputWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
     main()