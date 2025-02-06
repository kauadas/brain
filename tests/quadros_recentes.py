
configs = {
    "last-five-canvas": ["ol","a","b","c","d"]
}


def add_canva_to_list(canva_name: str):
    """
    adiciona um canva ao list de canvas recentes
    """
    if canva_name in configs["last-five-canvas"]:
        configs["last-five-canvas"].remove(canva_name)

    if len(configs["last-five-canvas"]) == 5:
        
        configs["last-five-canvas"].pop()

    configs["last-five-canvas"].insert(0,canva_name)


add_canva_to_list("teste")

print(configs["last-five-canvas"])