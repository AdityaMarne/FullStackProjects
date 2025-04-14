def send_password_reset_email(email, reset_link):
     # You would replace this with Flask-Mail or an SMTP provider
    print(f"[EMAIL MOCK] To: {email} — Reset Link: {reset_link}")

def send_verification_email(email, link):
     print(f"[EMAIL MOCK] To: {email} — Verify your account: {link}")
