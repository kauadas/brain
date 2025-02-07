from os import walk, listdir, path, makedirs

from sys import path as path_sys

import re


files_path = path_sys[0]+"/data/modules/canvas_widgets"

widgets = []

if not path.exists(files_path):
    print("creating folder")
    makedirs(files_path)

for file in listdir(files_path):
    print(file)

    if file.endswith(".py"):
        print(file)
        with open(files_path+"/"+file) as f:
            data = f.read()
            f.close()

        for i in data.splitlines():
            if i.startswith("class") and "FloatWidget" in i:
                print(i)
                class_name = re.search("class (.*)\(",i).group(1)
                print(class_name)

                if class_name.strip().lower() == file.split(".")[0]:
                    print("match")
                    widgets.append((file,class_name))
                    exec(data)
                    break

        

types = {}
for i in widgets:
    file = i[0].split(".")[0]
    
    class_ = i[1]
    types[file] = eval(class_)

print(types)


