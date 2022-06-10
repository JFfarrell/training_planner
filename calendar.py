import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt

import sql
import test
from test import check_data
from sql import sql_insert


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.date = self.calendar.selectedDate()
        self.selected_date_string = test.date_string(self.date)
        self.data = check_data()
        self.sport_choice = ""
        self.duration_choice = 0
        self.intensity_choice = ""

        self.date_label = QLabel(self.date.toString())
        self.workouts_label = QLabel("Nothing here yet.")
        self.text_box = QTextEdit()
        self.sport_dropdown = QComboBox()
        self.duration_dropdown = QComboBox()
        self.intensity_dropdown = QComboBox()
        self.submit_button = QPushButton("Submit")

        self.calendar.clicked.connect(self.clicked)
        self.sport_dropdown.currentIndexChanged.connect(self.sport_changed)
        self.intensity_dropdown.currentIndexChanged.connect(self.intensity_changed)
        self.duration_dropdown.currentIndexChanged.connect(self.duration_changed)
        self.submit_button.clicked.connect(self.button_clicked)

        self.sports = ["Bike", "Run", "Swim", "S and C"]
        self.sport_dropdown.addItems(self.sports)

        self.intensity = ["Z1", "Z2", "Z3", "Z4", "Z5"]
        self.intensity_dropdown.addItems(self.intensity)

        self.duration = ["30", "45", "60", "75", "90", "105", "120", "135", "150"]
        self.duration_dropdown.addItems(self.duration)

        layout = QHBoxLayout()
        right_box = QVBoxLayout()
        right_upper = QHBoxLayout()
        right_lower = QHBoxLayout()
        dropdowns = QVBoxLayout()

        right_upper.addWidget(self.date_label, alignment=Qt.AlignCenter)
        right_lower.addWidget(self.workouts_label)
        right_lower.addLayout(dropdowns)
        dropdowns.addWidget(self.sport_dropdown)
        dropdowns.addWidget(self.duration_dropdown)
        dropdowns.addWidget(self.intensity_dropdown)
        dropdowns.addWidget(self.submit_button)
        right_box.addLayout(right_upper)
        right_box.addLayout(right_lower)
        layout.addWidget(self.calendar)
        layout.addLayout(right_box)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def clicked(self):
        self.selected_date_string = test.date_string(self.calendar.selectedDate())
        self.date_label.setText(self.calendar.selectedDate().toString())
        daily_data = sql.sql_retrieve(self.selected_date_string)

        if len(daily_data) != 0:
            self.workouts_label.setText(str(daily_data))
        else:
            self.workouts_label.setText("Nothing here yet.")

    def sport_changed(self, i):
        self.sport_choice = self.sports[i]
        print(self.sport_choice)

    def duration_changed(self, i):
        self.duration_choice = int(self.duration[i])
        print(self.duration_choice)

    def intensity_changed(self, i):
        self.intensity_choice = self.intensity[i]
        print(self.intensity)

    def button_clicked(self):
        event_name = f"{self.duration_choice} {self.sport_choice}"

        sql_insert(self.selected_date_string,
                   self.sport_choice,
                   event_name,
                   self.duration_choice,
                   self.intensity_choice)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
