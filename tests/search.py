import re
from os import walk
from os.path import join
from sys import argv

term = argv[1] if len(argv) > 1 else input("term: ")
file_type = argv[2] if len(argv) > 2 else ""
replace = argv[3] if len(argv) > 3 else None

# Expressões regulares para ignorar comentários
comment_pattern = re.compile(r"(#.*?$)|(\"\"\".*?\"\"\"|'''.*?''')", re.DOTALL | re.MULTILINE)

for root, dirs, files in walk("./"):
    for file in files:
        if file_type and not file.endswith(file_type):
            continue

        try:
            file_path = join(root, file)
            with open(file_path, "r", encoding="utf-8") as f:
                data = f.read()

            # Remove comentários do código antes de contar e substituir
            data_no_comments = re.sub(comment_pattern, "", data)

            if term in data_no_comments:
                count = data_no_comments.count(term)
                print(file_path, "count:", count)

                lines = data.splitlines()
                for i, line in enumerate(lines):
                    line_no_comments = re.sub(r"#.*$", "", line).strip()  # Remove comentários inline
                    if term in line_no_comments:
                        print(i + 1, line)

                if replace:
                    # Substituir apenas fora dos comentários
                    def replace_match(match):
                        return match.group(0) if match.group(1) else match.group(0).replace(term, replace)

                    new_data = re.sub(
                        r"(\"\"\".*?\"\"\"|'''.*?'''|#.*?$)|" + re.escape(term), replace_match, data, flags=re.MULTILINE
                    )

                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(new_data)

        except Exception as e:
            print(f"Erro ao processar {file}: {e}")
