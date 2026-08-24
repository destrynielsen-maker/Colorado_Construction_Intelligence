from pathlib import Path
from .pipeline import run
if __name__ == "__main__": print(run(Path(__file__).resolve().parents[2]))
