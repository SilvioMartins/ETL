import pandas as pd
import requests


# Função Conversão Horas:Minutos
def convert(seconds): 
    seconds = seconds % (24 * 3600) 
    hour = seconds // 3600 
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d:%02d" % (hour, minutes, seconds) 

#CRia Dataframe
df = pd.DataFrame(columns=['domain',
                           'start_date',
                           'end_date',
                           'global_rank',
                           'Total Visits',
                           'Total Unique Visitors',
                           'Total Pages Per Visit',
                           'Total Bounce Rate',
                           'Desktop share',
                           'Mobile share',
                           'Traffic share',
                           'Visit Duration'
                           ]
                  )

#Lista de sites    
sites=['futemax.gratis',
       'multicanais.tv',
       'futebolplayhd.com',
       'superflix.biz'
]

#Itera nos sites e gera DF
for site in sites:
    #Baixa JSON Via API
    jraw=requests.get('https://api.similarweb.com/v1/website/{0}/lead-enrichment/all?api_key=<<CODE_ACCESS>>&start_date=2021-10&end_date=2022-03&country=br&main_domain_only=false&format=json&show_verified=false'.format(site)).json()

    #Processa as colunas
    visits = 0.0
    for ch,v in enumerate(jraw['visits']):
        visits = visits  + float(v['value'])

    unique_visitors = 0.0
    for ch,v in enumerate(jraw['unique_visitors']):
        unique_visitors = unique_visitors  + float(v['value'])

    pages_per_visit = 0.0
    for ch,v in enumerate(jraw['pages_per_visit']):
        pages_per_visit = pages_per_visit  + float(v['value'])

    bounce_rate = 0.0
    for ch,v in enumerate(jraw['bounce_rate']):
        bounce_rate = bounce_rate  + float(v['value'])

    sum_desk = 0.0
    for ind in range(len(jraw['mobile_desktop_share'])):
        sum_desk = sum_desk  + float(jraw['mobile_desktop_share'][ind]['value']['desktop_share'])

    sum_mob = 0.0
    for ind in range(len(jraw['mobile_desktop_share'])):
        sum_mob = sum_mob  + float(jraw['mobile_desktop_share'][ind]['value']['mobile_share'])

    trafic = 0.0
    for ind in range(len(jraw['traffic_sources'])):
        for v in jraw['traffic_sources'][ind]['value']:
            trafic = trafic  + float(v['share'])

    visit_duration = 0.0
    for v in jraw['average_visit_duration']:
        visit_duration = visit_duration  + float(v['value'])
    avarage_visit_duration = convert(visit_duration / len(jraw['average_visit_duration']))

    #Monta Linha para inserir no DF
    df_row = [
            str(jraw['meta']['request']['domain']),
            str(jraw['meta']['request']['start_date']),
            str(jraw['meta']['request']['end_date']),
            str(jraw['global_rank']),
            visits,
            unique_visitors,
            pages_per_visit,
            bounce_rate,
            sum_desk,
            sum_mob,
            trafic,
            avarage_visit_duration
    ]
    df.loc[-1] = df_row 
    df.index = df.index + 1
    df = df.sort_index()

#Para excel
df.to_excel(r'C:\Lab_Python\df.xlsx')