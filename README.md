# Web Scraper de Concursos Públicos com Python

## Descrição

Este projeto realiza a extração automática de concursos públicos do site PCI Concursos utilizando Web Scraping com Python.

O programa coleta informações dos concursos, organiza os dados e gera arquivos JSON contendo:

- Todos os concursos encontrados
- Apenas concursos com inscrições abertas
- Apenas concursos do Rio Grande do Sul

O script utiliza tratamento de erros e validações para garantir que os dados sejam extraídos corretamente. 

---

## Bibliotecas Utilizadas

```python
import re
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from datetime import datetime
import json
import copy
```

---

## Informações Extraídas

Para cada concurso, são coletados os seguintes dados:

- URL da notícia
- Instituição
- Estado
- Quantidade de vagas
- Salário
- Cargo
- Escolaridade
- Data limite de inscrição

Exemplo de estrutura:

```python
{
    "url": "https://...",
    "instituicao": "Prefeitura Municipal",
    "estado": "RS",
    "quantidade_vagas": 20,
    "salario": "R$ 3.500,00",
    "cargo": "Analista Administrativo",
    "escolaridade": "Ensino Superior",
    "data_limite": "30/06/2026"
}
```

---

## Funções do Projeto

### `ExtrairTodosConcursos()`

Responsável por acessar o site, percorrer o HTML e extrair todos os concursos encontrados.

Também gera o arquivo:

```python
TodosConcursos.json
```

---

### `MostrarConcursosAbertos(todos_concursos)`

Filtra apenas concursos cuja data limite de inscrição ainda não expirou.

Gera o arquivo:

```python
ConcursosAbertos.json
```

---

### `MostrarConcursosRioGrandeDoSul(todos_concursos)`

Filtra apenas concursos localizados no Rio Grande do Sul.

Gera o arquivo:

```python
ConcursosRS.json
```

---

## Tratamento de Erros

O código possui tratamento para:

- Falhas de conexão com o site
- URLs inválidas
- Problemas na estrutura HTML
- Campos vazios
- Datas ausentes ou inválidas
- Erros na gravação dos arquivos JSON

Exemplo:

```python
except HTTPError as e:
    print(f"Erro HTTP ao acessar o site: {e.code}")
```

---

## Como Executar

1. Instale a dependência necessária:

```bash
pip install beautifulsoup4
```

2. Execute o arquivo Python:

```bash
python trabalho1analise.py
```

3. Após a execução, serão gerados os arquivos:

```python
TodosConcursos.json
ConcursosAbertos.json
ConcursosRS.json
```

---

## Tecnologias Utilizadas

- Python
- BeautifulSoup
- urllib
- Regex
- JSON
- Web Scraping
