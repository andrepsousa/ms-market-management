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
    def __init__(self, account_sid, auth_token, twilio_number):
        self.client = Client(account_sid, auth_token)
        self.twilio_number = twilio_number

    def gerar_codigo(self):
        """Gera um código de 4 dígitos"""
        return str(random.randint(1000, 9999))

    def enviar_codigo(self, numero_destino):
        """Envia o código de ativação para o número via WhatsApp"""
        codigo = self.gerar_codigo()
        mensagem = f"Seu código de ativação é: {codigo}"

        # Envia a mensagem via Twilio WhatsApp
        message = self.client.messages.create(
            from_=self.twilio_number,
            body=mensagem,
            to=f"whatsapp:{numero_destino}"
        )
        
        # Retorna o código gerado e o SID da mensagem
        return {"codigo": codigo, "sid": message.sid}
