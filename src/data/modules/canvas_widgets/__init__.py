from os import walk, listdir
import re




files_path = "src/data/modules/canvas_widgets"

widgets = []

for file in listdir(files_path):
    print(file)

    if file.endswith(".py"):
        print(file)
        with open(files_path+"/"+file) as f:
            data = f.read()
            f.close()

        for i in data.splitlines():
            if i.startswith("class"):
                print(i)
                class_name = re.search("class (.*)\(",i).group(1)
                print(class_name)

                if class_name.strip().lower() == file.split(".")[0]:
                    print("match")
                    widgets.append((file,class_name))
                    break

types = {}
for i in widgets:
    file = i[0].split(".")[0]
    
    class_ = i[1]

    exec(f"from data.modules.canvas_widgets.{file} import {class_}")

    types[file] = eval(class_)

print(types)


