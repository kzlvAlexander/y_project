import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Window(QMainWindow):
    def __init__(self):
        super().__init__()


        self.setWindowTitle("PyPaint")
        self.resize(1920,1080)

        self.image = QImage(self.size(), QImage.Format_RGB32)
        self.image.fill(Qt.white)

        self.drawing = False
        self.brushSize = 2
        self.brushColor = Qt.black

        self.lastPoint = QPoint()

        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        BrushNColor = mainMenu.addMenu("Color and size")

        saveAction = QAction("Save", self)
        saveAction.setShortcut("Ctrl+S")
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save)

        clearAction = QAction("Clear", self)
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.clear)

        BrushSizeSelectAction = QAction("Select brush size", self)
        BrushNColor.addAction(BrushSizeSelectAction)
        BrushSizeSelectAction.triggered.connect(self.BrushSizeSelect)

        ColorSelectAction = QAction("Select color", self)
        BrushNColor.addAction(ColorSelectAction)
        ColorSelectAction.triggered.connect(self.ColorSelect)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvasPainter = QPainter(self)
        canvasPainter.drawImage(self.rect(), self.image, self.image.rect())

    def save(self):
        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "",
                                                  "PNG(*.png);;JPEG(*.jpg *.jpeg)")
        if filePath == "":
            return
        self.image.save(filePath)

    def clear(self):
        self.image.fill(Qt.white)
        self.update()

    def keyPressEvent(self, event):
        if (event.key() == Qt.Key_Control) and (event.key() == Qt.Key_S):
            save()

    def BrushSizeSelect(self):
        i, size = QInputDialog.getDouble(self, "Brush size select","Brush size in px:",2)
        if(size):
            self.brushSize = i

    def ColorSelect(self):
        color = QColorDialog.getColor()
        if(color.isValid()):
            self.brushColor = color
        else:
            pass


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec()
