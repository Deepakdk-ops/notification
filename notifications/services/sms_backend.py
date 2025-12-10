class SMSBackend:
    def send(self, phone_number: str, message: str):
        # Integrate Twilio, AWS SNS, or your gateway here
        print(f"[SMS] To: {phone_number} | {message}")