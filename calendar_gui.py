import sys
from PySide2.QtWidgets import *
from PySide2.QtCore import Qt
from PySide2.QtGui import QIcon
from PySide2.QtGui import QPalette, QColor

import sql
import data_management_functions
from sql import sql_insert


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # main widget settings
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setMinimumSize(500, 500)

        self.date = self.calendar.selectedDate()
        self.initial_date_string = data_management_functions.extract_date_string_from(self.date)
        self.selected_date_string = data_management_functions.extract_date_string_from(self.date)

        # get strava json data
        self.data = data_management_functions.load_strava_data()

        self.sport_choice = ""
        self.duration_choice = 0
        self.intensity_choice = ""

        self.date_label = QLabel(self.date.toString())
        self.text_box = QTextEdit()
        self.sport_dropdown = QComboBox()
        self.duration_dropdown = QComboBox()
        self.intensity_dropdown = QComboBox()
        self.refresh_button = QToolButton()

        # button settings
        self.submit_button = QPushButton("Submit")
        self.submit_button.setMinimumSize(50, 50)
        self.refresh_button.setIcon(QIcon("images/refresh.png"))
        self.refresh_button.clicked.connect(self.data_refresh)

        # scroll area for workouts
        self.scroll_area = QScrollArea()
        self.scroll_area.setMinimumSize(300, 200)
        self.scroll_area.setWidget(QLabel("Nothing here yet :)"))

        self.calendar.clicked.connect(self.render_workout_data_widget)
        self.sport_dropdown.currentIndexChanged.connect(self.sport_changed)
        self.intensity_dropdown.currentIndexChanged.connect(self.intensity_changed)
        self.duration_dropdown.currentIndexChanged.connect(self.duration_changed)
        self.submit_button.clicked.connect(self.button_clicked)

        self.sports = ["Ride", "Run", "Swim", "S and C"]
        self.sport_dropdown.addItems(self.sports)
        self.sport_dropdown.setMinimumSize(50, 50)

        self.intensity = ["Z1", "Z2", "Z3", "Z4", "Z5"]
        self.intensity_dropdown.addItems(self.intensity)
        self.intensity_dropdown.setMinimumSize(50, 50)

        self.duration = ["30", "45", "60", "75", "90", "105", "120", "135", "150", "160", "180"]
        self.duration_dropdown.addItems(self.duration)
        self.duration_dropdown.setMinimumSize(50, 50)

        layout = QHBoxLayout()
        right_box = QVBoxLayout()
        self.right_upper = QHBoxLayout()
        self.right_lower = QHBoxLayout()
        self.right_lower_right = QHBoxLayout()
        self.right_lower_left = QHBoxLayout()
        dropdowns = QVBoxLayout()

        self.right_upper.addWidget(self.date_label, alignment=Qt.AlignCenter)
        self.right_upper.addWidget(self.refresh_button)

        self.right_lower.addLayout(self.right_lower_left)
        self.right_lower.addLayout(self.right_lower_right)

        self.right_lower_left.addWidget(self.scroll_area)
        self.right_lower_right.addLayout(dropdowns)

        dropdowns.addWidget(self.sport_dropdown)
        dropdowns.addWidget(self.duration_dropdown)
        dropdowns.addWidget(self.intensity_dropdown)
        dropdowns.addWidget(self.submit_button)

        right_box.addLayout(self.right_upper)
        right_box.addLayout(self.right_lower)
        layout.addWidget(self.calendar)
        layout.addLayout(right_box)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.render_workout_data_widget(self.initial_date_string)

    def retrieve_workout_data_for_display_widget(self, selected_date_string):
        planned_sessions_for_selected_day = sql.sql_retrieve(selected_date_string)
        print("daily data: ", planned_sessions_for_selected_day)
        planned_workouts_for_day = []

        if len(planned_sessions_for_selected_day) != 0:

            for planned_session_details in planned_sessions_for_selected_day:
                strava_data_for_same_date = data_management_functions.return_matching_strava_data(self.data, selected_date_string)
                planned_workout = QTextEdit(planned_session_details[2])
                planned_workout_length = int(planned_session_details[3])
                planned_workout.setAutoFillBackground(True)
                palette = self.palette()

                if len(strava_data_for_same_date) > 0:
                    matching_strava_workout_data = strava_data_for_same_date[0]
                    matching_strava_workout_duration = matching_strava_workout_data[2]
                    planned_workout_short = matching_strava_workout_duration < planned_workout_length * 0.75

                    print("Planned session", planned_session_details)
                    print("Actual strava session", matching_strava_workout_data)

                    if planned_session_details[1] == matching_strava_workout_data[1]:

                        if planned_workout_short:
                            palette.setColor(QPalette.Window, QColor("Orange"))
                            palette.setColor(QPalette.Background, QColor("Orange"))

                        else:
                            palette.setColor(QPalette.Window, QColor("Green"))
                            palette.setColor(QPalette.Background, QColor("Green"))

                    else:
                        print("No matching workout data found.")
                        palette.setColor(QPalette.Window, QColor("Red"))
                        palette.setColor(QPalette.Background, QColor("Red"))

                else:
                    print("No matching workout data found.")
                    palette.setColor(QPalette.Window, QColor("Red"))
                    palette.setColor(QPalette.Background, QColor("Red"))

                planned_workout.setPalette(palette)
                planned_workouts_for_day.append(planned_workout)

            return planned_workouts_for_day

    def render_workout_data_widget(self, *args):
        if type(args[0]) == str:
            self.selected_date_string = args[0]
        else:
            self.selected_date_string = data_management_functions.extract_date_string_from(self.calendar.selectedDate())

        self.date_label.setText(self.calendar.selectedDate().toString())

        workout_display_widget = QWidget()
        vbox = QVBoxLayout()
        workout_display_widget.setLayout(vbox)

        returned_planned_workouts = self.retrieve_workout_data_for_display_widget(self.selected_date_string)
        if returned_planned_workouts is not None:
            for workout in returned_planned_workouts:
                vbox.addWidget(workout)
        else:
            workout_display_widget = QLabel("Nothing here yet :)")

        self.scroll_area.setWidget(workout_display_widget)

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

    def data_refresh(self):
        print("Refreshing strava data...")
        data_management_functions.fetch_strava_data()
        print("Done")


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
