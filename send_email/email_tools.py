import requests


def send_email(email_address, subject, body=None, html=None, sender='Daily papers'):
    data={"from": f"{sender} <postmaster@sandbox07032089b08247aa96d70d18b803e1d7.mailgun.org>",
          "to": email_address,
          "subject": subject}
    
    if body is not None:
        data['text'] = body
    if html is not None:
        data['html'] = html
        
    return requests.post(
        "https://api.mailgun.net/v3/sandbox07032089b08247aa96d70d18b803e1d7.mailgun.org/messages",
        auth=("api", "key-da44316443bf2723d2e165fd1158a7c7"),
        data=data)