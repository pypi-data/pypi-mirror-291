# coding: utf-8
from PySide2.QtCore import QEvent, QPoint, Qt
from PySide2.QtGui import QMouseEvent
from PySide2.QtWidgets import QApplication


class LinuxMoveResize:
    """ Tool class for moving and resizing window """

    @classmethod
    def startSystemMove(cls, window, globalPos):
        """ move window

        Parameters
        ----------
        window: QWidget
            window

        globalPos: QPoint
            the global point of mouse release event
        """
        window.windowHandle().startSystemMove()
        event = QMouseEvent(QEvent.MouseButtonRelease, QPoint(-1, -1),
                            Qt.LeftButton, Qt.NoButton, Qt.NoModifier)
        QApplication.instance().postEvent(window.windowHandle(), event)

    @classmethod
    def starSystemResize(cls, window, globalPos, edges):
        """ resize window

        Parameters
        ----------
        window: QWidget
            window

        globalPos: QPoint
            the global point of mouse release event

        edges: `Qt.Edges`
            window edges
        """
        if not edges:
            return

        window.windowHandle().startSystemResize(edges)
