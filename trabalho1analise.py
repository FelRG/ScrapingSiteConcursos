import re
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from datetime import datetime
import json
import copy


def ExtrairTodosConcursos():
    try:
        # Tenta fazer a requisição ao site
        html = urlopen('https://www.pciconcursos.com.br/concursos/')
        soup = BeautifulSoup(html.read(), 'html.parser')

    except HTTPError as e:
        print(f"Erro HTTP ao acessar o site: {e.code}")
        return []
    except URLError as e:
        print(f"Erro de URL ao acessar o site: {e.reason}")
        return []
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        return []

    # Lista para guardar todos os concursos
    todos_concursos = []

    # Seleciona todas as divs de concursos
    concursos = soup.find_all('div', class_=['na', 'da', 'ea'])

    for concurso in concursos:
        try:
            # primeira div "ca" que pega o nome da instituicao do concurso
            ca_div = concurso.find('div', class_='ca')  # facilitar captura do texto de dentro da div
            instituicao = ca_div.find('a').get_text(strip=True) or None

            # segunda div "cc" que pega o nome do estado
            cc_div = concurso.find('div', class_='cc')
            estado = cc_div.get_text(strip=True) or None

            # terceira div "cd" que pega a quantidade de vagas, salario, cargos, escolaridade
            cd_div = concurso.find('div', class_='cd')
            cargo = ''
            qnt_vagas = ''
            salario = ''
            escolaridade = ''

            if cd_div:
                # pega o primeiro texto diretamente da div (antes do primeiro <br>)
                textos = list(cd_div.stripped_strings)

                if textos:
                    primeiro_texto = textos[0]
                    vagas_match = re.search(r'(\d+)\s+vagas?', primeiro_texto, re.IGNORECASE)
                    salario_match = re.search(r'R\$[\s\d.,]+', primeiro_texto)

                    if vagas_match:
                        qnt_vagas = int(vagas_match.group(1))
                    else:
                        qnt_vagas = None

                    if salario_match:
                        salario = salario_match.group(0)
                    else:
                        salario = None

            if len(textos) >= 2:
                cargo = textos[1]
                if cargo.strip() == '': cargo = None
            if len(textos) >= 3:
                escolaridade = textos[2]
                if escolaridade.strip() == '': escolaridade = None

            # quarta div "ce" que pega a data limite de inscrição
            ce_div = concurso.find('div', class_='ce')
            data_limite_raw = ce_div.find('span').get_text(strip=True) or None

            # usa regex para extrair apenas a data no formato dd/mm/aaaa
            data_limite = None
            if data_limite_raw:
                match = re.search(r'\d{2}/\d{2}/\d{4}', data_limite_raw)
                if match:
                    data_limite = match.group(0)

            # span que pega a url do link da noticia do concurso
            url = concurso.get('data-url', '').strip() or None

            concurso_dict = {
                "url": url,
                "instituicao": instituicao,
                "estado": estado,
                "quantidade_vagas": qnt_vagas,
                "salario": salario,
                "cargo": cargo,
                "escolaridade": escolaridade,
                "data_limite": data_limite
            }

            todos_concursos.append(concurso_dict)

        except AttributeError as e:
            print(f"Erro ao acessar um elemento da página: {e}")
            continue  # Ignora o concurso e continua com o próximo

    with open('TodosConcursos.json', 'w', encoding='utf-8') as f:
        json.dump(todos_concursos, f, ensure_ascii=False, indent=4)

    print("Arquivo 'TodosConcursos.json' criado com sucesso!")

    return todos_concursos

def MostrarConcursosAbertos(todos_concursos):
    try:
        todos_concursos_copia = copy.deepcopy(todos_concursos)

        # Obtém a data atual do sistema
        data_atual = datetime.now().strftime('%d/%m/%Y')

        concursos_abertos = [
            concurso for concurso in todos_concursos_copia
            if concurso['data_limite'] and datetime.strptime(concurso['data_limite'], '%d/%m/%Y') >= datetime.strptime(
                data_atual, '%d/%m/%Y')
        ]

        with open('ConcursosAbertos.json', 'w', encoding='utf-8') as f:
            json.dump(concursos_abertos, f, ensure_ascii=False, indent=4)

        print("Arquivo 'ConcursosAbertos.json' criado com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro ao tentar exibir os concursos abertos: {e}")
    return

def MostrarConcursosRioGrandeDoSul(todos_concursos):
    try:
        todos_concursos_copia = copy.deepcopy(todos_concursos)
        concursos_rs = [
            concurso for concurso in todos_concursos_copia
            if concurso['estado'] == 'RS'
        ]

        with open('ConcursosRS.json', 'w', encoding='utf-8') as f:
            json.dump(concursos_rs, f, ensure_ascii=False, indent=4)

        print("Arquivo 'ConcursosRS.json' criado com sucesso!")

    except Exception as e:
        print(f"Ocorreu um erro ao tentar exibir os concursos de RS: {e}")


# Chamando a função para extrair todos os concursos
todos_concursos = ExtrairTodosConcursos()

# Chamando a função para mostrar os todos os concursos abertos
MostrarConcursosAbertos(todos_concursos)

# Chamando a função para mostrar os concursos de Rio Grande do Sul
MostrarConcursosRioGrandeDoSul(todos_concursos)

