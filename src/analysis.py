SPEED_OF_LIGHT_KM_S = 299792.458


def wavelength_to_frequency_thz(wavelength_nm):
    """
    f = c / lambda

    c is converted to km/s and wavelength from nm to km:
    1 nm = 1e-6 km
    """
    wavelength_km = wavelength_nm * 1e-6
    return SPEED_OF_LIGHT_KM_S / wavelength_km / 1e3


def wavelength_to_color(wavelength):
    if wavelength < 450:
        return "Violet"
    if wavelength < 495:
        return "Blue"
    if wavelength < 570:
        return "Green"
    if wavelength < 590:
        return "Yellow"
    if wavelength < 620:
        return "Orange"
    if wavelength <= 700:
        return "Red"
    return "Infrared"


def analyze_spectrum(raw_spectrum, blue_nm=450.0, red_nm=650.0):
    if not raw_spectrum:
        return []

    p0 = raw_spectrum[0]["pixel"]
    p1 = raw_spectrum[-1]["pixel"]

    if p1 == p0:
        return []

    result = []
    for item in raw_spectrum:
        p = item["pixel"]
        ratio = (p - p0) / (p1 - p0)

        # Camera spectrum is assumed to run blue -> red from left -> right.
        wavelength = blue_nm + ratio * (red_nm - blue_nm)
        intensity = max(0.0, min(100.0, item["intensity_raw"]))
        frequency = wavelength_to_frequency_thz(wavelength)

        result.append({
            "pixel": p,
            "wavelength": wavelength,
            "intensity": intensity,
            "frequency": frequency,
            "color": wavelength_to_color(wavelength),
        })

    return result
