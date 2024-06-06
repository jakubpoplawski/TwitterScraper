import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders

from loggingSettings import logger_wrapper, logger_initialization

from portability import resource_path
import pathlib
import json


def load_settings():
    """The function loads the settings and creates saveback path.

    Args:
        None
    """

    with open(resource_path(pathlib.Path('Settings/settings.txt'))) as source:
        settings_dict = json.load(source) 

    result_filepath = resource_path(pathlib.Path('SaveBacks/twitter.csv'))
    log_filepath = resource_path(pathlib.Path('Settings/log_file.log'))

    return settings_dict, result_filepath, log_filepath


@logger_wrapper
def define_message(receiver, sender):
    """The function initialize the message.

    Args:
        receiver (str): Reciever's e-mail. 
        sender (str): Sender's e-mail.   
    """

    message = MIMEMultipart()
    message['Subject'] = 'Twitter latest'
    message['From'] = sender
    if type(receiver) == str:
        message['To'] = receiver
    else:
        message['To'] = ','.join(receiver)
    return message    

@logger_wrapper
def attach_file(message, filepath, file_name):
    """The function attaches the files to the message.

    Args:
        message (class): Reciever's e-mail. 
        filepath (str): Path to the attached file.
        file_name (str): Name for the attached file.  
    """

    part = MIMEBase('application', 'octet-stream')
    part.set_payload(open(filepath, 'rb').read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 
                    f'attachment; filename = "{file_name}"')
    message.attach(part)
    return message

@logger_wrapper
def send_message(message, user, password, sender, receiver):
    """The function logins into the e-mail account of the senders and 
    sends the message to the reciever.

    Args:
        message (class): Reciever's e-mail. 
        user (str): Login credentials.
        password (str): Login credentials.
        sender (str): Sender's e-mail.  
        receiver (str): Reciever's e-mail. 
    """

    send = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
    send.login(user, password)
    send.sendmail(sender, receiver, message.as_string())


def main():
    settings_dict, result_filepath, log_filepath = load_settings()

    logger = logger_initialization(settings_dict["log_name"])    
    logger.info('E-mail sending script started.')

    message = define_message(settings_dict['receiver'], 
                             settings_dict['email'])

    message = attach_file(message, 
                          result_filepath, 
                          settings_dict["result_name"])
    
    message = attach_file(message, 
                          log_filepath, 
                          settings_dict["log_name"])
    
    send_message(message, 
                 settings_dict["email"], 
                 settings_dict["email_password"],
                 settings_dict['email'],
                 settings_dict['receiver'])
    
    logger.info('E-mail sending script ended.')

if __name__ == "__main__":
    main()
