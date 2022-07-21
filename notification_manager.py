from twilio.rest import Client

ACCOUNT_SID = "ACbb5fe55657e67c77a74de2b721985f53"
AUTH_TOKEN = "ef77490674686da58f602685b99395e8"

class NotificationManager:
    def __init__(self):
        self.client = Client(ACCOUNT_SID, AUTH_TOKEN)

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_='+18304520698',
            to='+48883965983'
        )

        print(message.status)
