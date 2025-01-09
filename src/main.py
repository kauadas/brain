from data.modules.interface import Aplicativo
from pathlib import Path
from os import chdir

file = Path(__file__)
chdir(file.parent)

if __name__ == '__main__':
    app = Aplicativo()
    app.run()