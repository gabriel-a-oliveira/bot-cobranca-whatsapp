from datetime import datetime
import pandas as pd
import pywhatkit as kit
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import tkinter as tk

def centralizar_janela(root, largura, altura):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    pos_x = (screen_width // 2) - (largura // 2)
    pos_y = (screen_height // 2) - (altura // 2)
    root.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

def mostrar_inicializacao():
    root = tk.Tk()
    root.title("Cobrança inquilino")
    root.config(bg="#f0f8ff")
    
    largura = 300
    altura = 150
    centralizar_janela(root, largura, altura)

    title_label = tk.Label(root, text="Iniciando o Processamento...", font=("Helvetica", 14, "bold"), bg="#f0f8ff", fg="#4CAF50")
    title_label.pack(pady=20)
    
    root.after(2000, root.quit)
    root.mainloop()

def mostrar_finalizacao():
    root = tk.Tk()
    root.title("Cobrança inquilino")
    root.config(bg="#f0f8ff")
    
    largura = 300
    altura = 150
    centralizar_janela(root, largura, altura)

    title_label = tk.Label(root, text="Processamento Concluído!", font=("Helvetica", 14, "bold"), bg="#f0f8ff", fg="#4CAF50")
    title_label.pack(pady=20)
    
    confirm_button = tk.Button(root, text="OK", command=root.quit, font=("Helvetica", 12), bg="#4CAF50", fg="white", relief="solid", borderwidth=2, width=10)
    confirm_button.pack()
    
    root.mainloop()

def realizar_processamento():
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    credentials_path = "./credenciais.json" 
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scopes)
    cliente = gspread.authorize(credentials)

    planilha_google = cliente.open("CobrançaInquilino").sheet1

    dados = planilha_google.get_all_records()
    planilha = pd.DataFrame(dados)


    def gerar_mensagem(status, inquilino, casa, endereco, valor, vencimento):
        if status == "Pendente":
            mensagem = (f"Olá, *{inquilino}*! 😊\n\n"
                        f"Esse é um lembrete de que o aluguel da casa "
                        f"(Endereço: {endereco}) no valor de *{valor}*, *vence hoje ({vencimento})*.\n\n"
                        f"Por favor, não se esqueça de realizar o pagamento. Caso já tenha feito, desconsidere esta mensagem.")
            
        elif status == "Atrasado":
            mensagem = (f"Oi, *{inquilino}*! ⚠️\n\n"
                            f"Infelizmente, o aluguel da casa {casa} (Endereço: {endereco}) "
                            f"no valor de *{valor}* está atrasado desde *{vencimento}*. \n\n"
                            f"Pedimos, por gentileza, que regularize o pagamento o quanto antes para evitar inconvenientes.\n\n"
                            f"Agradecemos pela sua atenção e compreensão.")
        
        return mensagem

    def enviar_mensagem_whatsapp_instantaneamente (whatsapp, mensagem):
        kit.sendwhatmsg_instantly(whatsapp, mensagem, 15, True)
        time.sleep(3)

    def pode_enviar_cobranca(ultima_cobranca, dias_permitidos=2):
        if ultima_cobranca:
            ultima_cobranca_date = datetime.strptime(ultima_cobranca, "%d/%m/%Y").date()
            dias_desde_ultima_cobranca = (datetime.now().date() - ultima_cobranca_date).days
            return dias_desde_ultima_cobranca >= dias_permitidos
            
        return True

    def atualizar_ultima_cobranca(linha, ultima_cobranca_data):
        planilha_google.update_cell(linha, planilha.columns.get_loc("Última Cobrança") + 1, ultima_cobranca_data)

    def atualizar_status(linha, novo_status):
        planilha_google.update_cell(linha, planilha.columns.get_loc("Status") + 1, novo_status)

    for _, linha in planilha.iterrows():
        casa = linha['Casa']
        inquilino = linha['Inquilino']
        whatsapp = str(linha['WhatsApp'])
        endereco = linha['Endereço']
        valor = linha['Valor']
        vencimento = linha['Vencimento']
        status = linha['Status']
        ultima_cobranca = linha.get('Última Cobrança', None)
        
        whatsapp = "+55" + whatsapp.strip()
        vencimento_date = datetime.strptime(vencimento, "%d/%m/%Y").date()
        dias_para_vencimento = (vencimento_date - datetime.now().date()).days

        if dias_para_vencimento < 0 and status != "Atrasado":
            atualizar_status(_ + 2, "Atrasado")

        if status == "Pendente" and dias_para_vencimento == 0 and pode_enviar_cobranca(ultima_cobranca):
            mensagem = gerar_mensagem(status, inquilino, casa, endereco, valor, vencimento)
            enviar_mensagem_whatsapp_instantaneamente(whatsapp, mensagem)
            atualizar_ultima_cobranca(_ + 2, datetime.now().strftime("%d/%m/%Y"))

        elif status == "Atrasado" and dias_para_vencimento < 0 and pode_enviar_cobranca(ultima_cobranca):
                mensagem = gerar_mensagem(status, inquilino, casa, endereco, valor, vencimento)
                enviar_mensagem_whatsapp_instantaneamente(whatsapp, mensagem)
                atualizar_ultima_cobranca(_ + 2, datetime.now().strftime("%d/%m/%Y"))

if __name__ == "__main__":
    mostrar_inicializacao()
    realizar_processamento()
    mostrar_finalizacao()
    