from PySide2.QtCore import Qt, QDate
from PySide2.QtGui import QIcon
from PySide2.QtWidgets import *
from PySide2.QtGui import QPalette, QColor

import data_management_functions
import sql
import sys


class RightSide(QWidget):
    def __init__(self, current_selected_date):
        super().__init__()

        self.current_selected_date = current_selected_date
        self.strava_json_data = data_management_functions.load_strava_data()

        dropdowns_layout = QVBoxLayout()
        self.date_label = QLabel(self.current_selected_date.toString())
        self.selected_date_string = data_management_functions.extract_date_string_from(current_selected_date)

        # button settings
        self.refresh_button = QToolButton()
        self.submit_button = QPushButton("Submit")
        self.submit_button.setMinimumSize(50, 50)
        self.refresh_button.setIcon(QIcon("images/refresh.png"))
        self.refresh_button.clicked.connect(self.data_refresh)
        self.submit_button.clicked.connect(self.button_clicked)

        # sport dropdown
        self.sport_dropdown = QComboBox()
        self.sport_choice = "Ride"
        self.sports = ["Ride", "Run", "Swim", "S and C"]
        self.sport_dropdown.addItems(self.sports)
        self.sport_dropdown.setMinimumSize(50, 50)
        self.sport_dropdown.currentIndexChanged.connect(self.sport_changed)

        # zone dropdown
        self.zone_dropdown = QComboBox()
        self.zone_choice = "Z1"
        self.zone = ["Z1", "Z2", "Z3", "Z4", "Z5"]
        self.zone_dropdown.addItems(self.zone)
        self.zone_dropdown.setMinimumSize(50, 50)
        self.zone_dropdown.currentIndexChanged.connect(self.intensity_changed)

        # duration dropdown
        self.duration_dropdown = QComboBox()
        self.duration_choice = "30"
        self.duration = ["30", "45", "60", "75", "90", "105", "120", "135", "150", "160", "180"]
        self.duration_dropdown.addItems(self.duration)
        self.duration_dropdown.setMinimumSize(50, 50)
        self.duration_dropdown.currentIndexChanged.connect(self.duration_changed)

        self.layout = QVBoxLayout()
        self.header_layout = QHBoxLayout()
        self.body_layout = QVBoxLayout()
        self.workouts_box = QHBoxLayout()

        # scroll area for workouts
        self.scroll_area = QScrollArea()
        self.scroll_area.setMinimumSize(300, 100)
        self.scroll_area.setWidget(QLabel("Nothing here yet :)"))

        self.header_layout.addWidget(self.date_label, alignment=Qt.AlignCenter)
        self.header_layout.addWidget(self.refresh_button)

        dropdowns_layout.addWidget(self.zone_dropdown)
        dropdowns_layout.addWidget(self.sport_dropdown)
        dropdowns_layout.addWidget(self.duration_dropdown)
        dropdowns_layout.addWidget(self.submit_button)

        self.workouts_box.addWidget(self.scroll_area)
        self.workouts_box.addLayout(dropdowns_layout)
        self.body_layout.addLayout(self.workouts_box)

        self.layout.addLayout(self.header_layout)
        self.layout.addLayout(self.body_layout)
        self.setLayout(self.layout)

    def intensity_changed(self, i):
        self.zone_choice = self.zone[i]
        print(self.zone_choice)
        return self.zone_choice

    def sport_changed(self, i):
        self.sport_choice = self.sports[i]
        print(self.sport_choice)
        return self.sport_choice

    def duration_changed(self, i):
        self.duration_choice = int(self.duration[i])
        print(self.duration_choice)
        return self.duration_choice

    def button_clicked(self):
        event_name = f"{self.duration_choice} {self.sport_choice}"
        print(event_name)

        sql.sql_insert(self.selected_date_string,
                       self.sport_choice,
                       event_name,
                       self.duration_choice,
                       self.zone_choice)

    def render_workout_data_widget(self, date_string):
        self.selected_date_string = date_string
        workout_display_widget = QWidget()
        vbox = QVBoxLayout()
        workout_display_widget.setLayout(vbox)

        returned_planned_workouts = self.retrieve_workout_data_for_display_widget(
            self.selected_date_string)

        if returned_planned_workouts is not None:
            for workout in returned_planned_workouts:
                vbox.addWidget(workout)
        else:
            workout_display_widget = QLabel("Nothing here yet :)")

        self.scroll_area.setWidget(workout_display_widget)

    def retrieve_workout_data_for_display_widget(self, selected_date_string):
        """
        should implement a measure to prevent this method failing is bad data is
        returned from the database
        """

        planned_sessions_for_selected_day = sql.sql_retrieve(selected_date_string)
        print(f"daily data for {selected_date_string}: ", planned_sessions_for_selected_day)
        planned_workouts_for_day = []

        if len(planned_sessions_for_selected_day) != 0:

            for planned_session_details in planned_sessions_for_selected_day:
                strava_data_for_same_date = data_management_functions.return_matching_strava_data(self.strava_json_data,
                                                                                                  selected_date_string)
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

    def data_refresh(self):
        print("Refreshing strava data...")
        data_management_functions.fetch_strava_data()
        print("Done")
