# Local CAD Viewer

A small desktop app for opening and viewing CAD files on your computer.

## Install

Use Python, then install the required libraries:

```powershell
python -m pip install pythonocc-core PyQt5
```

## Run

From this folder, run:

```powershell
python local_cad_viewer.py
```

Choose a file in the window that opens. You can also open a file directly:

```powershell
python local_cad_viewer.py "C:\path\to\part.step"
```

## Supported files

STEP (`.step`, `.stp`), IGES (`.iges`, `.igs`), STL (`.stl`), and Open CASCADE BREP (`.brep`).

## Privacy

This is a local desktop viewer. It opens the selected model on your computer and does not upload it to a website.
