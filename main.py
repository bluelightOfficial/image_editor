#create the Easy Editor photo editor here!
from PyQt5.QtWidgets import (
   QApplication, QWidget, QPushButton, QListWidget,
     QHBoxLayout, QVBoxLayout, QLabel, QFileDialog,
     QMessageBox
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import os
from PIL import Image, ImageFilter
from PIL.ImageFilter import SHARPEN

app = QApplication([])
win = QWidget()      
win.resize(700, 500)
win.setWindowTitle('Easy Editor')

row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
rowOfButtons = QHBoxLayout()

folderButton = QPushButton('Folder')
leftBtn = QPushButton('Left')
rightBtn = QPushButton('Right')
mirrorBtn = QPushButton('Mirror')
sharpnessBtn = QPushButton('Sharpness')
BNWBtn = QPushButton('B&W')
imgList = QListWidget()
imgLabel = QLabel('image')

BtnList = [folderButton, leftBtn, rightBtn, mirrorBtn, sharpnessBtn, BNWBtn, ]

for i in BtnList:
    i.setStyleSheet("""
        QPushButton {
            background-color: #009dff;
            color: white;
            padding: 5px 20px;
            border-radius: 10px;
            font-size: 15px;
        }
        QPushButton:hover {
            background-color: #1f83c2;
        }
    """)

rowOfButtons.addWidget(leftBtn)
rowOfButtons.addWidget(rightBtn)
rowOfButtons.addWidget(mirrorBtn)
rowOfButtons.addWidget(sharpnessBtn)
rowOfButtons.addWidget(BNWBtn)

col1.addWidget(folderButton)
col1.addWidget(imgList)

col2.addWidget(imgLabel)
col2.addLayout(rowOfButtons)

row.addLayout(col1, 20)
row.addLayout(col2, 80)

win.setLayout(row)

def Chooseworkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

def showfilenamelist():
    Chooseworkdir()
    try:
        filenames = filter(os.listdir(workdir))
        imgList.clear()
        for filename in filenames:
            imgList.addItem(filename)
    except:
        errorImageInput2()

def errorImageInput():
        inpmsgbox = QMessageBox()
        inpmsgbox.setWindowTitle('error! 404')
        inpmsgbox.setText('the image input is empty.')
        inpmsgbox.setStandardButtons(QMessageBox.Ok)
        inpmsgbox.exec_()

def errorImageInput2():
        inpmsgbox = QMessageBox()
        inpmsgbox.setWindowTitle('error! 404')
        inpmsgbox.setText('the path input is empty.')
        inpmsgbox.setStandardButtons(QMessageBox.Ok)
        inpmsgbox.exec_()



class ImageProcessor():
    def __init__(self):
        self.image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"

    def loadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        path = os.path.join(self.dir, self.filename)
        self.image = Image.open(path)
    
    def showImage(self, path):
        imgLabel.hide()
        pixmapimage = QPixmap(path)
        w, h = imgLabel.width(), imgLabel.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        imgLabel.setPixmap(pixmapimage)
        imgLabel.show()
    
    def do_bw(self):
        try:
            self.image = self.image.convert('L')
            self.saveImage()
            image_path = os.path.join(workdir, self.save_dir, self.filename)
            self.showImage(image_path)
        except:
            errorImageInput()
    
    def saveImage(self):
        path = os.path.join(workdir, self.save_dir)
        if not(os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def do_flip(self):
        try:
            self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
            self.saveImage()
            image_path = os.path.join(workdir, self.save_dir, self.filename)
            self.showImage(image_path)
        except:
            errorImageInput()
    
    def do_left(self):
        try:
            self.image = self.image.transpose(Image.ROTATE_90)
            self.saveImage()
            image_path = os.path.join(workdir, self.save_dir, self.filename)
            self.showImage(image_path)
        except:
            errorImageInput()
    
    def do_right(self):
        try:
            self.image = self.image.transpose(Image.ROTATE_270)
            self.saveImage()
            image_path = os.path.join(workdir, self.save_dir, self.filename)
            self.showImage(image_path)
        except:
            errorImageInput()

    def do_sharp(self):
        try:
            self.image = self.image.filter(SHARPEN)
            self.saveImage()
            image_path = os.path.join(workdir, self.save_dir, self.filename)
            self.showImage(image_path)
        except:
           errorImageInput()


workimage = ImageProcessor()

def showChosenImage():
    if imgList.currentRow() >= 0:
        filename = imgList.currentItem().text()
        workimage.loadImage(workdir, filename)
        image_path = os.path.join(workimage.dir, workimage.filename)
        workimage.showImage(image_path)


def filter(files):
    result = []
    extenstions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
    for filename in files:
        for ext in extenstions:
            if filename.endswith(ext):
                result.append(filename)
    return result

folderButton.clicked.connect(showfilenamelist)
imgList.currentRowChanged.connect(showChosenImage)
BNWBtn.clicked.connect(workimage.do_bw)
mirrorBtn.clicked.connect(workimage.do_flip)
leftBtn.clicked.connect(workimage.do_left)
rightBtn.clicked.connect(workimage.do_right)
sharpnessBtn.clicked.connect(workimage.do_sharp)


win.show()
app.exec()

