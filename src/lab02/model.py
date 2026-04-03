from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import sys


LAB01_PATH = Path(__file__).resolve().parents[1] / "lab01"
if str(LAB01_PATH) not in sys.path:
    sys.path.insert(0, str(LAB01_PATH))

spec = spec_from_file_location("lab01_model_module", LAB01_PATH / "model.py")
lab01_model_module = module_from_spec(spec)
spec.loader.exec_module(lab01_model_module)
Bus = lab01_model_module.Bus

__all__ = ["Bus"]
