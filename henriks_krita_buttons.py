from krita import DockWidget, DockWidgetFactory, DockWidgetFactoryBase, Document
from PyQt5.QtWidgets import *
import sys
#import pyautogui as p
from time import sleep
from threading import Thread
import os



DOCKER_NAME = 'Ryans Config'
DOCKER_ID = 'henriks_buttons'





class HenriksOnscreenKritaShortcutButtons(DockWidget):
    r = 0
    z = 0
    f = 0
    firstTime = 0



    def updateR(self):
        self.r = Krita.instance().activeDocument().currentTime()
        with open("/home/soft-dev/Desktop/beet.txt", "w") as f:
            f.write(str(self.r))

    def undo(self):
        qdock = next((w for w in Krita.instance().dockers() if w.objectName() == 'TimelineDocker'), None)
        wobj = qdock.findChild(QTableView)

        wobj.model().dataChanged.connect(self.updateR)
        x = Krita.instance().activeDocument().currentTime()
        Krita.instance().action('edit_undo').trigger()
        sleep(.1)
        self.r = Krita.instance().activeDocument().currentTime()





    def playAndpause(self):
        Krita.instance().action('toggle_playback').trigger()

    def redo(self):
        x = 0
        while x <= 7:
            if os.path.exists("/var/www/html/frame000"+str(x)+".png"):
                os.remove("/var/www/html/frame000"+str(x)+".png")
            x += 1
        Krita.instance().action('render_animation_again').trigger()

    def onionskin(self):
        Krita.instance().action('toggle_onion_skin').trigger()

    def previous_frame(self):
        if self.r > 0:
            Krita.instance().action('previous_frame').trigger()
            self.r -= 1

    def next_frame(self):
        if self.r < 7:
            Krita.instance().action('next_frame').trigger()
            self.r += 1





    def mirror_canvas(self):
        Krita.instance().action('view_toggledockers').trigger()

    def only_canvas(self):

        if self.firstTime == 0:
            if Krita.instance().action('view_show_canvas_only') == None:
                return
            Krita.instance().action('view_show_canvas_only').trigger()

            if self.f % 2 == 0:
                Krita.instance().action('view_toggledockers').trigger()
                self.f +=1

            qwin = Krita.instance().activeWindow().qwindow()
            dockers = qwin.findChildren(QDockWidget)

            for qdock in dockers:
                qdock.setFeatures(QDockWidget.NoDockWidgetFeatures)
            if self.z == 0:
                for qdock in dockers:
                    size = qdock.size()
                    if qdock.minimumSize() == qdock.maximumSize():
                        qdock.setMinimumSize(qdock.minimumSizeHint())
                        qdock.setMaximumSize(QSize(16777215, 16777215))
                    else:
                        qdock.setMinimumSize(size)
                        qdock.setMaximumSize(size)

                qwin = Krita.instance().activeWindow().qwindow()
                wobj = qwin.findChild(QMdiArea)
                wobj.setTabsClosable(False)
                self.onlyCanvasButton.hide()
                self.onlyCanvasButton.update()

                self.z = 1
                self.firstTime = 1

    def reset_canvas_rotation(self):
        Krita.instance().action('clear').trigger()

    def create_button(self, text, parentWidget, action):
        button = QPushButton(text, parentWidget)
        button.clicked.connect(action)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        return button

    def __init__(self):
        super().__init__()
        self.setWindowTitle(DOCKER_NAME)

        self.mainWidget = QWidget(self)
        self.setWidget(self.mainWidget)
        self.mainWidget.setLayout(QVBoxLayout())


        previousBrushButton = self.create_button("Preview Animation", self.mainWidget, self.playAndpause)
        self.mainWidget.layout().addWidget(previousBrushButton)

        undoButton = self.create_button("Undo Last Action", self.mainWidget, self.undo)
        self.mainWidget.layout().addWidget(undoButton)

        rotateContainer = QWidget(self)
        rotateContainer.setLayout(QHBoxLayout())

        self.mainWidget.layout().addWidget(rotateContainer)
        rotateLeftButton = self.create_button("Go Left", rotateContainer, self.previous_frame)
        rotateRightButton = self.create_button("Go Right", rotateContainer, self.next_frame)
        rotateContainer.layout().addWidget(rotateLeftButton)
        rotateContainer.layout().addWidget(rotateRightButton)

        redoButton = self.create_button("View On Screen", self.mainWidget, self.redo)
        self.mainWidget.layout().addWidget(redoButton)

        resetCanvasContainer = QWidget(self)
        resetCanvasContainer.setLayout(QHBoxLayout())
        self.mainWidget.layout().addWidget(resetCanvasContainer)

        resetZoomButton = self.create_button("See Previous Frames", self.mainWidget, self.onionskin)
        resetCanvasContainer.layout().addWidget(resetZoomButton)
        resetCanvasRotationButton = self.create_button("Clear Frame", self.mainWidget, self.reset_canvas_rotation)
        resetCanvasContainer.layout().addWidget(resetCanvasRotationButton)

        canvasContainer = QWidget(self)
        canvasContainer.setLayout(QHBoxLayout())
        self.mainWidget.layout().addWidget(canvasContainer)
        self.onlyCanvasButton = self.create_button("Only", canvasContainer, self.only_canvas)
        canvasContainer.layout().addWidget(self.onlyCanvasButton)





    def canvasChanged(self, canvas):
        self.only_canvas()



instance = Krita.instance()
dock_widget_factory = DockWidgetFactory(DOCKER_ID,
                                        DockWidgetFactoryBase.DockLeft,
                                        HenriksOnscreenKritaShortcutButtons)

instance.addDockWidgetFactory(dock_widget_factory)

