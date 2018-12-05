from bs4 import BeautifulSoup
import requests
import telepot
import random
import time
from datetime import date
from unicodedata import normalize
import os

bot = telepot.Bot('660870867:AAEIGmJV0IPXmz8eN03Ewr16UZwXG9n4Rd4')
vips = [556126858]
comandos = ["/addsaudacao 'texto' - Ensina o bot uma nova saudação.","/eventos 'cidade' - Te manda todos os eventos de uma cidade.","/criaragenda - Cria uma agenda.","/agenda 'texto' - Escreve na sua agenda.","/agenda - Mostra a sua agenda.","/deletaragenda - Deleta sua agenda."]

print('Bot Iniciado...')

def escreverAgenda(chatID,anotacao):
    try:
        arquivo = open('./data/agenda/'+str(chatID)+".txt",'a')
        arquivo.write(anotacao+'\n')
        arquivo.close()
    except OSError:
        bot.sendMessage(chatID,'Você não possui uma agenda! Use /criaragenda para criar uma.')
    
def mostrarAgenda(chatID):
    arquivo = open('./data/agenda/'+str(chatID)+".txt",'r')
    texto = arquivo.read()
    bot.sendMessage(chatID,texto)
    arquivo.close()
def criarAgenda(chatID):
    arquivo = open('./data/agenda/'+str(chatID)+".txt",'a')
    arquivo.write("Anotações:\n")
    arquivo.close()
def deletarAgenda(chatID):
    try:
        os.remove('./data/agenda/'+str(chatID)+'.txt')
        bot.sendMessage(chatID, 'Agenda deletada!')

    except OSError:
        bot.sendMessage(chatID,'Você não possui uma agenda!.')
    

def raspandoeventos(cidade,chatID):
    cidade_nome = cidade
    cidade = cidade.replace(" ","-")
    url = 'https://www.sympla.com.br/eventos/'+cidade+'-sp'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    nomes = soup.findAll('div',class_='event-name')
    datas_meses = soup.findAll('div',class_='calendar-month')
    datas_dias = soup.findAll('div',class_='calendar-day')
    horarios_locais = soup.findAll('div',class_='event-local-box')
    links_imagens = soup.findAll('div',class_='event-image-box')
    for nome,data_mes,data_dia,horario_local,link_imagem in zip(nomes,datas_meses,datas_dias,horarios_locais,links_imagens):
        evento_nome = nome.text
        evento_data_mes = data_mes.text
        evento_data_dia = data_dia.text
        evento_data_mes = evento_data_mes.replace('\n','').replace(' ','')
        evento_data_dia = evento_data_dia.replace('\n','').replace(' ','')
        evento_horario_local = horario_local.text
        evento_horario_local = evento_horario_local.replace('\n','')
        evento_imagem = link_imagem['style']
        evento_imagem = evento_imagem.replace("background-image:url('","")
        evento_imagem = evento_imagem.replace("')","")
    
        bot.sendPhoto(chatID,evento_imagem)
        bot.sendMessage(chatID,evento_nome)
        bot.sendMessage(chatID,evento_data_dia +' de '+evento_data_mes)
        bot.sendMessage(chatID,evento_horario_local.lstrip())
    print('Quartinha raspou alguns eventos...')
    
    
def raspandonomes(chatID):
    url = 'https://www.pornpics.com/pornstars/list/'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    nomes = soup.findAll('a',href=True,title=True)
    links = soup.findAll('a',href=True,title=True)
    cont = 0
    nome = ''
    link = ''
    sort = random.randint(1,1751)

    for x,y in zip(nomes,links):
        nome = x['title']
        link = y['rel']
        cont=cont+1
        if cont == sort:break
    bot.sendMessage(chatID,nome)
    for l in link:
        bot.sendPhoto(chatID,l)
    nome = nome.replace(' ','-')    
    bot.sendMessage(chatID,'https://www.pornhub.com/pornstar/'+nome)
    print('Quartinha raspou um nome...')
        
def aprenderSaudacao(chatID,novasaudacao):
    novasaudacao = novasaudacao.replace('/addsaudacao ','')
    saudacoes = open('./data/saudações.txt','r')
    if (novasaudacao+'\n' in saudacoes)==False:
        saudacoes.close()
        saudacoes = open('./data/saudações.txt', 'a')
        saudacoes.write(novasaudacao+'\n')
        saudacoes.close()
        bot.sendMessage(chatID,'Eu registrei isso no meu banco de dados!')
    else:
        bot.sendMessage(chatID,'Essa saudação já está registrada no meu banco de dados!')
    print('Quartinha aprendeu uma nova saudação...')
    
def saudar(chatID):
    if chatID in vips:
        bot.sendMessage(chatID,'Olá Criador!')
        bot.sendMessage(chatID,'Aqui está uma lista do que posso fazer:')
        for comando in comandos:
            bot.sendMessage(chatID,comando)
    else:
        bot.sendMessage(chatID,'Olá, eu sou Quartinha, seu assistente pessoal!')
        bot.sendMessage(chatID,'Aqui está uma lista do que posso fazer:')
        for comando in comandos:
            bot.sendMessage(chatID,comando)
    
def recebendoMsg(msg):
    horario = time.localtime(time.time())
    hora =  str(horario.tm_hour)
    minuto = str(horario.tm_min)
    segundo = str(horario.tm_sec)
    if len(hora)==1:
        hora = '0'+hora
    if len(minuto)==1:
        minuto = '0'+minuto
    if len(segundo)==1:
        segundo = '0'+segundo
    tempo = hora+':'+minuto+':'+segundo+' '
    data = date.today()
    chatID = msg['chat']['id']
    nome = msg['chat']['first_name']
    sobrenome = msg['chat']['last_name']
    log = open("./data/log/"+str(data)+".txt", 'a')
    log.write(tempo+'['+str(chatID)+']'+nome+':'+msg['text']+'\n')
    log.close()
    print('[',chatID,']',nome,sobrenome,':',msg['text'])
    mensagem = (msg['text'])
    mensagem = mensagem.lower()
    mensagem = normalize('NFKD', mensagem).encode('ASCII', 'ignore').decode('ASCII')
    saudacoes = open('./data/saudações.txt','r')
    
    if mensagem+'\n' in saudacoes:
        mensagem = ''
        saudar(chatID)
    saudacoes.close()
    
    if mensagem == '/fazaboa':
        mensagem = ''
        raspandonomes(chatID)
        
    if '/addsaudacao ' in mensagem:
        novasaudacao = mensagem
        mensagem = ''
        aprenderSaudacao(chatID,novasaudacao)
    if '/eventos ' in mensagem:
        cidade = mensagem.replace('/eventos ','')
        mensagem = ''
        raspandoeventos(cidade,chatID)
        
    if mensagem == '/criaragenda':
        mensagem = ''
        criarAgenda(chatID)

    if mensagem == '/deletaragenda':
        mensagem = ''
        deletarAgenda(chatID)
    
    if '/agenda ' in mensagem:
        anotacao = mensagem.replace('/agenda', '')
        mensagem = ''
        escreverAgenda(chatID,anotacao)
    if mensagem == '/agenda':
        mensagem = ''
        mostrarAgenda(chatID)
        
    if mensagem != '':
        bot.sendMessage(chatID,'Hmmm, eu não entendi, tente usar "Oi".')

    

    
bot.message_loop(recebendoMsg)

while True:
    pass
