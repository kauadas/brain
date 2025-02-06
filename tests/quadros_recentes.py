
configs = {
    "last-five-canvas": ["ol","a","b","c","d"]
}


def add_quadro_to_list(quadro_name: str):
    """
    adiciona um quadro ao list de quadros recentes
    """
    if quadro_name in configs["last-five-canvas"]:
        configs["last-five-canvas"].remove(quadro_name)

    if len(configs["last-five-canvas"]) == 5:
        
        configs["last-five-canvas"].pop()

    configs["last-five-canvas"].insert(0,quadro_name)


add_quadro_to_list("teste")

print(configs["last-five-canvas"])