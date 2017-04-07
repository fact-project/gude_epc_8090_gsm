#!/usr/bin/env python
from twilio.rest import Client
import json
import begin
import time
import logging
from envelopes import Envelope

import os

os.path.realpath(__file__)

def config():
    config_path = os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        'credentials.json')
    return json.load(open(config_path))

@begin.subcommand
def send(cmd=r"%config get all"):
    j = config()
    c = Client(j['api_key'], j['api_secret'], j['account_sid'])
    m = c.messages.create(to=j['gudenumber'], from_=j['fromnumber'], body=cmd)
    start = time.time()
    while True:
        time.sleep(2)
        try:
            m.delete()
        except:
            pass
        else:
            break
    logging.debug("message sent.")


def mail(body):
    try:
        Envelope(
            to_addr="neised@phys.ethz.ch",
            from_addr="dneise@fact-project.org",
            subject="Gude EPC SMS keep alve",
            text_body=body
        ).send(
            host='gate',
            port=25,
            tls=False,
            timeout=20
        )
    except:
        logging.exception("Could not send email:")


@begin.subcommand
def receive():
    j = config()
    c = Client(j['api_key'], j['api_secret'], j['account_sid'])

    ms = c.messages.list()
    replies = [m for m in ms if m.direction == 'inbound']
    for r in replies:
        mail(r.body)
        try:
            r.delete()
        except:
            logging.exception("could not delete message:")

@begin.subcommand
def delete():
    j = config()
    c = Client(j['api_key'], j['api_secret'], j['account_sid'])
    ms = c.messages.list()
    for m in ms:
        m.delete()

@begin.subcommand
def print():
    j = config()
    c = Client(j['api_key'], j['api_secret'], j['account_sid'])
    ms = c.messages.list()
    for m in ms:
        logging.info(vars(m))


@begin.subcommand
def both():
    send()
    time.sleep(30)
    receive()


@begin.start
@begin.logging
def main():
    pass
