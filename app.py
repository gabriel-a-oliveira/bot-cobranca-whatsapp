import os
from datetime import datetime
import pandas as pd
import pywhatkit as kit
import pyautogui  # Biblioteca para automatizar pressionamentos de teclas
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

# Verifica cada aluguel
for _, linha in planilha.iterrows():
    casa = linha['Casa']
    inquilino = linha['Inquilino']
    whatsapp = str(linha['WhatsApp'])  # Converter para string
    endereco = linha['Endereço']
    valor = linha['Valor']
    vencimento = linha['Vencimento']
    status = linha['Status']
    
    # Garantir que o número de WhatsApp tenha o código do país
    whatsapp = "+55" + whatsapp.strip()  # Adiciona o código do país (Brasil)

    # Converte a data de vencimento
    vencimento_date = datetime.strptime(vencimento, "%d/%m/%Y").date()
    dias_para_vencimento = (vencimento_date - hoje).days

    # Envia lembretes ou cobranças
    if status == "Pendente":
        if dias_para_vencimento == 5:  # Lembrete 5 dias antes
            
            mensagem = (f"Olá, {inquilino}! 😊 "
                        f"Lembrete: o aluguel da casa {casa} (Endereço: {endereco}), "
                        f"no valor de R$ {valor}, vence em 5 dias ({vencimento}).")
            kit.sendwhatmsg_instantly(whatsapp, mensagem, 15, True)
            
            time.sleep(10)  # Aumenta o tempo de espera para garantir que a página tenha carregado
            pyautogui.click(200, 200)  # Clica no campo de texto do WhatsApp para garantir o foco
            time.sleep(2)  # Espera 2 segundos
            pyautogui.press('enter')  # Simula o pressionamento da tecla 'Enter' para enviar a mensagem

        elif dias_para_vencimento < 0:  # Cobrança de atraso
            mensagem = (f"Oi, {inquilino}! ⚠️ "
                        f"O aluguel da casa {casa} (Endereço: {endereco}), "
                        f"no valor de R$ {valor}, está atrasado desde {vencimento}. "
                        f"Por favor, regularize o pagamento.")
            kit.sendwhatmsg_instantly(whatsapp, mensagem, 15, True)
        
    elif status == "Atrasado":
            mensagem = (f"Oi, {inquilino}! ⚠️ "
                        f"O aluguel da casa {casa} (Endereço: {endereco}), "
                        f"no valor de R$ {valor}, está atrasado desde {vencimento}. "
                        f"Por favor, regularize o pagamento.")
            kit.sendwhatmsg_instantly(whatsapp, mensagem, 15, True)
            
            time.sleep(10)  # Aumenta o tempo de espera para garantir que a página tenha carregado
            pyautogui.click(200, 200)  # Clica no campo de texto do WhatsApp para garantir o foco
            time.sleep(2)  # Espera 2 segundos
            pyautogui.press('enter')  # Simula o pressionamento da tecla 'Enter' para enviar a mensagem