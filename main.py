import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QLabel, QGridLayout, \
    QDesktopWidget
from PyQt5.QtGui import QIcon, QPixmap
import logic

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Jpeg decoder'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon('icon.jpg'))
        grid = QGridLayout()
        grid.setHorizontalSpacing(2)
        grid.setVerticalSpacing(7)

        self.open_filename_dialog()
        if self.filename:
            pixmap = QPixmap(self.filename)
            image = QLabel(self)
            image.setPixmap(pixmap)
            image_label = QLabel('Image:')
            grid.addWidget(image_label, 0, 0)
            grid.addWidget(image, 0, 1)
            raw_number = 1
            image_sectors = logic.parse(self.filename)
            for key, value in image_sectors.items():
                grid.addWidget(QLabel(key),raw_number,0)
                grid.addWidget(QLabel((value).hex()),raw_number,1)
                raw_number+=1
            self.setLayout(grid)
            self.center()
            self.show()

    def open_filename_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fname, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;JPEG (*.jpg)", options=options)
        self.filename = fname


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())