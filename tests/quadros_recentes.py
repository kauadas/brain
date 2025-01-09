
configs = {
    "ultimos-5-quadros": ["ol","a","b","c","d"]
}


def add_quadro_to_list(quadro_name: str):
    """
    adiciona um quadro ao list de quadros recentes
    """
    if quadro_name in configs["ultimos-5-quadros"]:
        configs["ultimos-5-quadros"].remove(quadro_name)

    if len(configs["ultimos-5-quadros"]) == 5:
        
        configs["ultimos-5-quadros"].pop()

    configs["ultimos-5-quadros"].insert(0,quadro_name)


add_quadro_to_list("teste")

print(configs["ultimos-5-quadros"])