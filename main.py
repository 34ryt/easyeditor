#создай тут фоторедактор Easy Editor!
# импорт модулей
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QButtonGroup, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QGroupBox, QTextEdit, QListWidget, QLineEdit, QInputDialog, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PIL import Image, ImageOps, ImageEnhance
import os
# классы
class ImageProcessor():
    def __init__(self):
        self.image = None
        self.name = None
        self.savedir = 'changed'
        self.orig = None
    def load_image(self, filename):
        self.name = filename
        file_path = os.path.join(workdir, self.name)
        self.image = Image.open(file_path)
    def show_image(self, path):
        choosen_image.hide()
        pixmapimage = QPixmap(path)
        w, h = choosen_image.width(), choosen_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        choosen_image.setPixmap(pixmapimage)
        choosen_image.show()
    def do_bw(self):
        self.image = ImageOps.grayscale(self.image)
        self.save_image()
        image_path = os.path.join(workdir, self.savedir, self.name)
        self.show_image(image_path)
    def do_left(self):
        self.image = self.image.rotate(90)
        self.save_image()
        image_path = os.path.join(workdir, self.savedir, self.name)
        self.show_image(image_path)
    def do_right(self):
        self.image = self.image.rotate(-90)
        self.save_image()
        image_path = os.path.join(workdir, self.savedir, self.name)
        self.show_image(image_path)
    def do_mirror(self):
        self.image = ImageOps.mirror(self.image)
        self.save_image()
        image_path = os.path.join(workdir, self.savedir, self.name)
        self.show_image(image_path)
    def do_jpeg(self):
        self.image = ImageEnhance.Contrast(self.image)
        self.image = self.image.enhance(1.5)
        self.save_image()
        image_path = os.path.join(workdir, self.savedir, self.name)
        self.show_image(image_path)
    def save_image(self):
        folder_path = os.path.join(workdir, self.savedir)
        if not(os.path.exists(folder_path) or os.path.isdir(folder_path)):
            os.mkdir(folder_path)
        image_path = os.path.join(folder_path, self.name)
        self.image.save(image_path)
    def reset(self):
        self.image = self.orig
        self.save_image()
        image_path = os.path.join(workdir, self.savedir, self.name)
        self.show_image(image_path)
workimage = ImageProcessor()
# САМАЯ ВАЖНАЯ ПЕРЕМЕННАЯ!!!
workdir = ''
def chooseWorkDir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()
# функции
def filter(files, extensions):
    result = []
    for filename in files:
        for extension in extensions:
            if filename.endswith(extension):
                result.append(filename)
    return result
def showFilenameList():
    chooseWorkDir()
    extensions = ['png', 'jpg', 'bmp', 'jpeg', 'gif']
    try:
        files = os.listdir(workdir)
        result = filter(files, extensions)
        file_list.clear()
        for f in result:
            file_list.addItem(f)
    except:
        error_nofound = QMessageBox()
        error_nofound.setText('Вы не выбрали ни одно изображение!')
        error_nofound.exec_()
def showChoosenImage():
    if file_list.currentRow() >= 0:
        filename = file_list.currentItem().text()
        workimage.load_image(filename)
        image_path = os.path.join(workdir, workimage.name)
        workimage.show_image(image_path)
# генератор Qt
app = QApplication([])
main_win = QWidget()
main_win.setWindowTitle('Редактор изображений')
main_win.resize(700, 400)
# виджеты
btn_dir = QPushButton('Папка')
file_list = QListWidget()
choosen_image = QLabel('Картинка')
left_btn = QPushButton('Повернуть налево')
right_btn = QPushButton('Повернуть направо')
mirror_btn = QPushButton('Отзеркалить')
contrast_btn = QPushButton('Контраст')
do_bw_btn = QPushButton('Чёрно-Белое')
save_btn = QPushButton('Сохранить')
reset_btn = QPushButton('Сброс')
# лэйаут
row = QHBoxLayout()
col1 = QVBoxLayout()
manipulate_lay = QHBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(file_list)
manipulate_lay.addWidget(left_btn)
manipulate_lay.addWidget(right_btn)
manipulate_lay.addWidget(mirror_btn)
manipulate_lay.addWidget(contrast_btn)
manipulate_lay.addWidget(do_bw_btn)
manipulate_lay.addWidget(save_btn)
manipulate_lay.addWidget(reset_btn)
col2.addWidget(choosen_image, 95)
col2.addLayout(manipulate_lay)
row.addLayout(col1, 20)
row.addLayout(col2, 80)
# действия
btn_dir.clicked.connect(showFilenameList)
file_list.currentRowChanged.connect(showChoosenImage)
do_bw_btn.clicked.connect(workimage.do_bw)
left_btn.clicked.connect(workimage.do_left)
right_btn.clicked.connect(workimage.do_right)
mirror_btn.clicked.connect(workimage.do_mirror)
contrast_btn.clicked.connect(workimage.do_jpeg)
save_btn.clicked.connect(workimage.save_image)
reset_btn.clicked.connect(workimage.reset)
# запуск
main_win.setLayout(row)
main_win.show()
app.exec_()