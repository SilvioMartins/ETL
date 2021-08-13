#Importações de Módulos
import json 
from tweepy import OAuthHandler, Stream , StreamListener
from datetime import datetime

#Chaves de acesso ao Tweeter
consumer_key = 
consumer_secret = 

access_token = 
access_token_secret = 

#definir arquivo de saída
data_agora = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
out = open(f"tweets_coleted_{data_agora}.txt","w")

#Classe para Conexão com o tweeter- Sobreescrever 2 métodos
class MyListener(StreamListener):
    #Quando receber algum dados escreve no arquivo no formato json
    def on_data(self, data):
        itemString = json.dumps(data)
        out.write(itemString + "\n")
        return True

    #Printa os erros
    def on_error(self, status):
        print(status)

#Implementação MAIN
if __name__ == "__main__":
    #Instacia Listener
    l= MyListener()
    #Faz a conexão no tweeter com as chaves
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    #Se autentica no Tweeter e pega conforme as palavras-chave
    stream = Stream(auth, l)
    stream.filter(track=["Diney Plus","disney plus","disney+"])
