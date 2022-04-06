##pip install pandas 
# -*- coding: utf-8 -*-
## Importa Bibliotecas

import requests
import pandas as pd
import sys
import os

reload(sys)
encoding = 'utf-8'
sys.setdefaultencoding(encoding)
processes = 6


today = sys.argv[1:]
data =  today[0]

## URL de acesso da API para pegar o token

url = 'http://0800web.directdial.com.br/api/v1/request-token'

## Login de Acesso

login = {"login": "XXXXXX", "password": "XXXXXXX"}

## Solicita token de acesso

token = requests.post(url,data=login)
## converte token em json

token = token.json()
## Definindo Parâmetros para a Solcitação do Reltório

date_ini_str = data
date_fin_str = data 


url_r15 = 'http://0800web.directdial.com.br/api/v1/relatorio/metrica-atendida?data-inicial='+date_ini_str+' 00:00&data-final='+date_fin_str+' 23:59&page=1&page-size=5000'
## Pegando Relatório via API



relatorio15 = requests.get(url_r15,headers = {"Authorization" : token['access_token']})

##  Covertendo Para JSON

r15_json = relatorio15.json()
## Convertendo para Dataframe

df_r15 = pd.DataFrame(r15_json['_embedded']['collection'])

df_r15.rename(columns = {'% Atend. End to End (N+R)':'Perc Atend. End to End (N+R)',
                '% Atend. End to End (Novos)':'Perc Atend. End to End (Novos)',
                '% Atend. Entregues (Novos)':'Perc Atend. Entregues (Novos)',
                '% de atendido total':'Perc de atendido total',
                '% de entregues':'Perc de entregues',
                'Abandono (Novos)':'Abandono_novos',
                'Abandono (Reaproveitados)':'Abandono_Reaproveitados',
                'Atendido (N+R)':'Atendido_N_R_Atendidos_Novos',
                'Atendidos (Novos)':'Atendidos_Reaproveitados',
                'Atendidos reaproveitados':'Chamada curta Novos',
                'Chamada curta (Novos)':'Chamada_Curta_nova',
                'Chamada curta (Reaproveitados)':'Chamada_curta_Reaproveitados',
                'Data':'Data',
                'Dia da semana':'Dia da semana',
                'Entregue (N+R)':'Entregue',
                'Entregues (Novos)':'Entregues_Novos',
                'Entregues reaproveitados':'Entregues_reaproveitados',
                'Operação':'Operacao',
                'Solicitação Site (novos)':'Solicitacao_Site_novos',
                'TMR':'TMR'},inplace = True)


df_r15.columns=df_r15.columns.str.replace('%','Perc') 

## Tira o % das linhas


df_r15['Perc de entregues'] = df_r15['Perc de entregues'].str.replace('%','')
df_r15['Perc Atend. End to End (N+R)'] = df_r15['Perc Atend. End to End (N+R)'].str.replace('%','')
df_r15['Perc Atend. Entregues (Novos)'] = df_r15['Perc Atend. Entregues (Novos)'].str.replace('%','')
df_r15['Perc Atend. End to End (Novos)'] = df_r15['Perc Atend. End to End (Novos)'].str.replace('%','')
df_r15['Perc de atendido total'] = df_r15['Perc de atendido total'].str.replace('%','')


## Gerando CSV - relatorio15.csv


df_r15.to_csv('/databi/pmv/scripts/data/data.output/relatorio15-{0}.csv'.format(data),sep=';',index=False,header=True)
