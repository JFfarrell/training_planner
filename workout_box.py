from PySide2.QtGui import QIcon
from PySide2.QtWidgets import *
from PySide2.QtGui import QPalette, QColor
import sql


class WorkoutBox(QWidget):
    def __init__(self, right_side, planned_session_details, strava_data):
        super().__init__()

        self.right_side = right_side
        self.strava_data = strava_data
        self.planned_session_details = planned_session_details
        self.sql_manipulator = sql.SqlManipulator()
        self.main_layout = QHBoxLayout()
        self.workout_label = QLabel()
        self.delete_button = QToolButton()
        self.delete_button.setIcon(QIcon("images/trash.png"))
        self.delete_button.clicked.connect(self.delete_button_clicked)

        self.planned_workout = QLabel()
        self.planned_workout_length = int(planned_session_details[3])
        self.planned_session_details = planned_session_details
        self.planned_workout.setAutoFillBackground(True)
        self.planned_workout.setMinimumSize(200, 100)
        self.palette = self.palette()

        self.left_layout = QHBoxLayout()
        self.left_layout.addWidget(self.planned_workout)

        self.workout_layout = QHBoxLayout()
        self.workout_layout.addLayout(self.left_layout)
        self.workout_layout.addWidget(self.delete_button)
        self.setLayout(self.workout_layout)
        # self.setStyleSheet("border :2px solid ;"
        #                    "border-color : red; "
        #                    )
        self.set_palette_colour()

    def set_palette_colour(self):
        if len(self.strava_data) > 0:
            self.planned_workout.setText(self.planned_session_details[2])
            matching_strava_workout_data = self.strava_data[0]
            matching_strava_workout_duration = matching_strava_workout_data[2]
            planned_workout_short = matching_strava_workout_duration < self.planned_workout_length * 0.75

            print("Planned session", self.planned_session_details)
            print("Actual strava session", matching_strava_workout_data)

            if self.planned_session_details[1] == matching_strava_workout_data[1]:
                print("Matching workout found")

                if planned_workout_short:
                    self.palette.setColor(QPalette.Window, QColor("Orange"))
                    self.palette.setColor(QPalette.Background, QColor("Orange"))

                else:
                    self.palette.setColor(QPalette.Window, QColor("Green"))
                    self.palette.setColor(QPalette.Background, QColor("Green"))

            else:
                print("No matching workout data found.")
                self.palette.setColor(QPalette.Window, QColor("Red"))
                self.palette.setColor(QPalette.Background, QColor("Red"))

        else:
            print("No matching workout data found.")
            self.planned_workout.setText("Nothing here yet.")
            self.palette.setColor(QPalette.Window, QColor("Red"))
            self.palette.setColor(QPalette.Background, QColor("Red"))

    def delete_button_clicked(self):
        print("planned session details: ", self.planned_session_details)
        print(self.planned_workout)
        self.sql_manipulator.sql_remove_workout(self.planned_session_details)
        self.right_side.render_workout_data_widget(self.planned_session_details[0])
