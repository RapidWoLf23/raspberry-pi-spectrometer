from pathlib import Path
import cv2
import numpy as np

try:
    from picamera2 import Picamera2
except ImportError:
    Picamera2 = None


class SpectrometerCapture:
    """
    Camera acquisition layer.

    On a Raspberry Pi with Picamera2 installed, it uses the Pi Camera.
    Otherwise it falls back to an OpenCV camera (useful for development).
    """

    def __init__(self, camera_index=0, width=1280, height=720):
        self.width = width
        self.height = height
        self.camera_index = camera_index
        self.picam2 = None
        self.cap = None

        if Picamera2 is not None:
            try:
                self.picam2 = Picamera2()
                config = self.picam2.create_preview_configuration(
                    main={"size": (width, height), "format": "RGB888"}
                )
                self.picam2.configure(config)
                self.picam2.start()
            except Exception:
                self.picam2 = None

        if self.picam2 is None:
            self.cap = cv2.VideoCapture(camera_index)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

    def capture_frame(self):
        if self.picam2 is not None:
            frame = self.picam2.capture_array()
            return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        if self.cap is None or not self.cap.isOpened():
            raise RuntimeError(
                "Camera could not be opened. Check the Pi Camera connection "
                "or use a USB camera."
            )

        ok, frame = self.cap.read()
        if not ok:
            raise RuntimeError("Camera frame capture failed.")
        return frame

    def frame_to_spectrum(self, frame):
        """
        Convert the camera image into a 1-D spectrum.

        The spectroscope should produce a horizontally aligned spectrum.
        We average a narrow vertical strip around the centre to reduce noise.
        """
        if frame is None or frame.size == 0:
            return []

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Ignore the outer edges where the spectrum is less reliable.
        h, w = gray.shape
        y1 = int(h * 0.35)
        y2 = int(h * 0.65)
        strip = gray[y1:y2, :]

        profile = np.mean(strip, axis=0)
        profile = cv2.GaussianBlur(profile.reshape(1, -1), (1, 0), 1.2).flatten()

        min_v = float(profile.min())
        max_v = float(profile.max())
        if max_v - min_v < 1e-9:
            intensity = np.zeros_like(profile)
        else:
            intensity = (profile - min_v) / (max_v - min_v) * 100.0

        return [
            {"pixel": int(i), "intensity_raw": float(v)}
            for i, v in enumerate(intensity)
        ]

    def close(self):
        if self.picam2 is not None:
            try:
                self.picam2.stop()
            except Exception:
                pass
        if self.cap is not None:
            self.cap.release()
