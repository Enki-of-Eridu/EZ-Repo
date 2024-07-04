import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QVBoxLayout, QWidget, QToolBar, QAction, QStyle, QSizePolicy, QLabel, QDialog, QDialogButtonBox
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
import subprocess
import os

class RepoDialog(QDialog):
    def __init__(self, parent=None):
        super(RepoDialog, self).__init__(parent)

        self.setWindowTitle("Enter Repo Address")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout()

        self.repo_entry = QLineEdit()
        layout.addWidget(self.repo_entry)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("Git Repo Setup")
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QVBoxLayout()

        make_repo_button = QPushButton("Make Repo")
        make_repo_button.setFont(QFont('Arial', 12))
        make_repo_button.clicked.connect(self.make_repo)
        layout.addWidget(make_repo_button)

        self.link_and_push_button = QPushButton("Repo?")
        self.link_and_push_button.clicked.connect(self.link_and_push)
        layout.addWidget(self.link_and_push_button)

        self.ready_label = QLabel()
        layout.addWidget(self.ready_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.create_toolbar()

    def make_repo(self):
        print("Command: git init")
        print("Command: git add .")
        print('Command: git commit -m "Initial Commit"')

    def link_and_push(self):
        if not hasattr(self, 'repo_url'):
            dialog = RepoDialog(self)
            if dialog.exec_():
                self.repo_url = dialog.repo_entry.text()
                self.ready_label.setText("READY")
                self.ready_label.setStyleSheet("color: lime;")
                self.link_and_push_button.setText("Link & Push")
        else:
            print(f"Command: git remote add origin {self.repo_url}.git")
            print("Command: git push -u origin main")

    def create_toolbar(self):
        toolbar = QToolBar()
        toolbar.setMovable(False)
        toolbar.setIconSize(self.style().standardIcon(QStyle.SP_TitleBarCloseButton).actualSize(24))
        toolbar.setStyleSheet("background-color: #2f2f2f; color: white;")

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        toolbar.addWidget(spacer)

        minimize_action = QAction(QIcon(self.style().standardIcon(QStyle.SP_TitleBarMinButton)), "Minimize", self)
        minimize_action.triggered.connect(self.showMinimized)
        toolbar.addAction(minimize_action)

        close_action = QAction(QIcon(self.style().standardIcon(QStyle.SP_TitleBarCloseButton)), "Close", self)
        close_action.triggered.connect(self.close)
        toolbar.addAction(close_action)

        self.addToolBar(Qt.TopToolBarArea, toolbar)

app = QApplication(sys.argv)
app.setStyleSheet("QMainWindow {background-color: #2f2f2f; color: white;} QPushButton {color: white; background-color: #3f3f3f;} QLineEdit {color: white; background-color: #3f3f3f;}")
window = MainWindow()
window.show()
sys.exit(app.exec_())
