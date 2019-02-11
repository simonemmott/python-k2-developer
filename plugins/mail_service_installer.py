'''
Created on 10 Feb 2019

@author: simon
'''
from k2.service.local import LocalServiceInstaller
from k2.service.local import local_service


def plugin(app):
    app.logger.info('Installing {plugin}'.format(plugin=__name__))


@local_service()
class Installer(LocalServiceInstaller):
    
    def service(self):
        return {
            'name': 'email',
            'ref': 'sendmail',
            'title': 'Email Services',
            'description': 'This service sends emails via the sendmail service',
            'interface': {
                'name': 'k2.email',
                'title': 'K2 Email Service Type',
                'description': 'The interface of the K2 email service',
                'type': 'INTERFACE',
                'methods': [
                        {
                            'name': 'send_email',
                            'title': 'Send An Email Message',
                            'description': 'Send an email message synchronously or asynchronously with optional attachments',
                            'returns': 'None',
                            'return_type': {
                                'type': 'void'
                            },
                            'parameters': [
                                {
                                    'name': 'subject',
                                    'title': 'Subject',
                                    'description': 'The subject of the email message',
                                    'type': 'string',
                                    'required': True
                                },
                                {
                                    'name': 'sender',
                                    'title': 'Sender',
                                    'description': 'The email address of the sender',
                                    'type': 'string',
                                    'required': True
                                },
                                {
                                    'name': 'recipients',
                                    'title': 'Recipients',
                                    'description': 'The email address of the recipients',
                                    'type': 'array',
                                    'items': {
                                        'type': 'string'
                                    },
                                    'required': True
                                },
                                {
                                    'name': 'text_body',
                                    'title': 'Text Body',
                                    'description': 'The body of the email as text',
                                    'type': 'string',
                                    'required': True
                                },
                                {
                                    'name': 'html_body',
                                    'title': 'Html Body',
                                    'description': 'The body of the email as html',
                                    'type': 'string',
                                    'required': True
                                },
                                {
                                    'name': 'attachments',
                                    'title': 'Attachments',
                                    'description': 'The list of attachments to this email',
                                    'type': 'array',
                                    'items': {
                                        'type': 'k2.email.Attachment'
                                    },
                                    'required': False,
                                    'default': None
                                },
                                {
                                    'name': 'sync',
                                    'title': 'Synchronous',
                                    'description': 'Send the email synchronously or not',
                                    'type': 'boolean',
                                    'required': False,
                                    'default': {
                                        'type': 'boolean',
                                        'boolean_value': False
                                    }
                                }
                            ]
                        }
                    ]
                }
            }
        
    def configuration_labels(self):
        return []
    
    def source(self):
        return '''
from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body, attachments=None, sync=False):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)
    if sync:
        mail.send(msg)
    else:
        Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()
'''
