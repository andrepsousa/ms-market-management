from twilio.rest import Client
import random
from dotenv import load_dotenv  # Corrigido aqui
import os

# Carrega as variáveis de ambiente do .env
load_dotenv()

# Obtém as credenciais do Twilio a partir das variáveis de ambiente
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_PHONE_NUMBER")


class WhatsAppService:
    def __init__(self):
        self.account_sid = 'AC414bf889a4c7b481bc78a65b64d238f2'
        self.auth_token = '486a00f7c1d0d97728b3729ac1aa483a'
        self.twilio_number = 'whatsapp:+14155238886'
        self.client = Client(self.account_sid, self.auth_token)

    def enviar_codigo(self, numero_destino, codigo):
        """Envia o código de ativação para o número via WhatsApp"""
        mensagem = f"Seu código de ativação é: {codigo}"

        # Envia a mensagem via Twilio WhatsApp
        message = self.client.messages.create(
            from_=self.twilio_number,
            body=mensagem,
            to=f"whatsapp:{numero_destino}"
        )
        
        print(message)
        # Retorna o código gerado e o SID da mensagem
        return {"codigo": codigo, "sid": message.sid}