from data.modules.interface import Aplicativo
from data.modules.utils import generate_paths
from pathlib import Path
from os import chdir, path, mkdir

file = Path(__file__)
chdir(file.parent)
print(file.parent)


generate_paths()

if __name__ == '__main__':
    app = Aplicativo()
    app.run()