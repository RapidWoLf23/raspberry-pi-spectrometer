from dataclasses import dataclass, asdict
from pathlib import Path
import json

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.json"


@dataclass
class Calibration:
    red_wavelength: float = 650.0
    blue_wavelength: float = 450.0

    def save(self, path=CONFIG_PATH):
        Path(path).write_text(
            json.dumps(asdict(self), indent=2),
            encoding="utf-8"
        )

    @classmethod
    def load(cls, path=CONFIG_PATH):
        try:
            data = json.loads(Path(path).read_text(encoding="utf-8"))
            return cls(
                red_wavelength=float(data["red_wavelength"]),
                blue_wavelength=float(data["blue_wavelength"]),
            )
        except (FileNotFoundError, KeyError, ValueError, json.JSONDecodeError):
            return cls()
