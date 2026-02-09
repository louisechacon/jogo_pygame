ARQUIVO_RECORDES = "recordes.csv"

def formatar_tempo(tempo_total_em_mili):
    if tempo_total_em_mili is None:
        return "--:--:---"
    
    tempo_em_segundos = tempo_total_em_mili // 1000
    resto_em_mili = tempo_total_em_mili % 1000

    minutos = tempo_em_segundos // 60
    resto_em_seg = tempo_em_segundos % 60

    return f"{minutos:02d}:{resto_em_seg:02d}:{resto_em_mili:03d}"

def converter_texto_para_recorde(texto):
    try:
        return int(texto)
    except ValueError:
        return None

def carregar_recordes():
    try:
        with open(ARQUIVO_RECORDES, "r") as arquivo:
            linha = arquivo.readline()
            lista = list(map(converter_texto_para_recorde, linha.split(",")))
            if len(lista) < 3:
                return [None, None, None]
            return lista
    except FileNotFoundError:
        return [None, None, None]

def salvar_recordes(lista_recordes):
    with open(ARQUIVO_RECORDES, "w") as arquivo:
        arquivo.write(",".join(map(str, lista_recordes)))