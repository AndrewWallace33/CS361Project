# Andrew Wallace
# BudgetInvestmentCalculator
# CS361 Class Project

import sys
from PyQt5.QtWidgets import *


# Citation: Tutorial for building a GUI in PyQt5 from
# https://www.tutorialspoint.com/pyqt5/pyqt5_tutorial.pdf was used to develop this GUI.
# And geeksforgeeks.com
# And doc.qt.io

#TODO: All text fields need error validation!!!!

# Create the App
class Window(QWidget):
    # Create Application and Main window.

    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        # Variables to run program
        self.monthly_expenses = 0.00
        self.income_minus_expenses = 0.00
        self.principal = 0.00
        self.interest = 0.00
        self.total = 0.00

        # Set up the Expense Window
        self.expense_window = QMdiSubWindow(self)
        self.expense_window.setWindowTitle("Add an Expense")
        self.expense_window.setGeometry(30, 75, 600, 200)

        # Description Label and text Box
        description_label = QLabel("Expense Description:", self.expense_window)
        description_label.resize(200, 30)
        description_label.move(30, 45)
        self.expense_description_textbox = QLineEdit(self.expense_window)
        self.expense_description_textbox.setPlaceholderText(" Enter an Expense Description (EX: Rent)")
        self.expense_description_textbox.resize(300, 30)
        self.expense_description_textbox.move(230, 45)

        # Amount Label and text Box
        amount_label = QLabel("Expense Amount:", self.expense_window)
        amount_label.resize(200, 30)
        amount_label.move(30, 90)
        self.expense_amount_textbox = QLineEdit(self.expense_window)
        self.expense_amount_textbox.setPlaceholderText(" Enter an Expense Amount (EX: 1250.00)")
        self.expense_amount_textbox.resize(300, 30)
        self.expense_amount_textbox.move(230, 90)

        # Add Cancel Button
        self.cancel_button = QPushButton("Cancel", self.expense_window)
        self.cancel_button.resize(120, 30)
        self.cancel_button.move(45, 150)
        self.cancel_button.clicked.connect(lambda: self.cancelled())

        # Add Add Expense Button
        self.add_button = QPushButton("Add Expense", self.expense_window)
        self.add_button.resize(120, 30)
        self.add_button.move(435, 150)
        self.add_button.clicked.connect(lambda: self.committed())

        self.expense_window.hide()

        # Net Income Label and Text Box
        net_income_label = QLabel("Enter Your Monthly Net Income:", self)
        net_income_label.resize(300, 30)
        net_income_label.move(30, 15)

        self.net_income_textbox = QLineEdit(self)
        self.net_income_textbox.setPlaceholderText(" Enter Net Income (EX: 1200)")
        self.net_income_textbox.resize(300, 30)
        self.net_income_textbox.move(300, 15)
        self.net_income_textbox.textChanged.connect(lambda: self.calculate_net_value())

        # Time Frame Label and Text Box
        time_frame_label = QLabel("Enter Your Time Period in Months:", self)
        time_frame_label.resize(300, 30)
        time_frame_label.move(30, 75)

        self.time_frame_textbox = QLineEdit(self)
        self.time_frame_textbox.setPlaceholderText(" Enter Time Period in Months (EX: 12)")
        self.time_frame_textbox.resize(300, 30)
        self.time_frame_textbox.move(300, 75)

        # Interest Rate Label and Text Box
        annual_rate_label = QLabel("Enter Your Expected Annual Interest Rate:", self)
        annual_rate_label.resize(300, 30)
        annual_rate_label.move(30, 135)

        self.annual_rate_textbox = QLineEdit(self)
        self.annual_rate_textbox.setPlaceholderText(" Enter Expected Annual Interest Rate (EX: 7.2)")
        self.annual_rate_textbox.resize(300, 30)
        self.annual_rate_textbox.move(300, 135)

        # Total Principal Invested Label and Value
        principal_label = QLabel("Total Principal Invested:", self)
        principal_label.resize(250, 30)
        principal_label.move(30, 340)

        self.principal_value = QLabel("$%.2f" % self.principal, self)
        self.principal_value.resize(250, 30)
        self.principal_value.move(350, 340)

        # Total Interest Invested Label and Value
        interest_label = QLabel("Total Projected Interest Earned:", self)
        interest_label.resize(250, 30)
        interest_label.move(30, 400)

        self.interest_value = QLabel("$%.2f" % self.interest, self)
        self.interest_value.resize(250, 30)
        self.interest_value.move(350, 400)

        # Total Interest Invested Label and Value
        total_label = QLabel("Total Projected Value:", self)
        total_label.resize(250, 30)
        total_label.move(30, 460)

        self.total_value = QLabel("$%.2f" % self.total, self)
        self.total_value.resize(250, 30)
        self.total_value.move(350, 460)

        # Expense Table Label
        monthly_expense_label = QLabel("Monthly Expenses", self)
        monthly_expense_label.resize(250, 30)
        monthly_expense_label.move(875, 40)

        # Add Expense Button
        self.add_expense_button = QPushButton("Add Expense", self)
        self.add_expense_button.resize(120, 30)
        self.add_expense_button.move(1045, 40)
        self.add_expense_button.clicked.connect(lambda: self.add_expense_launch())

        # Remove Selected Expense Button
        self.remove_expense_button = QPushButton("Remove Selected Expense", self)
        self.remove_expense_button.resize(200, 30)
        self.remove_expense_button.move(630, 40)
        self.remove_expense_button.clicked.connect(lambda: self.remove_expense())

        # Create Expense Table and set column names
        self.expense_table = QTableWidget(self)
        self.expense_table.setColumnCount(2)
        self.expense_table.setColumnWidth(0, 385)
        self.expense_table.setColumnWidth(1, 150)
        self.expense_table.setHorizontalHeaderLabels(["Description", "$ Amount"])
        self.expense_table.resize(550, 250)
        self.expense_table.move(630, 75)

        # Total Monthly Expense Label and Value
        total_expense_label = QLabel("Total Monthly Expense:", self)
        total_expense_label.resize(250, 30)
        total_expense_label.move(630, 350)

        self.total_expense_value = QLabel("$%.2f" % self.monthly_expenses, self)
        self.total_expense_value.resize(230, 30)
        self.total_expense_value.move(1095, 350)

        # Income - Expenses Label and Value
        net_label = QLabel("Monthly Net Income Less Expenses:", self)
        net_label.resize(250, 30)
        net_label.move(630, 410)

        self.net_value = QLabel("$%.2f" % self.income_minus_expenses, self)
        self.net_value.resize(230, 30)
        self.net_value.move(1095, 410)

        # Add Calculate Button
        self.calculate_button = QPushButton("Calculate", self)
        self.calculate_button.resize(250, 60)
        self.calculate_button.move(475, 500)
        self.calculate_button.clicked.connect(lambda: self.calculate())

        # Set the main window size and Title
        self.setGeometry(50, 50, 1200, 600)
        self.setWindowTitle("Budget Investment Calculator")

    def add_expense_launch(self):
        # Show the window if it isn't visible
        if self.expense_window.isVisible() is False:
            self.expense_window.show()
            self.expense_window.raise_()

    def remove_expense(self):
        # Citation: Used the following blog post to help code the removal
        # https://forum.qt.io/topic/25599/remove-user-selected-rows-from-a-qtablewidget/8
        # Decrement the total monthly expense
        row_num = self.expense_table.currentRow()
        value = self.expense_table.item(row_num, 1).text()
        self.monthly_expenses -= float(value)
        # Remove the row
        self.expense_table.removeRow(self.expense_table.currentRow())
        # Update the shown value
        self.total_expense_value.setText("$%.2f" % self.monthly_expenses)
        self.calculate_net_value()

    def cancelled(self):
        self.expense_amount_textbox.clear()
        self.expense_description_textbox.clear()
        self.expense_window.hide()

    def committed(self):
        # grab data and clear the values
        amount = self.expense_amount_textbox.text()
        self.expense_amount_textbox.clear()
        desc = self.expense_description_textbox.text()
        self.expense_description_textbox.clear()
        # Insert a new row
        row_count = self.expense_table.rowCount()
        self.expense_table.insertRow(row_count)
        # Insert the item
        self.expense_table.setItem(row_count, 0, QTableWidgetItem(desc))
        self.expense_table.setItem(row_count, 1, QTableWidgetItem(amount))
        # Index the expense amount
        self.monthly_expenses += float(amount)
        self.total_expense_value.setText("$%.2f" % self.monthly_expenses)
        self.calculate_net_value()
        # Hide the window
        self.expense_window.hide()

    def calculate_net_value(self):
        # On Change check the value in th text box
        value = self.net_income_textbox.text()
        if is_float(value):
            # If it is a float update the total expenses
            self.income_minus_expenses = float(value) - self.monthly_expenses
            self.net_value.setText("$%.2f" % self.income_minus_expenses)

    def calculate(self):
        if self.net_income_textbox.isModified() is False \
                or self.time_frame_textbox.isModified() is False \
                or self.annual_rate_textbox.isModified() is False:
            QMessageBox.about(self, "Not all input values are filled out!",
                              "Make sure you fill out all the input values")
        else:
            QMessageBox.about(self,
                              "Placeholder until Microservice is Implemented",
                              "This button will communicate with the microservice via socket and" +
                              " receive the data to fill in:\n" +
                              "Total Principal\n" +
                              "Total Projected Interest\n" +
                              "Total Projected Value\n" +
                              "Format to send to socket:\n" +
                              "%.2f;%d;%.2f" % (self.income_minus_expenses,
                                                int(self.time_frame_textbox.text()),
                                                float(self.annual_rate_textbox.text()))
                              )


# Citation: Code to check if value is a float is from
# https://pythonhow.com/how/check-if-a-string-is-a-float/
def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def main():
    # Create and lunch the app
    app = QApplication(sys.argv)
    BICApplication = Window()
    BICApplication.show()
    sys.exit(app.exec_())


# Main Function
if __name__ == '__main__':
    main()
