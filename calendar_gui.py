import sys
from PySide2.QtWidgets import *

import data_management_functions
import right_side


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # main widget settings
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setMinimumSize(500, 500)

        self.date = self.calendar.selectedDate()
        self.selected_date_string = data_management_functions.extract_date_string_from(self.date)

        self.right_side_object = right_side.RightSide(self.date)
        self.calendar.clicked.connect(self.trigger_widget_on_calendar_click)

        layout = QHBoxLayout()
        layout.addWidget(self.calendar)
        layout.addWidget(self.right_side_object)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.right_side_object.render_workout_data_widget(self.selected_date_string)

    def set_current_date_variables(self):
        self.date = self.calendar.selectedDate()
        self.selected_date_string = data_management_functions.extract_date_string_from(self.date)
        self.right_side_object.date_label.setText(self.date.toString())

    def trigger_widget_on_calendar_click(self):
        self.set_current_date_variables()
        self.right_side_object.render_workout_data_widget(self.selected_date_string)


app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec_()
