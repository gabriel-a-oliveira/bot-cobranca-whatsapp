from datetime import datetime
import pandas as pd
import pywhatkit as kit
import pyautogui
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configurar o acesso à planilha do Google Sheets
scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
credentials_path = "./credenciais.json"  # Caminho direto para o arquivo de credenciais
credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scopes)
cliente = gspread.authorize(credentials)

# Acessa a planilha pelo nome
planilha_google = cliente.open("CobrançaInquilino").sheet1

# Converte os dados da planilha em um DataFrame do pandas
dados = planilha_google.get_all_records()
planilha = pd.DataFrame(dados)

# Data atual
hoje = datetime.now().date()

def GerarMensagem(status, inquilino, casa, endereco, valor, vencimento):
    if status == "Pendente":
        mensagem = (f"Olá, *{inquilino}*! 😊\n\n"
                    f"Esse é um lembrete de que o aluguel da casa "
                    f"(Endereço: {endereco}) no valor de *R$ {valor}*, *vence hoje ({vencimento})*.\n\n"
                    f"Por favor, não se esqueça de realizar o pagamento. Caso já tenha feito, desconsidere esta mensagem.")
        
    elif status == "Atrasado":
        mensagem = (f"Oi, *{inquilino}*! ⚠️\n\n"
                        f"Infelizmente, o aluguel da casa {casa} (Endereço: {endereco}) "
                        f"no valor de *R$ {valor}* está atrasado desde *{vencimento}*. \n\n"
                        f"Pedimos, por gentileza, que regularize o pagamento o quanto antes para evitar inconvenientes.\n\n"
                        f"Agradecemos pela sua atenção e compreensão.")
    
    return mensagem

def EnviarMensagemWhatsapp(whatsapp, mensagem):
    kit.sendwhatmsg_instantly(whatsapp, mensagem, 15, True)
    time.sleep(3)
        
for _, linha in planilha.iterrows():
    casa = linha['Casa']
    inquilino = linha['Inquilino']
    whatsapp = str(linha['WhatsApp'])
    endereco = linha['Endereço']
    valor = linha['Valor']
    vencimento = linha['Vencimento']
    status = linha['Status']
    
    whatsapp = "+55" + whatsapp.strip()

    # Converte a data de vencimento
    vencimento_date = datetime.strptime(vencimento, "%d/%m/%Y").date()
    dias_para_vencimento = (vencimento_date - hoje).days

    # Envia cobranças
    if status == "Pendente" and dias_para_vencimento == 0:
        mensagem = GerarMensagem(status, inquilino, casa, endereco, valor, vencimento)
        EnviarMensagemWhatsapp(whatsapp, mensagem)

    elif status == "Atrasado" and dias_para_vencimento < 0:
            mensagem = GerarMensagem(status, inquilino, casa, endereco, valor, vencimento)
            EnviarMensagemWhatsapp(whatsapp, mensagem)
