import re
import sys
import requests
import datetime
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc


class MainWindow(qtw.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Define window attributes
        self.title = "Nasa Image Archive Viewer"
        self.width = 650
        self.height = 500
        self.left = 200
        self.top = 200
        self.icon = qtg.QIcon("rocket.png")
        self.initUI()
        self.item_num = 0
        self.image_data = ""
        self.data = ""
        self.r = ""

    # FUNCTIONS
    def searched(self):
        # Vars
        now = datetime.datetime.now()
        search_term = self.search_terms.text()
        base_url = "https://images-api.nasa.gov/search"
        payload = {"q": search_term, "media_type": "image", "year_start": now.year}

        self.r = requests.get(base_url, params=payload)
        self.updateImage(self)

    def forward(self):
        self.item_num += 1
        self.updateImage(self.item_num)
        self.back_button.setEnabled(True)

    def backward(self, item_num):
        if self.item_num == 1:
            self.back_button.setEnabled(False)

        self.item_num -= 1
        self.updateImage(self.item_num)

    def updateImage(self, item_num):
        self.data = self.r.json()
        desc = self.data["collection"]["items"][self.item_num]["data"][0]["description"]
        # Grab the small version of the image
        thumb = self.data["collection"]["items"][self.item_num]["links"][0]["href"]

        # Display the desc and strip urls
        urlReg = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
        desc = re.sub(urlReg, "", desc)
        self.descbox.setText(desc)

        self.image_data = requests.get(thumb).content
        self.pixmap.loadFromData(self.image_data)

        self.image_view.setPixmap(self.pixmap)

    def initUI(self):

        # Search terms
        self.search_terms_label = qtw.QLabel(
            "What pictures are you looking for? (eg. Earth):"
        )
        # search_terms_label.setStyleSheet("background-color:red")
        self.search_terms_label.setAlignment(qtc.Qt.AlignCenter)
        self.search_terms = qtw.QLineEdit()

        # Search Button
        self.search_button = qtw.QPushButton("SEARCH")
        self.search_button.clicked.connect(self.searched)
        # self.search_button.setMaximumWidth(150)

        # Image view area
        self.image_view = qtw.QLabel()
        self.pixmap = qtg.QPixmap()
        self.resize(300, 300)
        # Imageview styles
        self.image_view.setStyleSheet("background-color:black")
        self.image_view.setAlignment(qtc.Qt.AlignCenter)

        # Description box
        self.descbox_title = qtw.QLabel("Description")
        self.descbox_title.setAlignment(qtc.Qt.AlignCenter)

        self.descbox = qtw.QLabel()
        self.descbox.resize(self.pixmap.width(), 500)
        self.descbox.setWordWrap(True)
        self.descbox.setStyleSheet("background-color:white")

        # Back Button
        self.back_button = qtw.QPushButton("BACK")
        self.back_button.clicked.connect(self.backward)

        # Make button disabled at the start
        self.back_button.setEnabled(False)

        # Forward Button
        self.forward_button = qtw.QPushButton("FORWARD")
        self.forward_button.clicked.connect(self.forward)

        # Search add
        search_area = qtw.QHBoxLayout()
        search_area.addWidget(self.search_terms)
        search_area.addWidget(self.search_button)
        search_area.setAlignment(qtc.Qt.AlignCenter)

        # Forward and back buttons
        nav_buttons = qtw.QHBoxLayout()
        nav_buttons.addWidget(self.back_button)
        nav_buttons.addWidget(self.forward_button)
        nav_buttons.setAlignment(qtc.Qt.AlignCenter)

        # Alt layout
        main_layout = qtw.QVBoxLayout()
        main_layout.addWidget(self.search_terms_label)
        main_layout.addLayout(search_area)
        main_layout.addWidget(self.image_view)
        main_layout.addWidget(self.descbox_title)
        main_layout.addWidget(self.descbox)
        main_layout.addLayout(nav_buttons)

        # Set window attributes
        self.setLayout(main_layout)

        self.setWindowTitle(self.title)
        self.setWindowIcon(self.icon)
        self.setGeometry(self.left, self.top, self.height, self.width)

        # Show the window
        self.show()


if __name__ == "__main__":
    app = qtw.QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())
