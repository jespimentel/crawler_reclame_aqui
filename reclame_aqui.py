#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 15:09:19 2023

@author: pimentel
"""
#%% Importações

import requests
from bs4 import BeautifulSoup
import pandas as pd

#%% Configurações do usuário

empresa = 'estrela10'
n_max_pag = 50

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}         

#%% Lista de links com as reclamações

link_list = []

for pag in range (1, n_max_pag+1):
    url = f'https://www.reclameaqui.com.br/empresa/{empresa}/lista-reclamacoes/?pagina={str(pag)}'
    classe = "sc-1sm4sxr-0 jLKCJu"

    response = requests.get(url, headers=headers)
    print('Estou na página', pag)

    soup = BeautifulSoup(response.content, 'html.parser')
    conteudo_div = soup.find('div', class_= classe)

    links = conteudo_div.find_all('a')        
    for link in links:
        href = link.get('href')
        link_list.append('https://www.reclameaqui.com.br' + href)
        
#%% Gerando arquivo com a lista de links de reclamações

# Excluindo os repetidos
link_list = list(set(link_list))

print(f'Foram encontrados {len(link_list)} links únicos.')

with open('lista_de_links.txt', 'w') as file:
    for link in link_list:
        file.write(str(link) + '\n')
        
#%% Função para a coleta das reclamações

def obtem_reclamacao (url, headers=headers):
    
    response = requests.get(url, headers=headers)
    
    soup = BeautifulSoup(response.content, 'html.parser')
    conteudo_div = soup.find('div', class_= 'lzlu7c-19 bewOsl')
    
    titulo = conteudo_div.find('h1', attrs={'data-testid': 'complaint-title'})
    if titulo:
        titulo = titulo.text.strip()
    
    localizacao = conteudo_div.find('span', attrs={'data-testid': 'complaint-location'})
    if localizacao:
        localizacao = localizacao.text.strip()
    
    data_criacao = conteudo_div.find('span', attrs={'data-testid':'complaint-creation-date'})
    if data_criacao:
        data_criacao = data_criacao.text.strip()
    
    ident = conteudo_div.find('span', attrs={'data-testid':'complaint-id'})
    if ident:
        ident = ident.text.strip()
    
    descricao = conteudo_div.find('p', attrs={'data-testid':'complaint-description'})
    if descricao:
        descricao = descricao.text.strip()
        
    return (data_criacao, localizacao, ident, titulo, descricao)

#%% Lista de reclamações

lista_de_reclamacoes = []
n=1
for link in link_list:
    reclamacao = obtem_reclamacao(link)
    lista_de_reclamacoes.append(reclamacao)
    print(f'\n\nAdicionando a reclamacao n. {n}\n', reclamacao)
    n += 1
    
#%% Criando o dataframe 

df = pd.DataFrame(lista_de_reclamacoes, columns=['Data_da_criacao', 'Localizacao', 'Id', 'Titulo', 'Descricao'])

#%% Salvando o dataframe

df.to_csv('reclamacoes_{empresa}.csv')







