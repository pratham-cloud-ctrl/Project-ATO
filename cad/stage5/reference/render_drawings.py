"""Render reference-specific vector drawings using Qt's actual SVG renderer."""
import os
os.environ['QT_QPA_PLATFORM']='offscreen'
from pathlib import Path
from PySide6 import QtCore,QtGui,QtSvg
app=QtGui.QGuiApplication([])
for filename in ['arial.ttf','arialbd.ttf']:
    assert QtGui.QFontDatabase.addApplicationFont(str(Path('C:/Windows/Fonts')/filename))>=0
HERE=Path(__file__).resolve().parent
for p in (HERE/'drawings').glob('*.svg'):
    renderer=QtSvg.QSvgRenderer(str(p));assert renderer.isValid(),p
    image=QtGui.QImage(1191,842,QtGui.QImage.Format_ARGB32);image.fill(QtCore.Qt.white)
    painter=QtGui.QPainter(image);renderer.render(painter);painter.end()
    assert image.save(str(p.with_suffix('.png'))),p
print('Rendered9actual SVG drawing sheets')
