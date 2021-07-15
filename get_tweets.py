#Importações de Módulos
import json 
from tweepy import OAuthHandler, Stream , StreamListener
from datetime import datetime

#Chaves de acesso ao Tweeter
consumer_key = "Tr51hE893RIQtz5JPfZSgaozl"
consumer_secret = "HMSv7tRF4t8HlfM97CizBhzjBHopa7JYPREr3nLXaRAUoOSpCi"

access_token = "171893216-sDNQCYsholRyzhiX9ok9WsPP3q6nBUAU2scSFqCY"
access_token_secret = "ZpXdBkELUiKUtiTixNQ9wWFmtr8XM8UjnDQTZPsDm6KXc"

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