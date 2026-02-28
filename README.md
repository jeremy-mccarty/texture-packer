[![Python](https://img.shields.io/badge/python-3.12-blue)](https://www.python.org/)
[![Latest Release](https://img.shields.io/github/v/release/<username>/texture-packer?logo=github&label=Release&color=blue)](https://github.com/<username>/texture-packer/releases/latest)
[![CI/CD](https://github.com/<username>/texture-packer/actions/workflows/build.yml/badge.svg)](https://github.com/<username>/texture-packer/actions/workflows/build.yml)

## Downloads

[![Download Linux](https://img.shields.io/badge/Download-Linux-blue?logo=linux)](https://github.com/<username>/texture-packer/releases/latest)
[![Download Windows](https://img.shields.io/badge/Download-Windows-brightgreen?logo=windows)](https://github.com/<username>/texture-packer/releases/latest)
[![Download macOS](https://img.shields.io/badge/Download-macOS-lightgrey?logo=apple)](https://github.com/<username>/texture-packer/releases/latest)

Pack and unpack RGBA texture channels easily across Linux, Windows, and macOS.

# Texture Packer

A simple Python application to **pack and unpack RGBA texture channels**, built with `Tkinter` and `Pillow`.

This tool allows you to:

- Split an RGBA texture into individual R, G, B, and A grayscale images.
- Merge four grayscale images into a single RGBA texture.
- Quickly prepare textures for game engines and rendering pipelines.

---

## Features

* Split RGBA images into individual channel images.
* Merge R, G, B, and A grayscale images into a single RGBA texture.
* Automatic channel filename generation.
* Image dimension validation before packing.
* Output log with timestamps.
* Clean and responsive Tkinter UI.
* Works on Windows, Linux, and macOS.

---

## Using the Executable

- Download the latest release for your OS from the [Releases page](https://github.com/<username>/texture-packer/releases).  
- Run the executable — no Python installation required.

---

## Usage

### Unpacking Channels

1. Click **Select Input Path** under *Unpack Input*.
2. Review or adjust the generated channel filenames.
3. Click **Unpack**.
4. The R, G, B, and A channel images will be saved individually.

### Packing Channels

1. Select the R, G, B, and A grayscale images.
2. Enter a name for the output RGBA texture.
3. Click **Pack**.
4. The merged texture will be saved as a `.png`.

Check the **Output Log** for status messages and errors.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/<username>/texture-packer.git
cd texture-packer
```

2. Create a Python virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

Linux/macOS:
```bash
source venv/bin/activate
```

Windows (PowerShell):
```bash
.\venv\Scripts\Activate.ps1
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the App

With the virtual environment active:

```bash
python app/main.py
```

---

## Building Executables

You can create a standalone executable using PyInstaller:

```bash
pyinstaller --noconfirm --onefile --name TexturePacker app/main.py
```

The executable will be located in the `dist` folder.

---

## GitHub Actions Auto-Build

Whenever a tag like `v1.0.0` is pushed, GitHub Actions will:

1. Build standalone executables for Windows, macOS, and Linux.  
2. Upload them as artifacts.  
3. Create a GitHub release with the executables attached.  

The badge above reflects the **latest workflow status**.

---

## Release Guide

Push a version tag:

```bash
git tag v1.0.0
git push origin v1.0.0
```

GitHub Actions will automatically:

* Build executables for all supported OSes.
* Upload artifacts to a GitHub release.
* Generate release notes automatically.

---

## License

MIT License — see the LICENSE file for details.
