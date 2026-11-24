"""
Simple CAD viewer (STEP / IGES / STL / BREP)
Based on pythonocc-core (Open CASCADE) with a Qt window.

Mouse:
  Left drag          = rotate
  Middle drag        = pan (move)
  Right drag / wheel = zoom
  Shift + right drag = zoom to a box
  Left click         = select a part (info printed in console)
Keys:
  F = fit all, W = wireframe, S = shaded, H = hidden lines
"""

import os
import sys

from OCC.Display.SimpleGui import init_display
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.TopAbs import TopAbs_FACE, TopAbs_EDGE
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Extend.DataExchange import (
    read_step_file_with_names_colors,
    read_iges_file,
    read_stl_file,
)
from OCC.Core.BRepTools import breptools
from OCC.Core.BRep import BRep_Builder
from OCC.Core.TopoDS import TopoDS_Shape

# ---------- Start the 3D window ----------
display, start_display, add_menu, add_function_to_menu = init_display(
    "pyqt5", size=(1280, 800)
)

from PyQt5 import QtWidgets  # file dialog and message boxes

display.set_bg_gradient_color([230, 235, 240], [150, 160, 170])
display.display_triedron()  # small XYZ axis in the corner

DEFAULT_COLOR = Quantity_Color(0.7, 0.7, 0.75, Quantity_TOC_RGB)


# ---------- File loading ----------
def load_brep(path):
    shape = TopoDS_Shape()
    breptools.Read(shape, path, BRep_Builder())
    return shape


def count(shape, kind):
    exp, n = TopExp_Explorer(shape, kind), 0
    while exp.More():
        n += 1
        exp.Next()
    return n


def open_file(path):
    ext = os.path.splitext(path)[1].lower()
    display.EraseAll()

    try:
        if ext in (".step", ".stp"):
            shapes = read_step_file_with_names_colors(path)  # keeps colors
            for shp, (name, color) in shapes.items():
                display.DisplayShape(shp, color=color or DEFAULT_COLOR,
                                     update=False)
        elif ext in (".iges", ".igs"):
            for shp in read_iges_file(path, return_as_shapes=True):
                display.DisplayShape(shp, color=DEFAULT_COLOR, update=False)
        elif ext == ".stl":
            display.DisplayShape(read_stl_file(path), color=DEFAULT_COLOR,
                                 update=False)
        elif ext == ".brep":
            display.DisplayShape(load_brep(path), color=DEFAULT_COLOR,
                                 update=False)
        else:
            QtWidgets.QMessageBox.warning(None, "Not supported",
                                          f"File type {ext} is not supported.")
            return
    except Exception as e:
        QtWidgets.QMessageBox.critical(None, "Error", f"Could not open file:\n{e}")
        return

    display.View_Iso()
    display.FitAll()
    display.Repaint()
    print(f"Loaded: {path}")


def menu_open(event=None):
    path, _ = QtWidgets.QFileDialog.getOpenFileName(
        None, "Open CAD file", "",
        "CAD files (*.step *.stp *.iges *.igs *.stl *.brep);;All files (*)"
    )
    if path:
        open_file(path)


# ---------- View commands ----------
def fit_all(event=None):      display.FitAll()
def view_iso(event=None):     display.View_Iso();    display.FitAll()
def view_front(event=None):   display.View_Front();  display.FitAll()
def view_back(event=None):    display.View_Rear();   display.FitAll()
def view_top(event=None):     display.View_Top();    display.FitAll()
def view_bottom(event=None):  display.View_Bottom(); display.FitAll()
def view_left(event=None):    display.View_Left();   display.FitAll()
def view_right(event=None):   display.View_Right();  display.FitAll()
def shaded(event=None):       display.SetModeShaded()
def wireframe(event=None):    display.SetModeWireFrame()
def hidden_lines(event=None): display.SetModeHLR()
def clear(event=None):        display.EraseAll()


# ---------- Click a part to see info ----------
def on_select(shapes, *args):
    for s in shapes:
        print(f"Selected shape: "
              f"{count(s, TopAbs_FACE)} faces, {count(s, TopAbs_EDGE)} edges")

display.register_select_callback(on_select)


# ---------- Menus ----------
add_menu("File")
add_function_to_menu("File", menu_open)
add_function_to_menu("File", clear)

add_menu("View")
for f in (fit_all, view_iso, view_front, view_back,
          view_top, view_bottom, view_left, view_right):
    add_function_to_menu("View", f)

add_menu("Display")
for f in (shaded, wireframe, hidden_lines):
    add_function_to_menu("Display", f)


# ---------- Run ----------
if __name__ == "__main__":
    if len(sys.argv) > 1:          # python local_cad_viewer.py part.step
        open_file(sys.argv[1])
    else:
        menu_open()                # otherwise ask for a file at start
    start_display()
