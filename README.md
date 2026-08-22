# Raspberry Pi Spectrometer

A low-cost optical spectrometer built with a Raspberry Pi, camera, diffraction grating, and a Python/OpenCV analysis pipeline.

The system captures a dispersed light spectrum, converts camera position into wavelength, calculates frequency, classifies visible colors, and exports the measured spectrum as CSV.

## Project Overview

### Hardware

- Raspberry Pi
- Raspberry Pi Camera / compatible camera
- Diffraction grating
- Custom optical enclosure / tube
- Camera ribbon cable
- Python desktop application

![Spectrometer hardware](docs/images/hardware-front.jpg)

The camera is positioned to view the dispersed spectrum through the optical tube. Careful alignment, focus, exposure, and a stable light path are important for consistent measurements.

![Spectrometer hardware - rear](docs/images/hardware-rear.jpg)

![Spectrometer hardware - close-up](docs/images/hardware-closeup.jpg)

## Software

The application provides four main functions:

1. **Capture** – acquire an image from the camera.
2. **Analyze** – extract the spectrum and calculate wavelength, intensity, frequency, and color.
3. **Calibrate** – configure the reference wavelengths used by the wavelength mapping.
4. **Export** – save the analyzed spectrum as a CSV file.

### Spectrum Analysis

![Spectrum analysis](docs/images/gui-spectrum-blue.jpg)

The GUI displays:

- Wavelength (nm)
- Relative intensity (%)
- Frequency (THz)
- Approximate visible-light color

![Green and yellow spectrum](docs/images/gui-spectrum-green.jpg)

### Calibration

![Calibration settings](docs/images/calibration-window.jpg)

The default calibration references are:

- Blue: **450 nm**
- Red: **650 nm**

For improved accuracy, the calibration can be extended to use multiple known spectral lines instead of only two endpoints.

## How It Works

```text
Camera
  ↓
Capture spectrum image
  ↓
OpenCV image processing
  ↓
Extract intensity profile
  ↓
Normalize intensity
  ↓
Pixel position → wavelength
  ↓
Wavelength → frequency
  ↓
Color classification
  ↓
GUI / CSV export
```

Frequency is calculated using:

```text
f = c / λ
```

where `c` is the speed of light and `λ` is wavelength.

## Calibration Model

The current implementation uses a simple linear mapping between the calibrated blue and red reference wavelengths:

```text
wavelength = blue_nm + position_ratio × (red_nm - blue_nm)
```

This keeps the implementation simple and easy to understand.

A future version could use multiple reference lines and polynomial calibration to compensate for optical non-linearity and improve wavelength accuracy.

## Project Structure

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
│       ├── gui-spectrum-green.jpg
│       ├── hardware-front.jpg
│       ├── hardware-rear.jpg
│       └── hardware-closeup.jpg
├── config.json
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

On Raspberry Pi OS:

```bash
sudo apt update
sudo apt install python3-tk python3-opencv
sudo apt install python3-picamera2
```

Then:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the application:

```bash
python3 src/main_gui.py
```

## Technologies Used

- **Python**
- **Tkinter**
- **OpenCV**
- **NumPy**
- **Picamera2**
- **Raspberry Pi**
- **Diffraction grating / optical spectroscopy**

## Accuracy

This is an educational, low-cost spectrometer rather than a laboratory-grade instrument. Results depend on camera response, optical alignment, focus, exposure, diffraction-grating geometry, and calibration quality.

## Future Improvements

- Multi-point wavelength calibration
- Polynomial calibration
- Automatic peak detection
- Spectrum graphing
- Dark-frame subtraction
- Exposure control
- Saving measurement sessions
- Real-time spectrum visualization

## License

MIT License
