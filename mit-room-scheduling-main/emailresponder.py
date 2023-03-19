import smtplib
import time
import imaplib
import email

emailaddress  = "fuukaasahina@gmail.com"
password    = "dragonnest"
smtpserver = "imap.gmail.com"
smtpport   = 993

try:
    mail = imaplib.IMAP4_SSL(smtpserver)
    mail.login(emailaddress,password)
    mail.select('inbox')

    type, data = mail.search(None, 'ALL')
    mail_ids = data[0]

    id_list = mail_ids.split()   
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])
    print latest_email_id
    print first_email_id
    typ, data = mail.fetch(latest_email_id, '(RFC822)' )
    for response_part in data:
        if isinstance(response_part, tuple):
            msg = email.message_from_string(response_part[1])
            emailresponse = msg['subject']
            emailadmin = msg['from']
            print 'From : ' + emailadmin + '\n'
            print 'Response: ' + emailresponse + '\n'
            status=emailresponse.split(",")[0]
            approvalid=emailresponse.split(",")[1] 
except Exception, e:
    print str(e)

if emailadmin=="Kevin Francisco <rkcfrancisco08@gmail.com>":
    if status=="Yes":
        print "Approved: "+str(approvalid)
    elif status=="No":
        print "Not Approved: "+str(approvalid)
    
    mail.store(str(latest_email_id), '+FLAGS', '\\Deleted')
    mail.expunge()
else:
    print "No latest message"
