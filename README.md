# Cobrança de Inquilinos com WhatsApp e Google Sheets

Este projeto automatiza o envio de mensagens de cobrança para inquilinos via WhatsApp utilizando dados armazenados no Google Sheets. O programa verifica o status dos pagamentos, identifica aluguéis vencidos ou atrasados, e envia lembretes personalizados para cada inquilino.

## 🛠️ Tecnologias Utilizadas

- **Python**: Linguagem principal para o desenvolvimento.
- **Tkinter**: Para criar interfaces gráficas de inicialização e finalização.
- **Pandas**: Para manipulação e análise de dados.
- **PyWhatKit**: Para envio de mensagens no WhatsApp.
- **Google Sheets API**: Para integração com planilhas do Google.
- **gspread**: Biblioteca para trabalhar com Google Sheets.
- **OAuth2**: Para autenticação e autorização segura.

## 📋 Funcionalidades

1. **Verificação de Pagamentos**: 
   - Identifica aluguéis pendentes ou atrasados com base na data de vencimento.
   - Atualiza o status na planilha do Google Sheets.

2. **Envio de Mensagens pelo WhatsApp**:
   - Gera mensagens personalizadas com base no status de pagamento.
   - Envia as mensagens diretamente para o número do inquilino.

3. **Interface Gráfica**:
   - Exibe telas de inicialização e finalização para facilitar a interação do usuário.

4. **Controle de Cobranças**:
   - Evita cobranças repetidas em um intervalo de tempo definido.
   - Atualiza a data da última cobrança na planilha.

## 🖥️ Demonstração

1. Ao iniciar o programa, uma tela indica o início do processamento.
2. O script acessa a planilha do Google Sheets e processa os dados dos inquilinos.
3. Mensagens personalizadas são enviadas via WhatsApp para os inquilinos com status pendente ou atrasado.
4. Uma tela de finalização confirma o término do processamento.

## 📦 Estrutura do Código

- **Funções Principais**:
  - `mostrar_inicializacao()`: Exibe a interface inicial.
  - `realizar_processamento()`: Realiza a lógica principal de verificação e envio de mensagens.
  - `mostrar_finalizacao()`: Exibe a interface de finalização.

- **Lógica de Processamento**:
  - Lê dados da planilha do Google Sheets.
  - Verifica status de pagamentos e atualiza informações conforme necessário.
  - Envia mensagens personalizadas no WhatsApp para inquilinos.

## 🛡️ Segurança

- As credenciais do Google são armazenadas no arquivo `credenciais.json` e devem ser mantidas privadas.
- O envio de mensagens pelo WhatsApp utiliza a biblioteca `pywhatkit`, que requer a abertura do WhatsApp Web no navegador.

## 📚 Dependências

- **Pandas**: Manipulação e análise de dados.
- **PyWhatKit**: Envio de mensagens no WhatsApp.
- **Tkinter**: Interface gráfica.
- **gspread**: Integração com Google Sheets.
- **oauth2client**: Autenticação via OAuth2.
