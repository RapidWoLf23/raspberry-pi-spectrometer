# Raspberry Pi Spectrometer

A low-cost Raspberry Pi optical spectrometer that captures a dispersed light spectrum with a camera, converts the camera position into wavelength, calculates frequency, classifies visible colors, and exports the measured spectrum to CSV.

> **Note:** This repository is a clean reconstruction of the software architecture represented by the project screenshots. It is intended as a portfolio-ready implementation; it is not claimed to be the original source code from the project.

## Project overview

The physical instrument uses:

- Raspberry Pi
- Raspberry Pi Camera / compatible camera
- Diffraction-grating spectroscope
- Homemade optical enclosure/tube
- Ribbon cable between camera and Raspberry Pi
- Python desktop GUI

The software provides four main operations:

1. **Capture** – acquire a frame from the camera.
2. **Analyze** – convert the horizontal spectrum into wavelength/intensity/frequency data.
3. **Calibrate** – set the blue and red reference wavelengths.
4. **Export** – save the spectrum as CSV.

The overall approach is consistent with established Raspberry Pi spectrometer projects, where a camera views a diffraction-grating spectrum and calibration maps camera position to wavelength. Multi-point calibration can improve accuracy further. citeturn0search0turn0search1

## Hardware

The enclosure and optical arrangement in this project are visible in:

![Hardware front](docs/images/hardware-front.jpg)

![Hardware rear](docs/images/hardware-rear.jpg)

![Hardware close-up](docs/images/hardware-closeup.jpg)

The camera is positioned so that the spectrum is spread horizontally across the sensor. The physical alignment matters: the spectrum should be focused and stable before taking measurements. Similar Raspberry Pi spectrometer builds use a Pi camera looking down the barrel of a diffraction spectroscope. citeturn0search2

## Software screenshots

### Spectrum analysis

![Blue spectrum](docs/images/gui-spectrum-blue.jpg)

![Green/yellow spectrum](docs/images/gui-spectrum-green.jpg)

The application displays:

- Wavelength in nm
- Relative intensity in %
- Frequency in THz
- Approximate visible-light color

### Calibration

![Calibration window](docs/images/calibration-window.jpg)

The calibration screen lets the user enter the known blue and red reference wavelengths.

The included default values are:

- Blue: **450 nm**
- Red: **650 nm**

For a more scientifically accurate instrument, use known emission lines or multiple calibration wavelengths rather than relying only on two endpoints. Existing open-source spectrometer projects recommend using reference wavelengths that are well separated across the measured range, and newer implementations use polynomial/multi-wavelength calibration. citeturn0search0turn0search1

## Project structure

```text
raspberry-pi-spectrometer/
├── src/
│   ├── main_gui.py
│   ├── capture.py
│   ├── calibrate.py
│   └── analysis.py
├── docs/
│   └── images/
│       ├── gui-spectrum-blue.jpg
│       ├── calibration-window.jpg
│       ├── hardware-front.jpg
│       ├── hardware-rear.jpg
│       ├── gui-spectrum-green.jpg
│       └── hardware-closeup.jpg
├── config.json
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation on Raspberry Pi

Update the system:

```bash
sudo apt update
sudo apt install python3-tk python3-opencv
```

For Raspberry Pi Camera support on current Raspberry Pi OS:

```bash
sudo apt install python3-picamera2
```

Create a virtual environment if desired:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run:

```bash
python3 src/main_gui.py
```

Some older Raspberry Pi spectrometer implementations used OpenCV plus the older camera stack, while newer Raspberry Pi OS versions use Picamera2/libcamera. citeturn0search0turn0search7

## How the measurement works

The camera sees the diffraction pattern as a horizontal band.

The software:

```text
Camera image
     ↓
Grayscale conversion
     ↓
Average central horizontal strip
     ↓
1-D intensity profile
     ↓
Normalize intensity to 0–100%
     ↓
Pixel position → wavelength
     ↓
Wavelength → frequency
     ↓
Color classification
     ↓
GUI table / CSV
```

Frequency is calculated using:

```text
f = c / λ
```

where `c` is the speed of light and `λ` is wavelength.

## Calibration model

The current reconstruction uses a simple linear mapping:

```text
wavelength = blue_nm + position_ratio × (red_nm - blue_nm)
```

This is deliberately simple so that the project is easy to understand.

For a stronger final-year / portfolio version, replace this with 3+ known spectral lines and a polynomial fit. A second-generation open-source Raspberry Pi spectrometer uses a third-order polynomial calibration to compensate for non-linearity. citeturn0search1

## GitHub upload

From the project folder:

```bash
git init
git add .
git commit -m "Initial Raspberry Pi spectrometer project"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/raspberry-pi-spectrometer.git
git push -u origin main
```

Before pushing, replace `YOUR_USERNAME` with your GitHub username and create an empty repository named:

```text
raspberry-pi-spectrometer
```

## Adding your project images

The six supplied images are already arranged in:

```text
docs/images/
```

GitHub automatically renders the images referenced by the README when the folder structure is preserved.

If you add another photo, for example:

```text
docs/images/assembled-device.jpg
```

add this to the README:

```markdown
![Assembled device](docs/images/assembled-device.jpg)
```

## Recommended GitHub presentation

Use this repository title:

**Raspberry Pi Spectrometer**

Suggested GitHub description:

> Low-cost Raspberry Pi optical spectrometer using a camera, diffraction grating, Python, OpenCV and wavelength calibration.

Suggested topics:

```text
raspberry-pi
python
opencv
spectrometer
spectroscopy
computer-vision
optics
electronics
stem
hardware
```

## Important accuracy note

This project should be presented as a **low-cost educational spectrometer**, not as a laboratory-grade spectrometer. Camera response, optical alignment, diffraction-grating geometry, focus, exposure and calibration all affect the result. Existing low-cost Raspberry Pi spectrometer work reports accuracy on the order of a few nanometres for suitable builds, while more advanced calibration methods can improve the mapping. citeturn0search0turn0search1

## License

Choose a license appropriate to your own code. MIT is a simple option for a portfolio project if you want others to reuse it.
