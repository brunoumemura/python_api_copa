import requests
from dataclasses import dataclass

@dataclass
class Gol:
    nome_jogador: str
    minuto: int

    def _repr_(self) -> str:
        return self.nome_jogador + " " + str(self.minuto)

@dataclass
class Partida:
    numero: int
    fase: str
    estadio: str
    mandante: str
    visitante: str
    gols_mandante: int
    gols_visitante: int
    gols: list[Gol]

    def contem(self, codigo_time: str) -> bool:
        return self.mandante == codigo_time or self.visitante == codigo_time

    def _repr_(self) -> str:
        return (
            self.fase+ " " +
            self.mandante + " " + str(self.gols_mandante) 
                + " X " 
                + str(self.gols_visitante) + " " + self.visitante)

PARTIDAS: list[Partida] = []
URL: str = "https://raw.githubusercontent.com/leandroflores/api-world-cup/main/results_2018"

def load_dados():
    response = requests.get(URL)
    dados = response.json()
    rodadas = dados["rounds"]
    for rodada in rodadas:
        partidas = rodada["matches"]
        for partida in partidas:
            numero = partida["num"]
            estadio = partida["stadium"]["name"]
            mandante = partida["team1"]["code"]
            visitante = partida["team2"]["code"]
            gols_mandante = partida["score1"]
            gols_visitante = partida["score2"]
            if "group" in partida:
                fase = partida["group"]
            else:
                fase = rodada["name"]

            gols: list[Gol] = []
            todos_os_gols: list[dict] = partida["goals1"] + partida["goals2"]
            for gol in todos_os_gols:
                gols.append(
                    Gol(gol["name"], gol["minute"])
                )
            
            partida: Partida = Partida(
                numero,
                fase,
                estadio,
                mandante,
                visitante,
                gols_mandante,
                gols_visitante,
                gols,
            )

            PARTIDAS.append(partida)
            
#maps (filtro)


    
            
def get_vitorias_visitante():
    vitorias_visitantes = []
    for partida in PARTIDAS:
        if partida.gols_visitante > partida.gols_mandante:
            vitorias_visitantes.append(partida)
    
    return vitorias_visitantes

def get_partidas_tradicional(codigo_time: str) -> list[Partida]:
    partidas_time: list[Partida] = []
    for partida in PARTIDAS:
        if partida.contem(codigo_time):
            partidas_time.append(partida)
    return partidas_time

def get_partidas_com_filter(codigo_time: str) -> list[Partida]:
    return list(
        filter(
            lambda time: time.contem(codigo_time), 
            PARTIDAS
        )
    )


def get_gols_jogador(nome_jogador: str) -> list[Gol]:
    gols_jogador: list[dict] = []
    for partida in PARTIDAS:
        for gol in partida.gols:
            if gol.nome_jogador == nome_jogador:
                gols_jogador.append(
                    {
                        "gol": gol,
                        "partida": partida,
                    }
                )
    return gols_jogador

load_dados()
# print(len(PARTIDAS))
print(PARTIDAS)

# final = PARTIDAS[-1]
# print(final)
# print(final.gols)

#gols_neymar = get_gols_jogador("Griezmann")
#print(Partida())