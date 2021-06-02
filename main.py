from SMTPClient import SMTPClient
from GetConfigs import GetConfigs

if __name__ == '__main__':
    configs = GetConfigs("attachments/mail-config.yml")
    smtp_client = SMTPClient("mail.smtp2go.com", "YOUR-LOGIN",
                             "YOUR-PASSWORD", "RECEIVER")

    smtp_client.add_text_plain(configs.text_plain)
    smtp_client.add_text_html(configs.text_html)
    smtp_client.add_file_attachment(configs.attachment)
    smtp_client.send_email(configs.receiver, configs.subject)
