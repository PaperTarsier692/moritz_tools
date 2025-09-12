import sys
from typing import Any
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QMessageBox, QVBoxLayout,
    QLabel, QLineEdit, QCheckBox, QHBoxLayout, QTextEdit, QRadioButton,
    QComboBox, QListWidget, QSlider, QSpinBox, QProgressBar, QTabWidget,
    QFormLayout, QDateEdit, QTimeEdit, QDateTimeEdit, QColorDialog,
    QFileDialog, QFontDialog, QDial
)


class MainWindow(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("PyQt6 Mega-Beispiel")
        self.setGeometry(100, 100, 700, 600)

        main_layout: QVBoxLayout = QVBoxLayout()

        # Tabs
        self.tabs: QTabWidget = QTabWidget()
        main_layout.addWidget(self.tabs)

        # --- Tab 1: Formular ---
        form_widget: QWidget = QWidget()
        form_layout: QFormLayout = QFormLayout()

        self.name_input: QLineEdit = QLineEdit()
        form_layout.addRow("Name:", self.name_input)

        self.email_input: QLineEdit = QLineEdit()
        form_layout.addRow("E-Mail:", self.email_input)

        self.password_input: QLineEdit = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Passwort:", self.password_input)

        self.date_edit: QDateEdit = QDateEdit()
        form_layout.addRow("Geburtsdatum:", self.date_edit)

        self.time_edit: QTimeEdit = QTimeEdit()
        form_layout.addRow("Uhrzeit:", self.time_edit)

        self.datetime_edit: QDateTimeEdit = QDateTimeEdit()
        form_layout.addRow("Datum & Zeit:", self.datetime_edit)

        self.gender_combo: QComboBox = QComboBox()
        self.gender_combo.addItems(["Männlich", "Weiblich", "Divers"])
        form_layout.addRow("Geschlecht:", self.gender_combo)

        self.agree_checkbox: QCheckBox = QCheckBox("AGB akzeptieren")
        form_layout.addRow(self.agree_checkbox)

        self.form_submit: QPushButton = QPushButton("Absenden")
        self.form_submit.clicked.connect(self.submit_form)
        form_layout.addRow(self.form_submit)

        form_widget.setLayout(form_layout)
        self.tabs.addTab(form_widget, "Formular")

        # --- Tab 2: Listen & Auswahl ---
        list_widget: QWidget = QWidget()
        list_layout: QVBoxLayout = QVBoxLayout()

        self.list_label: QLabel = QLabel("Wähle ein Element aus der Liste:")
        list_layout.addWidget(self.list_label)

        self.list: QListWidget = QListWidget()
        self.list.addItems(
            ["Apfel", "Banane", "Kirsche", "Dattel", "Erdbeere"])
        list_layout.addWidget(self.list)

        self.radio1: QRadioButton = QRadioButton("Option 1")
        self.radio2: QRadioButton = QRadioButton("Option 2")
        self.radio3: QRadioButton = QRadioButton("Option 3")
        list_layout.addWidget(self.radio1)
        list_layout.addWidget(self.radio2)
        list_layout.addWidget(self.radio3)

        self.select_button: QPushButton = QPushButton("Auswahl anzeigen")
        self.select_button.clicked.connect(self.show_selection)
        list_layout.addWidget(self.select_button)

        list_widget.setLayout(list_layout)
        self.tabs.addTab(list_widget, "Listen & Auswahl")

        # --- Tab 3: Slider, SpinBox, ProgressBar, Dial ---
        controls_widget: QWidget = QWidget()
        controls_layout: QVBoxLayout = QVBoxLayout()

        self.slider: QSlider = QSlider()
        self.slider.setMinimum(0)
        self.slider.setMaximum(100)
        controls_layout.addWidget(QLabel("Slider:"))
        controls_layout.addWidget(self.slider)

        self.spinbox: QSpinBox = QSpinBox()
        self.spinbox.setRange(0, 100)
        controls_layout.addWidget(QLabel("SpinBox:"))
        controls_layout.addWidget(self.spinbox)

        self.dial: QDial = QDial()
        self.dial.setRange(0, 100)
        controls_layout.addWidget(QLabel("Dial:"))
        controls_layout.addWidget(self.dial)

        self.progress: QProgressBar = QProgressBar()
        controls_layout.addWidget(QLabel("ProgressBar:"))
        controls_layout.addWidget(self.progress)

        self.update_progress_btn: QPushButton = QPushButton(
            "Fortschritt setzen")
        self.update_progress_btn.clicked.connect(self.update_progress)
        controls_layout.addWidget(self.update_progress_btn)

        controls_widget.setLayout(controls_layout)
        self.tabs.addTab(controls_widget, "Steuerelemente")

        # --- Tab 4: Text, Farben, Datei, Schrift ---
        misc_widget: QWidget = QWidget()
        misc_layout: QVBoxLayout = QVBoxLayout()

        self.textedit: QTextEdit = QTextEdit()
        self.textedit.setPlaceholderText("Hier kannst du Text eingeben...")
        misc_layout.addWidget(QLabel("Mehrzeiliges Textfeld:"))
        misc_layout.addWidget(self.textedit)

        self.color_btn: QPushButton = QPushButton("Farbe wählen")
        self.color_btn.clicked.connect(self.choose_color)
        misc_layout.addWidget(self.color_btn)

        self.file_btn: QPushButton = QPushButton("Datei öffnen")
        self.file_btn.clicked.connect(self.open_file)
        misc_layout.addWidget(self.file_btn)

        self.font_btn: QPushButton = QPushButton("Schrift wählen")
        self.font_btn.clicked.connect(self.choose_font)
        misc_layout.addWidget(self.font_btn)

        misc_widget.setLayout(misc_layout)
        self.tabs.addTab(misc_widget, "Text & Dialoge")

        # --- Hauptfenster-Buttons ---
        main_button_layout: QHBoxLayout = QHBoxLayout()
        self.quit_button: QPushButton = QPushButton("Beenden")
        self.quit_button.clicked.connect(self.close)
        main_button_layout.addWidget(self.quit_button)

        main_layout.addLayout(main_button_layout)
        self.setLayout(main_layout)

    def submit_form(self) -> None:
        name: str = self.name_input.text()
        email: str = self.email_input.text()
        password: str = self.password_input.text()
        agreed: bool = self.agree_checkbox.isChecked()
        if not name or not email or not password:
            QMessageBox.warning(self, "Fehler", "Bitte alle Felder ausfüllen.")
            return
        if not agreed:
            QMessageBox.warning(self, "Fehler", "Bitte AGB akzeptieren.")
            return
        QMessageBox.information(self, "Erfolg", f"Willkommen, {name}!")

    def show_selection(self) -> None:
        selected_items = self.list.selectedItems()
        radios = [self.radio1, self.radio2, self.radio3]
        radio_selected = next((r.text()
                              for r in radios if r.isChecked()), None)
        msg = ""
        if selected_items:
            msg += f"Liste: {selected_items[0].text()}\n"
        if radio_selected:
            msg += f"Radio: {radio_selected}"
        if not msg:
            msg = "Nichts ausgewählt."
        QMessageBox.information(self, "Auswahl", msg)

    def update_progress(self) -> None:
        value = (self.slider.value() +
                 self.spinbox.value() + self.dial.value()) // 3
        self.progress.setValue(value)

    def choose_color(self) -> None:
        color = QColorDialog.getColor()
        if color.isValid():
            QMessageBox.information(
                self, "Farbe", f"Gewählte Farbe: {color.name()}")

    def open_file(self) -> None:
        file, _ = QFileDialog.getOpenFileName(self, "Datei öffnen")
        if file:
            QMessageBox.information(self, "Datei", f"Gewählte Datei: {file}")

    def choose_font(self) -> None:
        font, ok = QFontDialog.getFont()
        if ok:
            QMessageBox.information(
                self, "Schrift", f"Gewählte Schrift: {font.family()}")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
