from src.Infrastructure.http.whats_app import WhatsAppService

whatsapp_service = WhatsAppService()
whatsapp_service.enviar_codigo("+5511999999999", "1234")