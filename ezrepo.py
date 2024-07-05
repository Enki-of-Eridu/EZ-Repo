import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QCheckBox, QPushButton, QLineEdit, QVBoxLayout, QWidget, QToolBar, QStyle, QSizePolicy, QLabel, QDialog, QDialogButtonBox
from PyQt6.QtGui import QIcon, QFont, QAction, QPalette
from PyQt6.QtCore import Qt, QSize, QPoint
import subprocess
import os

class RepoDialog(QDialog):
    def __init__(self, parent=None):
        super(RepoDialog, self).__init__(parent)
        self.oldPos = self.pos()
        print("RepoDialog is initialized")                          # Debugging print statement
        self.setStyleSheet("""RepoDialog{border: 3px solid #3f3f3f;}""")

        self.setWindowTitle("Enter Repo Address")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        layout = QVBoxLayout()

        self.repo_entry = QLineEdit()
        layout.addWidget(self.repo_entry)

        self.verify_checkbox = QCheckBox("Verify URL")
        layout.addWidget(self.verify_checkbox)

        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.verify_url)
        layout.addWidget(button_box)

        self.setLayout(layout)

    def verify_url(self):
        if self.verify_checkbox.isChecked():
            url = self.repo_entry.text()
            try:
                subprocess.check_output(['git', 'ls-remote', url], stderr=subprocess.STDOUT)
            except subprocess.CalledProcessError:
                error_dialog = QMessageBox()
                error_dialog.setWindowTitle("Error")
                error_dialog.setText("Invalid URL!")
                error_dialog.setIcon(QMessageBox.Icon.Warning)
                error_dialog.exec()
                return
        self.accept()
            
    def mousePressEvent(self, event):
        self.oldPos = event.globalPosition()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPosition().toPoint() - self.oldPos.toPoint())
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.oldPos = self.pos()

        self.setWindowTitle("Git Repo Setup")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet("""QMainWindow {border: 8px solid #3f3f3f;}""")
  #      self.resize(200, 200)

        layout = QVBoxLayout()

        make_repo_button = QPushButton("Make Repo")
        make_repo_button.setFont(QFont('Arial', 12))
        make_repo_button.clicked.connect(self.make_repo)
        layout.addWidget(make_repo_button)

        self.repo_button = QPushButton("Repo?")
        self.repo_button.setFont(QFont('Arial', 12))
        self.repo_button.clicked.connect(self.set_repo)
        layout.addWidget(self.repo_button)

        self.link_and_push_button = QPushButton("Link and Push")
        self.link_and_push_button.clicked.connect(self.prepare_link_and_push)
        layout.addWidget(self.link_and_push_button)

        self.pull_button = QPushButton("Pull")
        self.pull_button.setFont(QFont('Arial', 12))
        self.pull_button.clicked.connect(self.prepare_pull)
        layout.addWidget(self.pull_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.create_toolbar()

    def pullz(self):
        print("Command: git pull")
        self.pull_button.setStyleSheet("")
        self.pull_button.clicked.disconnect
        self.pull_button.clicked.connect(self.pullz)

    def prepare_pull(self):
        self.pull_button.setStyleSheet("background-color: lime; color: red; font-weight: bold;")
        self.pull_button.clicked.disconnect
        self.pull_button.clicked.connect(self.pullz)
        

    def make_repo(self):
        print("Command: git init")
        print("Command: git add .")
        print('Command: git commit -m "Initial Commit"')

    def set_repo(self):
            print("Repo button clicked")                    # Debugging print statement
            dialog = RepoDialog()
            if dialog.exec() == QDialog.DialogCode.Accepted:
                self.repo_url = dialog.repo_entry.text()
                if not self.repo_url.endswith('.git'):
                    self.repo_url += '.git'
                self.repo_button.setText(self.repo_url)
            print(self.repo_url)                                 # Debugging print statement

    def prepare_link_and_push(self):
        if hasattr(self, 'repo_url'):
            self.link_and_push_button.clicked.disconnect()
            self.link_and_push_button.clicked.connect(self.link_and_push)    # why do i have to click this 3x the first run
        else:
            error_dialog = QMessageBox()
            error_dialog.setWindowTitle("Error")
            error_dialog.setText("No remote repository set!")
            error_dialog.setIcon(QMessageBox.Icon.Warning)
            error_dialog.exec()

    def link_and_push(self):
        if hasattr(self, 'repo_url'):
            self.link_and_push_button.setStyleSheet("background-color: #BFFF00; color: #000000; font-weight: bold;")
            self.link_and_push_button.clicked.disconnect()
            self.link_and_push_button.clicked.connect(self.execute_commands)


    def execute_commands(self):
        print(f"Command: git remote add origin {self.repo_url}")
        print("Command: git push -u origin main")
        self.link_and_push_button.setStyleSheet("")
        self.link_and_push_button.clicked.disconnect()
        self.link_and_push_button.clicked.connect(self.link_and_push)

    def create_toolbar(self):
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setIconSize(QSize(24, 24))
        toolbar.setStyleSheet("background-color: #2f2f2f; color: white;")

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        toolbar.addWidget(spacer)

        minimize_action = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarMinButton)), "Minimize", self)
        minimize_action.triggered.connect(self.showMinimized)
        toolbar.addAction(minimize_action)

        close_action = QAction(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarCloseButton)), "Close", self)
        close_action.triggered.connect(self.close)
        toolbar.addAction(close_action)

        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        # movable with mouse

    def mousePressEvent(self, event):
        self.oldPos = event.globalPosition()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPosition().toPoint() - self.oldPos.toPoint())
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPosition()
        


app = QApplication(sys.argv)
app.setStyleSheet("QMainWindow {background-color: #2f2f2f; color: white;} QPushButton {color: white; background-color: #3f3f3f;} QLineEdit {color: white; background-color: #3f3f3f;}")
window = MainWindow()
window.show()
sys.exit(app.exec())
