# gude_epc_8090_gsm
script to keep SIM card in FACT Gude EPC active by requesting monthly report

FACT uses several network power switches by [Gude](https://www.gude.info/en/home.html)
to remotely control lines power for the major system components like:

 * computers
 * camera power supplies
 * cooling pump
 * surveillance cameras

Gude calls these devices "Expert Power Control" hence the abbreviation EPC.

The EPC controlling the main network gateway PC power is equipped with a GSM
module and can be controlled via SMS.

The device is a Gude EPC 8090, the [manual](doc/manual-epc8090.pdf) is stored
within this repository for later reference.

Apart from this documentation this repository contains a software capable of
making monthly requests to the EPC 8090 in order to keep the SIM card provider happy.

## Monthly Gude SMS Requester

Requests the EPC Status *once per month* and relays it via email to fact-online
This is one spam-like mail, as nobody will be interested in it,
per month, maybe ok.

The requester uses the ETH [Twilio](https://www.twilio.com/) account for sending and receiving
SMS. Email will be sent via the SMTP server on the FACT gateway PC.

We will try to at least show the balance of the prepaid SIM card, so that it
can be recharged when needed. (At the moment this is not yet possible)


I would like to keep this repo simple and let it contain all relevant information
including a picture of the SIM card package with:
 * PIN and PUK
 * provider information
 * twilio credentials
 * GUDE switch master and port passwords

But then again, not all FACT members (want to have) github accounts in
order to take part in this venture.

So as with other repos, this might be split into two repos, one just containing the
credentials.

## Installation and Usage

  To install this, clone it, install the requirements, enter the credentials, and call it e.g. using cron:
  
  * git clone https://github.com/fact-project/gude_epc_8090_gsm.git
  * cd gude_epc_8090_gsm
  * pip install -r requierements.txt
  * cp credentials.json_template credentials.json
  * vi credentials.json  # enter the twilio keys and phone numbers and so on
  * crontab -e 

At the moment this setup is checked out on `newdaq` and my (dneises) crontag line for this looks like this:

    0 10 1 * * /home/dneise/gude_epc_8090_gsm/gude.py send_and_receive

So it will be called every 1st of a month at 10am. It will send an email to the FACT mailing list with content like this:

    Device name: FACT-computer 
    Config Status:
    COD=Off,TB=Off,ST=On,MAIL=Off,TEMP=Off,RESP=On,ERR=On,PN=On,FC=Off,MGSM=Off,ASYN=On,GSM=On,CTON=Off,CVOI=Off,ANUM=+41774528842,TMIN=0,TMAX=0
    Contract SIM Card
    Temperature: 26.4 C

The contents are actually irrelevant, but we have to use a SIM card a bit, so this communication should be enough.
