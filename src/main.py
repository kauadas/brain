from data.modules.interface import Aplicativo
from pathlib import Path
from os import chdir, path, mkdir

file = Path(__file__)
chdir(file.parent)
print(file.parent)

if not path.exists("data/json/quadros"):
    mkdir("data/json/quadros")

if not path.exists("data/png/quadros"):
    mkdir("data/png/quadros")


if __name__ == '__main__':
    app = Aplicativo()
    app.run()