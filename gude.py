#!/usr/bin/env python
from twilio.rest import Client
import json
import begin
import time
import logging
from envelopes import Envelope

@begin.subcommand
def send(cmd=r"%config get all"):
    j = json.load(open('credentials.json'))
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
    j = json.load(open('credentials.json'))
    c = Client(j['api_key'], j['api_secret'], j['account_sid'])

    replies = [m for m in c.messages.list() if m.direction == 'inbound']
    for r in replies:
        mail(r.body)
        try:
            r.delete()
        except:
            logging.exception("could not delete message:")


@begin.subcommand
def both():
    send()
    receive()



@begin.start
@begin.logging
def main():
    pass