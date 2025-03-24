from twilio.rest import Client
import random

class WhatsAppService:
    def __init__(self, account_sid, auth_token, twilio_number):
        self.client = Client(account_sid, auth_token)
        self.twilio_number = twilio_number

    def gerar_codigo(self):
        return str(random.randint(100000, 999999))  # Gera um código de 6 dígitos

    def enviar_codigo(self, numero_destino):
        codigo = self.gerar_codigo()
        mensagem = f"Seu código de ativação é: {codigo}"

        message = self.client.messages.create(
            from_=self.twilio_number,
            body=mensagem,
            to=f"whatsapp:{numero_destino}"
        )

        return {"codigo": codigo, "sid": message.sid}
