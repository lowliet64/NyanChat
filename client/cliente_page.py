import sys
import random
import asyncio
from PySide2 import QtCore, QtWidgets, QtGui


class MyWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        """Setting widgets to add a layout"""
        self.send_button = QtWidgets.QPushButton("Send")
        self.button = QtWidgets.QPushButton("Click me!")
        self.input = QtWidgets.QTextEdit()
        self.text = QtWidgets.QLabel("Nyan chat")
        self.text.setAlignment(QtCore.Qt.AlignCenter)

        """Setting a layout with widgets"""
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.send_button)
        self.layout.addWidget(self.input)
        self.setLayout(self.layout)

        """setting evetns to button"""
        self.send_button.clicked.connect(self.send_message)

    def send_message(self):
        print(self.input.toPlainText())

    async def listen_tcp(parameter_list):
        print('Hello ...')
        await asyncio.sleep(1)
        print('Hello...')


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    widget = MyWidget()
    widget.resize(800, 600)
    widget.show()
    asyncio.run(widget.listen_tcp())
    sys.exit(app.exec_())
