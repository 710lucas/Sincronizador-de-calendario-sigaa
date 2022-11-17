
from requests import Session, Request
import requests
from bs4 import BeautifulSoup
from getpass import getpass
from google_calendar import add_event
from google_calendar import get_event
import google_calendar
import datetime

def main():
    s = requests.Session()

    r = s.get("https://sigaa.ufpb.br/sigaa/logon.jsf")
    soup = BeautifulSoup(r.text, "lxml")
    j_id = soup.find("input", {"id": "javax.faces.ViewState"})["value"]

    usuario = input("Seu usuario do sigaa: ")
    senha  = getpass("Senha: ")

    dados = {
        "form": "form",
        "form:width":	"1920",
        "form:height": "1080",
        "form:login": usuario,
        "form:senha": senha,
        "form:entrar": "Entrar",
        "javax.faces.ViewState":	j_id
    }

    head =  {

        "Host": "sigaa.ufpb.br",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://sigaa.ufpb.br",
        "Connection": "keep-alive",
        "Referer": "https://sigaa.ufpb.br/sigaa/logon.jsf",
        "Upgrade-Insecure-Requests": "1",
    }


    s.headers = head
    resp = s.post("https://sigaa.ufpb.br/sigaa/logon.jsf", data=dados)

    lel = s.get("https://sigaa.ufpb.br/sigaa/portais/discente/beta/discente.jsf")

    if (lel.url != "https://sigaa.ufpb.br/sigaa/portais/discente/beta/discente.jsf"):
        print("Senha ou usuarion invalidos")

    else:
        print("login feito com sucesso")

        f = open("lel", "w")
        f.write(lel.text)

        soup = BeautifulSoup(lel.text, "lxml")
        turmas = soup.find("table", {"class": "minhas-turmas"})
        trs = turmas.find_all("tr")

        for i in range(1, len(trs), 1):
            try:
                materia_soup = BeautifulSoup(str(trs[i]), "lxml")
                materia = materia_soup.find("a").text
                info = materia_soup.find("div", {"class": "info"}).text
                dia = 0
                mes = 0
                for j in range(len(info)):
                    if (info[j] == "/"):
                        dia = int(info[j-2]+info[j-1])
                        mes = int(info[j+1]+info[j+2])

                print(info)
                print(str(dia)+"/"+str(mes))
                print(materia)
                if len(get_event(dia, mes, materia)["items"])>0:
                    for events in get_event(dia, mes, materia)["items"]:
                        if (events['start']['date'] != datetime.date.today().year+"-"+mes+"-"+dia and events['summary'] != materia):
                            add_event(dia, mes, materia)
                else:
                    add_event(dia,mes,materia)


            except:
                pass


main()