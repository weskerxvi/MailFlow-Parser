def email_reader():
    with open('emails.txt', 'r', encoding='utf-8') as file:
        return file.read()