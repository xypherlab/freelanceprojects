from PyQt4 import QtGui, QtCore
import sys
import time
import numpy as np
import pandas as pd
import os
import smtplib
import datetime
import imaplib
import email
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email import encoders
#import serial
#ser=serial.Serial('COM9',115200,timeout=1)
class Main(QtGui.QMainWindow):
    def __init__(self,parent=None):
        super(Main, self).__init__(parent)
        QtGui.QMainWindow.__init__(self)
        self.initUI()

    def initUI(self):
        global start_time,testflag
        testflag=0
        start_time = time.time()
        self.setWindowTitle("LABORATORY ROOM RESERVATION")
        centralwidget = QtGui.QWidget(self)
        self.setGeometry(500,100,500,400)
        self.infodisp=QtGui.QLabel("	    LABORATORY ROOM RESERVATION	",self)
        self.infodisp.move(10,80)
        self.infodisp.setStyleSheet('color: black')
        self.infodisp.resize(500,50)
        font = QtGui.QFont("Times", 14)
        self.infodisp.setFont(font)
       
        self.register = QtGui.QPushButton("Register",self)
        self.register.clicked.connect(self.registerfunc)
     
        self.register.move(200,210)
        
        self.registerpage = registergui(self)
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.Loop)
        self.timer.start()
        self.mainpage = maingui(self)
    def Loop(self):
        global start_time,testflag
        elapsed_time = time.time() - start_time
        
        try:
            idauthentication=ser.readline()
            #print idauthentication
            
            if idauthentication.split(" ")[2]=="UID" and idauthentication.split(" ")[3]=="Value:":
                endid=idauthentication.split(" ")[7]
                endid=endid.replace("\r\n", "")
                
                dataid=idauthentication.split(" ")[4]+" "+idauthentication.split(" ")[5]+" "+idauthentication.split(" ")[6]+" "+endid
                print dataid
                adminid="0x54 0x8B 0x62 0x8B"
                if adminid==dataid:
                    self.mainpage.exec_()
           
                
        except:
            x=0
        if elapsed_time>=30:
            emailaddress  = "fuukaasahina@gmail.com"
            password    = "dragonnest"
            smtpserver = "imap.gmail.com"
            smtpport   = 993
            start_time = time.time()
            
            
            
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

            if emailadmin=="Kevin Francisco <rkcfrancisco08@gmail.com>": #Adviser Email
                if status=="Yes":
                    print "Approved: "+str(approvalid)
                    pathtarget="statusdatabase.csv"
                    if os.path.exists(pathtarget):
                             
                         df=pd.read_csv(pathtarget,names=['Reference','Date Applied','Adviser','Dean','ILMO','Lab Assistant','Status'],skiprows=1)
                         np_df = df.as_matrix()
                         targetdata=np.where(df["Reference"] == int(approvalid))
                         targetdata=targetdata[0][0]
                         df.loc[targetdata,'Adviser'] = "Approve"
                         df.to_csv(pathtarget,  index = False)
                         print df
                elif status=="No":
                    
                    print "Not Approved: "+str(approvalid)
                    pathtarget="statusdatabase.csv"
                    if os.path.exists(pathtarget):
                             
                         df=pd.read_csv(pathtarget,names=['Reference','Date Applied','Adviser','Dean','ILMO','Lab Assistant','Status'],skiprows=1)
                         np_df = df.as_matrix()
                         targetdata=np.where(df["Reference"] == int(approvalid))
                         targetdata=targetdata[0][0]
                         df.loc[targetdata,'Adviser'] = "Deny"
                         df.to_csv(pathtarget,  index = False)
                         print df
                df=pd.read_csv(pathtarget,names=['Reference','Date Applied','Adviser','Dean','ILMO','Lab Assistant','Status'],skiprows=1)
                np_df = df.as_matrix()
                if np_df[targetdata][2]=="Approve" and np_df[targetdata][3]=="Approve" and np_df[targetdata][4]=="Approve" and np_df[targetdata][5]=="Approve":
                     
                     df.loc[targetdata,'Status'] = "Approved"
                     df.to_csv(pathtarget,  index = False)
                     print df
                     pathtarget="userdatabase.csv"
                     if os.path.exists(pathtarget):
                     
                        df=pd.read_csv(pathtarget,names=['ID','Name','Usertype','Student Number','Room','Time','Date','Program','Email'],skiprows=1)
                        np_df = df.as_matrix()
                        targetdata=np.where(df["ID"] == int(approvalid))
                        targetdata=targetdata[0][0]
                        emailtarget=np_df[targetdata][8]
                        roomrequest=np_df[targetdata][6]
                        timerequest=np_df[targetdata][5]
                        date=np_df[targetdata][4]
                        emailaddress  = "fuukaasahina@gmail.com"
                        emailpassword    = "dragonnest"
                        sent_from = emailaddress
                        to = [emailtarget]
                        subject="Subject: Room: "+roomrequest+" - Time: "+str(timerequest)+" - Date: "+str(date)
                        msg = "Your request has been approved."
                        email_text = "\r\n".join([
                        
                        subject,
                        "",
                        msg
                          ])
                        try:  
                            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                            server.ehlo()
                            server.login(emailaddress, emailpassword)
                            server.sendmail(sent_from, to, email_text)
                            server.close()

                            print 'Email sent!'
                        except:  
                            print 'Something went wrong...'
                elif np_df[targetdata][2]=="Deny"  and np_df[targetdata][3]!="----"and np_df[targetdata][4]!="----"and np_df[targetdata][5]!="----"or np_df[targetdata][3]=="Deny" and np_df[targetdata][2]!="----"and np_df[targetdata][4]!="----"and np_df[targetdata][5]!="----"or np_df[targetdata][4]=="Deny"and np_df[targetdata][3]!="----"and np_df[targetdata][2]!="----"and np_df[targetdata][5]!="----" or np_df[targetdata][5]=="Deny"and np_df[targetdata][3]!="----"and np_df[targetdata][4]!="----"and np_df[targetdata][2]!="----":
                     
                         df.loc[targetdata,'Status'] = "Denied"
                         df.to_csv(pathtarget,  index = False)
                         np_df = df.as_matrix()
                         print df
                if np_df[targetdata][6]=="Denied":
                    pathtarget="userdatabase.csv"
                    if os.path.exists(pathtarget):
                     
                        df=pd.read_csv(pathtarget,names=['ID','Name','Usertype','Student Number','Room','Time','Date','Program','Email'],skiprows=1)
                        np_df = df.as_matrix()
                        targetdata=np.where(df["ID"] == int(approvalid))
                        targetdata=targetdata[0][0]
                        emailtarget=np_df[targetdata][8]
                        roomrequest=np_df[targetdata][6]
                        timerequest=np_df[targetdata][5]
                        date=np_df[targetdata][4]
                        emailaddress  = "fuukaasahina@gmail.com"
                        emailpassword    = "dragonnest"
                        sent_from = emailaddress
                        to = [emailtarget]
                        subject="Subject: Room: "+roomrequest+" - Time: "+str(timerequest)+" - Date: "+str(date)
                        msg = "Your request has been denied."
                        email_text = "\r\n".join([
                        
                        subject,
                        "",
                        msg
                          ])
                        try:  
                            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                            server.ehlo()
                            server.login(emailaddress, emailpassword)
                            server.sendmail(sent_from, to, email_text)
                            server.close()

                            print 'Email sent!'
                        except:  
                            print 'Something went wrong...'
                mail.store(str(latest_email_id), '+FLAGS', '\\Deleted')
                mail.expunge()
            elif emailadmin=="Kevin Francisco <rkcfrancisco11@gmail.com>": #Dean Email
                if status=="Yes":
                    print "Approved: "+str(approvalid)
                    pathtarget="statusdatabase.csv"
                    if os.path.exists(pathtarget):
                             
                         df=pd.read_csv(pathtarget,names=['Reference','Date Applied','Adviser','Dean','ILMO','Lab Assistant','Status'],skiprows=1)
                         np_df = df.as_matrix()
                         targetdata=np.where(df["Reference"] == int(approvalid))
                         targetdata=targetdata[0][0]
                         df.loc[targetdata,'Dean'] = "Approve"
                         df.to_csv(pathtarget,  index = False)
                         print df
                elif status=="No":
                    print "Not Approved: "+str(approvalid)
                    pathtarget="statusdatabase.csv"
                    if os.path.exists(pathtarget):
                             
                         df=pd.read_csv(pathtarget,names=['Reference','Date Applied','Adviser','Dean','ILMO','Lab Assistant','Status'],skiprows=1)
                         np_df = df.as_matrix()
                         targetdata=np.where(df["Reference"] == int(approvalid))
                         targetdata=targetdata[0][0]
                         df.loc[targetdata,'Dean'] = "Deny"
                         df.to_csv(pathtarget,  index = False)
                         print df
                df=pd.read_csv(pathtarget,names=['Reference','Date Applied','Adviser','Dean','ILMO','Lab Assistant','Status'],skiprows=1)
                np_df = df.as_matrix()
                if np_df[targetdata][2]=="Approve" and np_df[targetdata][3]=="Approve" and np_df[targetdata][4]=="Approve" and np_df[targetdata][5]=="Approve":
                     
                     df.loc[targetdata,'Status'] = "Approved"
                     df.to_csv(pathtarget,  index = False)
                     print df
                     pathtarget="userdatabase.csv"
                     if os.path.exists(pathtarget):
                     
                        df=pd.read_csv(pathtarget,names=['ID','Name','Usertype','Student Number','Room','Time','Date','Program','Email'],skiprows=1)
                        np_df = df.as_matrix()
                        targetdata=np.where(df["ID"] == int(approvalid))
                        targetdata=targetdata[0][0]
                        emailtarget=np_df[targetdata][8]
                        roomrequest=np_df[targetdata][6]
                        timerequest=np_df[targetdata][5]
                        date=np_df[targetdata][4]
                        emailaddress  = "fuukaasahina@gmail.com"
                        emailpassword    = "dragonnest"
                        sent_from = emailaddress
                        to = [emailtarget]
                        subject="Subject: Room: "+roomrequest+" - Time: "+str(timerequest)+" - Date: "+str(date)
                        msg = "Your request has been approved."
                        email_text = "\r\n".join([
                        
                        subject,
                        "",
                        msg
                          ])
                        try:  
                            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                            server.ehlo()
                            server.login(emailaddress, emailpassword)
                            server.sendmail(sent_from, to, email_text)
                            server.close()

                            print 'Email sent!'
                        except:  
                            print 'Something went wrong...'
                elif np_df[targetdata][2]=="Deny"  and np_df[targetdata][3]!="----"and np_df[targetdata][4]!="----"and np_df[targetdata][5]!="----"or np_df[targetdata][3]=="Deny" and np_df[targetdata][2]!="----"and np_df[targetdata][4]!="----"and np_df[targetdata][5]!="----"or np_df[targetdata][4]=="Deny"and np_df[targetdata][3]!="----"and np_df[targetdata][2]!="----"and np_df[targetdata][5]!="----" or np_df[targetdata][5]=="Deny"and np_df[targetdata][3]!="----"and np_df[targetdata][4]!="----"and np_df[targetdata][2]!="----":
                     
                         df.loc[targetdata,'Status'] = "Denied"
                         df.to_csv(pathtarget,  index = False)
                         np_df = df.as_matrix()
                         print df
                if np_df[targetdata][6]=="Denied":
                    pathtarget="userdatabase.csv"
                    if os.path.exists(pathtarget):
                     
                        df=pd.read_csv(pathtarget,names=['ID','Name','Usertype','Student Number','Room','Time','Date','Program','Email'],skiprows=1)
                        np_df = df.as_matrix()
                        targetdata=np.where(df["ID"] == int(approvalid))
                        targetdata=targetdata[0][0]
                        emailtarget=np_df[targetdata][8]
                        roomrequest=np_df[targetdata][6]
                        timerequest=np_df[targetdata][5]
                        date=np_df[targetdata][4]
                        emailaddress  = "fuukaasahina@gmail.com"
                        emailpassword    = "dragonnest"
                        sent_from = emailaddress
                        to = [emailtarget]
                        subject="Subject: Room: "+roomrequest+" - Time: "+str(timerequest)+" - Date: "+str(date)
                        msg = "Your request has been denied."
                        email_text = "\r\n".join([
                        
                        subject,
                        "",
                        msg
                          ])
                        try:  
                            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                            server.ehlo()
                            server.login(emailaddress, emailpassword)
                            server.sendmail(sent_from, to, email_text)
                            server.close()

                            print 'Email sent!'
                        except:  
                            print 'Something went wrong...'
                mail.store(str(latest_email_id), '+FLAGS', '\\Deleted')
                mail.expunge()
            elif emailadmin=="Reynard Francisco <rkcfrancisco09@gmail.com>": #ILMO Email
                if status=="Yes":
                    print "Approved: "+str(approvalid)
                    pathtarget="statusdatabase.csv"
                    if os.path.exists(pathtarget):
                             
                         df=pd.read_csv(pathtarget,names=['Reference','Date Applied','Adviser','Dean','ILMO','Lab Assistant','Status'],skiprows=1)
                         np_df = df.as_matrix()
                         targetdata=np.where(df["Reference"] == int(approvalid))
                         targetdata=targetdata[0][0]
                         df.loc[targetdata,'ILMO'] = "Approve"
                         df.to_csv(pathtarget,  index = False)
                         print df
                elif status=="No":
                    print "Not Approved: "+str(approvalid)
                    pathtarget="statusdatabase.csv"
                    if os.path.exists(pathtarget):
                             
                         df=pd.read_csv(pathtarget,names=['Reference','Date Applied','Adviser','Dean','ILMO','Lab Assistant','Status'],skiprows=1)
                         np_df = df.as_matrix()
                         targetdata=np.where(df["Reference"] == int(approvalid))
                         targetdata=targetdata[0][0]
                         df.loc[targetdata,'ILMO'] = "Deny"
                         df.to_csv(pathtarget,  index = False)
                         print df
                df=pd.read_csv(pathtarget,names=['Reference','Date Applied','Adviser','Dean','ILMO','Lab Assistant','Status'],skiprows=1)
                np_df = df.as_matrix()
                if np_df[targetdata][2]=="Approve" and np_df[targetdata][3]=="Approve" and np_df[targetdata][4]=="Approve" and np_df[targetdata][5]=="Approve":
                     
                     df.loc[targetdata,'Status'] = "Approved"
                     df.to_csv(pathtarget,  index = False)
                     print df
                     pathtarget="userdatabase.csv"
                     if os.path.exists(pathtarget):
                     
                        df=pd.read_csv(pathtarget,names=['ID','Name','Usertype','Student Number','Room','Time','Date','Program','Email'],skiprows=1)
                        np_df = df.as_matrix()
                        targetdata=np.where(df["ID"] == int(approvalid))
                        targetdata=targetdata[0][0]
                        emailtarget=np_df[targetdata][8]
                        roomrequest=np_df[targetdata][6]
                        timerequest=np_df[targetdata][5]
                        date=np_df[targetdata][4]
                        emailaddress  = "fuukaasahina@gmail.com"
                        emailpassword    = "dragonnest"
                        sent_from = emailaddress
                        to = [emailtarget]
                        subject="Subject: Room: "+roomrequest+" - Time: "+str(timerequest)+" - Date: "+str(date)
                        msg = "Your request has been approved."
                        email_text = "\r\n".join([
                        
                        subject,
                        "",
                        msg
                          ])
                        try:  
                            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                            server.ehlo()
                            server.login(emailaddress, emailpassword)
                            server.sendmail(sent_from, to, email_text)
                            server.close()

                            print 'Email sent!'
                        except:  
                            print 'Something went wrong...'
                elif np_df[targetdata][2]=="Deny"  and np_df[targetdata][3]!="----"and np_df[targetdata][4]!="----"and np_df[targetdata][5]!="----"or np_df[targetdata][3]=="Deny" and np_df[targetdata][2]!="----"and np_df[targetdata][4]!="----"and np_df[targetdata][5]!="----"or np_df[targetdata][4]=="Deny"and np_df[targetdata][3]!="----"and np_df[targetdata][2]!="----"and np_df[targetdata][5]!="----" or np_df[targetdata][5]=="Deny"and np_df[targetdata][3]!="----"and np_df[targetdata][4]!="----"and np_df[targetdata][2]!="----":
                     
                         df.loc[targetdata,'Status'] = "Denied"
                         df.to_csv(pathtarget,  index = False)
                         np_df = df.as_matrix()
                         print df
                if np_df[targetdata][6]=="Denied":
                    pathtarget="userdatabase.csv"
                    if os.path.exists(pathtarget):
                     
                        df=pd.read_csv(pathtarget,names=['ID','Name','Usertype','Student Number','Room','Time','Date','Program','Email'],skiprows=1)
                        np_df = df.as_matrix()
                        targetdata=np.where(df["ID"] == int(approvalid))
                        targetdata=targetdata[0][0]
                        emailtarget=np_df[targetdata][8]
                        roomrequest=np_df[targetdata][6]
                        timerequest=np_df[targetdata][5]
                        date=np_df[targetdata][4]
                        emailaddress  = "fuukaasahina@gmail.com"
                        emailpassword    = "dragonnest"
                        sent_from = emailaddress
                        to = [emailtarget]
                        subject="Subject: Room: "+roomrequest+" - Time: "+str(timerequest)+" - Date: "+str(date)
                        msg = "Your request has been denied."
                        email_text = "\r\n".join([
                        
                        subject,
                        "",
                        msg
                          ])
                        try:  
                            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                            server.ehlo()
                            server.login(emailaddress, emailpassword)
                            server.sendmail(sent_from, to, email_text)
                            server.close()

                            print 'Email sent!'
                        except:  
                            print 'Something went wrong...'
                mail.store(str(latest_email_id), '+FLAGS', '\\Deleted')
                mail.expunge()
            elif emailadmin=="Reynard Francisco <rkcfrancisco10@gmail.com>": #Lab Assistant Email
                if status=="Yes":
                    print "Approved: "+str(approvalid)
                    pathtarget="statusdatabase.csv"
                    if os.path.exists(pathtarget):
                             
                         df=pd.read_csv(pathtarget,names=['Reference','Date Applied','Adviser','Dean','ILMO','Lab Assistant','Status'],skiprows=1)
                         np_df = df.as_matrix()
                         targetdata=np.where(df["Reference"] == int(approvalid))
                         targetdata=targetdata[0][0]
                         df.loc[targetdata,'Lab Assistant'] = "Approve"
                         df.to_csv(pathtarget,  index = False)
                         print df
                elif status=="No":
                    print "Not Approved: "+str(approvalid)
                    pathtarget="statusdatabase.csv"
                    if os.path.exists(pathtarget):
                             
                         df=pd.read_csv(pathtarget,names=['Reference','Date Applied','Adviser','Dean','ILMO','Lab Assistant','Status'],skiprows=1)
                         np_df = df.as_matrix()
                         targetdata=np.where(df["Reference"] == int(approvalid))
                         targetdata=targetdata[0][0]
                         df.loc[targetdata,'Lab Assistant'] = "Deny"
                         df.to_csv(pathtarget,  index = False)
                         print df
                df=pd.read_csv(pathtarget,names=['Reference','Date Applied','Adviser','Dean','ILMO','Lab Assistant','Status'],skiprows=1)
                np_df = df.as_matrix()
                if np_df[targetdata][2]=="Approve" and np_df[targetdata][3]=="Approve" and np_df[targetdata][4]=="Approve" and np_df[targetdata][5]=="Approve":
                     
                     df.loc[targetdata,'Status'] = "Approved"
                     df.to_csv(pathtarget,  index = False)
                     print df
                     pathtarget="userdatabase.csv"
                     if os.path.exists(pathtarget):
                     
                        df=pd.read_csv(pathtarget,names=['ID','Name','Usertype','Student Number','Room','Time','Date','Program','Email'],skiprows=1)
                        np_df = df.as_matrix()
                        targetdata=np.where(df["ID"] == int(approvalid))
                        targetdata=targetdata[0][0]
                        emailtarget=np_df[targetdata][8]
                        roomrequest=np_df[targetdata][6]
                        timerequest=np_df[targetdata][5]
                        date=np_df[targetdata][4]
                        emailaddress  = "fuukaasahina@gmail.com"
                        emailpassword    = "dragonnest"
                        sent_from = emailaddress
                        to = [emailtarget]
                        subject="Subject: Room: "+roomrequest+" - Time: "+str(timerequest)+" - Date: "+str(date)
                        msg = "Your request has been approved."
                        email_text = "\r\n".join([
                        
                        subject,
                        "",
                        msg
                          ])
                        try:  
                            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                            server.ehlo()
                            server.login(emailaddress, emailpassword)
                            server.sendmail(sent_from, to, email_text)
                            server.close()

                            print 'Email sent!'
                        except:  
                            print 'Something went wrong...'
                elif np_df[targetdata][2]=="Deny"  and np_df[targetdata][3]!="----"and np_df[targetdata][4]!="----"and np_df[targetdata][5]!="----"or np_df[targetdata][3]=="Deny" and np_df[targetdata][2]!="----"and np_df[targetdata][4]!="----"and np_df[targetdata][5]!="----"or np_df[targetdata][4]=="Deny"and np_df[targetdata][3]!="----"and np_df[targetdata][2]!="----"and np_df[targetdata][5]!="----" or np_df[targetdata][5]=="Deny"and np_df[targetdata][3]!="----"and np_df[targetdata][4]!="----"and np_df[targetdata][2]!="----":
                     
                         df.loc[targetdata,'Status'] = "Denied"
                         df.to_csv(pathtarget,  index = False)
                         np_df = df.as_matrix()
                         print df
                if np_df[targetdata][6]=="Denied":
                    pathtarget="userdatabase.csv"
                    if os.path.exists(pathtarget):
                     
                        df=pd.read_csv(pathtarget,names=['ID','Name','Usertype','Student Number','Room','Time','Date','Program','Email'],skiprows=1)
                        np_df = df.as_matrix()
                        targetdata=np.where(df["ID"] == int(approvalid))
                        targetdata=targetdata[0][0]
                        emailtarget=np_df[targetdata][8]
                        roomrequest=np_df[targetdata][6]
                        timerequest=np_df[targetdata][5]
                        date=np_df[targetdata][4]
                        emailaddress  = "fuukaasahina@gmail.com"
                        emailpassword    = "dragonnest"
                        sent_from = emailaddress
                        to = [emailtarget]
                        subject="Subject: Room: "+roomrequest+" - Time: "+str(timerequest)+" - Date: "+str(date)
                        msg = "Your request has been denied."
                        email_text = "\r\n".join([
                        
                        subject,
                        "",
                        msg
                          ])
                        try:  
                            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                            server.ehlo()
                            server.login(emailaddress, emailpassword)
                            server.sendmail(sent_from, to, email_text)
                            server.close()

                            print 'Email sent!'
                        except:  
                            print 'Something went wrong...'
                mail.store(str(latest_email_id), '+FLAGS', '\\Deleted')
                mail.expunge()
            else:
                print "No latest message"
                
    def loginfunc(self):
         
         self.loginpage.exec_()
    def registerfunc(self):
        self.registerpage.exec_()


class maingui(QtGui.QDialog):
    def __init__(self,parent=None):
        super(maingui, self).__init__(parent)
        self.setWindowTitle("Admin")
        self.setGeometry(490,70,500,400)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.viewsched = QtGui.QPushButton("Status",self)
        self.viewsched.clicked.connect(self.viewschedfunc)
        self.viewsched.move(120,175)
        #self.getfile = QtGui.QPushButton("Get File",self)
        #self.getfile.clicked.connect(self.getfilefunc)
        #self.getfile.move(220,175)
       
        self.logout = QtGui.QPushButton("Logout",self)
        self.logout.clicked.connect(self.logoutfunc)
        self.logout.move(320,175)
        self.schedpage = schedgui(self)
    def logoutfunc(self):
        self.close()

    def viewschedfunc(self):

        self.schedpage.exec_()
    #def getfilefunc(self):
        #fromaddr = "fuukaasahina@gmail.com"
        #toaddr = "rkcfrancisco08@gmail.com"
         
        #msg = MIMEMultipart()
         
        #msg['From'] = fromaddr
        #msg['To'] = toaddr
        #msg['Subject'] = "Report"
         
        #body = "Overall report as of 10-9-2018."
         
        #msg.attach(MIMEText(body, 'plain'))
         
        #filename = "roomdatabase.csv"
        #attachment = open("C:/Users/ADMIN/Desktop/Workspace/Room Scheduling", "rb")
         
        #part = MIMEBase('application', 'octet-stream')
        #part.set_payload((attachment).read())
        #encoders.encode_base64(part)
        #part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
         
        #msg.attach(part)
         
        #server = smtplib.SMTP('smtp.gmail.com', 587)
        #server.starttls()
        #server.login(fromaddr, "dragonnest")
        #text = msg.as_string()
        #server.sendmail(fromaddr, toaddr, text)
        #server.quit()
class schedgui(QtGui.QDialog):
    def __init__(self,parent=None):
        super(schedgui, self).__init__(parent)
        self.setWindowTitle("Room Schedule")
        self.setGeometry(390,70,700,600)
        self.table = QtGui.QTableWidget(self)
        self.table.setColumnCount(7)
        self.table.move(50,50)
        self.table.setHorizontalHeaderLabels(['     Reference       ','     Date Applied      ','     Adviser    ','      Dean        ','         ILMO        ','         Lab Assistant          ','         Status          '])
        self.table.resize(600,400)
        self.table.resizeColumnsToContents()
        self.table.verticalHeader().setVisible(0)
        pathtarget="statusdatabase.csv"
        if os.path.exists(pathtarget):
                     
             df=pd.read_csv(pathtarget,names=['Reference','Date Applied','Adviser','Dean','ILMO','Lab Assistant','Status'],skiprows=1)
             np_df = df.as_matrix()
             cnt=0
            
             self.table.setRowCount(len(np_df))
         
             for i in xrange(len(np_df)):
                     self.table.setItem(cnt, 0, QtGui.QTableWidgetItem(""+str(np_df[cnt][0])+""))
                     self.table.setItem(cnt, 1, QtGui.QTableWidgetItem(""+str(np_df[cnt][1])+""))
                     self.table.setItem(cnt, 2, QtGui.QTableWidgetItem(""+str(np_df[cnt][2])+""))
                     self.table.setItem(cnt, 3, QtGui.QTableWidgetItem(""+str(np_df[cnt][3])+""))
                     self.table.setItem(cnt, 4, QtGui.QTableWidgetItem(""+str(np_df[cnt][4])+""))
                     self.table.setItem(cnt, 5, QtGui.QTableWidgetItem(""+str(np_df[cnt][5])+""))
                     self.table.setItem(cnt, 6, QtGui.QTableWidgetItem(""+str(np_df[cnt][6])+""))
                     cnt=cnt+1
class registergui(QtGui.QDialog):
    def __init__(self,parent=None):
        super(registergui, self).__init__(parent)
        self.setWindowTitle("REGISTER")
        self.setGeometry(390,72,550,550)
        font10 = QtGui.QFont("Helvetica", 10)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.l1=QtGui.QLabel("Name:",self)
        self.l1.move(80,75)
        self.l1.setFont(font10)
        self.l2=QtGui.QLineEdit(self)
        self.l2.move(160,75)
        self.l2.resize(250,20)
        self.l3=QtGui.QLabel("Program:",self)
        self.l3.move(80,105)
        self.l3.setFont(font10)
        self.l4=QtGui.QLineEdit(self)
        self.l4.move(160,105)
        self.l4.resize(250,20)
        self.l5=QtGui.QLabel("User Type:",self)
        self.l5.move(80,135)
        self.l5.setFont(font10)
        self.l6=QtGui.QLabel("Student No.:",self)
        self.l6.move(80,165)
        self.l6.setFont(font10)
        self.l7=QtGui.QLineEdit(self)
        self.l7.move(160,165)
        self.l7.resize(250,20)
        self.l8=QtGui.QLabel("Date:",self)
        self.l8.move(80,195)
        self.l8.setFont(font10)
        self.l9=QtGui.QLineEdit(self)
        self.l9.move(160,195)
        self.l9.resize(250,20)
        self.l10=QtGui.QLabel("Email Address:",self)
        self.l10.move(80,225)
        self.l10.setFont(font10)
        self.l11=QtGui.QLineEdit(self)
        self.l11.move(180,225)
        self.l11.resize(230,20)
        self.l12=QtGui.QLabel("Purpose:",self)
        self.l12.move(80,285)
        self.l12.setFont(font10)
        self.l13=QtGui.QLineEdit(self)
        self.l13.move(160,285)
        self.l13.resize(250,20)
        self.l14=QtGui.QLabel("Equipment:",self)
        self.l14.move(80,315)
        self.l14.setFont(font10)
        self.l15=QtGui.QLineEdit(self)
        self.l15.move(160,315)
        self.l15.resize(250,20)
        self.l16=QtGui.QLabel("Adviser:",self)
        self.l16.move(80,345)
        self.l16.setFont(font10)
        self.l17=QtGui.QLabel("Dean:",self)
        self.l17.move(80,375)
        self.l17.setFont(font10)
        self.l18=QtGui.QLabel("Lab Assistant:",self)
        self.l18.move(80,405)
        self.l18.setFont(font10)
        self.l20=QtGui.QLabel("ILMO:",self)
        self.l20.move(80,435)
        self.l20.setFont(font10)
        self.l19=QtGui.QLabel("Room:",self)
        self.l19.move(80,255)
        self.l19.setFont(font10)
        self.l21=QtGui.QLabel("Time:",self)
        self.l21.move(310,255)
        self.l21.setFont(font10)
        self.roomtype = QtGui.QComboBox(self)
        #Room
        self.roomtype.addItems(["","NW315","S305"])
        self.roomtype.currentIndexChanged.connect(self.roomselect)
        self.roomtype.move(160,255)
        self.roomtype.resize(140,20)
        ##############
        self.timechoice = QtGui.QComboBox(self)
        self.timechoice.addItems(["","7:30 AM","9:00 AM","10:30 AM","12:00 PM","1:30 PM","3:00 PM","4:30 PM","6:00 PM","7:30 PM"])
        self.timechoice.currentIndexChanged.connect(self.timeselect)
        self.timechoice.move(350,255)
        self.timechoice.resize(140,20)
        
        self.usertype = QtGui.QComboBox(self)
        self.usertype.addItems(["","STUDENT","NONSTUDENT"])
        self.usertype.currentIndexChanged.connect(self.typeselect)
        self.usertype.move(160,135)
        self.usertype.resize(140,20)
        #Email Selection
        self.adviserchoice = QtGui.QComboBox(self)
        self.adviserchoice.addItems(["","ADVISER A","ADVISER B"])
        self.adviserchoice.currentIndexChanged.connect(self.adviserselect)
        self.adviserchoice.move(160,345)
        self.adviserchoice.resize(140,20)

        self.deanchoice = QtGui.QComboBox(self)
        self.deanchoice.addItems(["","DEAN A","DEAN B"])
        self.deanchoice.currentIndexChanged.connect(self.deanselect)
        self.deanchoice.move(160,375)
        self.deanchoice.resize(140,20)

        self.labassistantchoice = QtGui.QComboBox(self)
        self.labassistantchoice.addItems(["","LAB ASSISTANT A","LAB ASSISTANT B"])
        self.labassistantchoice.currentIndexChanged.connect(self.labassistantselect)
        self.labassistantchoice.move(180,405)
        self.labassistantchoice.resize(120,20)

        self.ilmochoice = QtGui.QComboBox(self)
        self.ilmochoice.addItems(["","ILMO A","ILMO B"])
        self.ilmochoice.currentIndexChanged.connect(self.ilmoselect)
        self.ilmochoice.move(180,435)
        self.ilmochoice.resize(120,20)
        ########################
        self.request = QtGui.QPushButton("Send",self)
        self.request.clicked.connect(self.requestfunc)
        self.request.move(200,465)

        
    def requestfunc(self):
        global roomrequest,adviseremail,deanemail,labassistantemail,usertype,ilmoemail,timerequest
        emailaddress  = "fuukaasahina@gmail.com"
        emailpassword    = "dragonnest"
        sent_from = emailaddress
        name=str(self.l2.text())
        studentnumber=str(self.l7.text())
        date=str(self.l9.text())
        program=str(self.l4.text())
        email=str(self.l11.text())
        purpose=str(self.l13.text())
        equipment=str(self.l15.text())
        to = [adviseremail,deanemail,labassistantemail,ilmoemail]
        pathtarget="statusdatabase.csv"
        if os.path.exists(pathtarget):
                     
             df=pd.read_csv(pathtarget,names=['Reference','Date Applied','Adviser','Dean','ILMO','Lab Assistant','Status'],skiprows=1)
             np_df = df.as_matrix()
             idnumber=len(df.index)
             df = df.append({'Reference':str(idnumber),'Date Applied':str(datetime.datetime.now()),'Adviser':"----",'Dean':"----",'ILMO':"----",'Lab Assistant':"----",'Status':"----"}, ignore_index=True)
             df.to_csv(pathtarget,  index = False)
             print df
        else:
             
             columns = ['Reference','Date Applied','Adviser','Dean','ILMO','Lab Assistant','Status']
             df = pd.DataFrame(columns=columns)
             np_df = df.as_matrix()
             idnumber=0
             df = df.append({'Reference':str(idnumber),'Date Applied':str(datetime.datetime.now()),'Adviser':"----",'Dean':"----",'ILMO':"----",'Lab Assistant':"----",'Status':"----"}, ignore_index=True)
             df.to_csv(pathtarget,  index = False)
             print df  
        subject="Subject: Room: "+roomrequest+" - Time: "+str(timerequest)+" - Reference No. "+str(idnumber)
        msg = "Purpose: "+purpose+"\n\n"+"Equipment: "+equipment
        email_text = "\r\n".join([
        
        subject,
        "",
        msg
          ])
        try:  
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.ehlo()
            server.login(emailaddress, emailpassword)
            server.sendmail(sent_from, to, email_text)
            server.close()

            print 'Email sent!'
        except:  
            print 'Something went wrong...'
        pathtarget="userdatabase.csv"
        if os.path.exists(pathtarget):
                     
             df=pd.read_csv(pathtarget,names=['ID','Name','Usertype','Student Number','Room','Time','Date','Program','Email'],skiprows=1)
             np_df = df.as_matrix()
             idnumber=len(df.index)
             df = df.append({'ID':str(idnumber),'Name':name,'Usertype':usertype,'Student Number':studentnumber,'Room':roomrequest,'Time':timerequest,'Date':date,'Program':program,'Email':email}, ignore_index=True)
             df.to_csv(pathtarget,  index = False)
             print df
        else:
             
             columns = ['ID','Name','Usertype','Student Number','Room','Time','Date','Program','Email']
             df = pd.DataFrame(columns=columns)
             np_df = df.as_matrix()
             
             df = df.append({'ID':"0",'Name':name,'Usertype':usertype,'Student Number':studentnumber,'Room':roomrequest,'Time':timerequest,'Date':date,'Program':program,'Email':email}, ignore_index=True)
             df.to_csv(pathtarget,  index = False)
             print df
        
        self.close()
        
    def typeselect(self,ax):
        global usertype
        if ax==1:
            print "Student"
            usertype="Student"
        elif ax==2:
            print "Non Student"
            usertype="Non Student"
    #Categories 
    def adviserselect(self,bx):
        global adviseremail
        if bx==1:
            print "Adviser A"
            adviseremail="rkcfrancisco09@gmail.com"
        elif bx==2:
            print "Adviser B"
    def deanselect(self,cx):
        global deanemail
        if cx==1:
            print "Dean A"
            deanemail="rkcfrancisco10@gmail.com"
        elif cx==2:
            print "Dean B"
    def ilmoselect(self,fx):
        global ilmoemail
        if fx==1:
            print "ILMO A"
            ilmoemail="rkcfrancisco08@gmail.com"
        elif fx==2:
            print "ILMO B"
            
    def labassistantselect(self,dx):
        global labassistantemail
        if dx==1:
            print "Lab Assistant A"
            labassistantemail="rkcfrancisco11@gmail.com"
        elif dx==2:
            print "Lab Assistant B"

    ##############

    #Room
    def roomselect(self,ex):
        global roomrequest
        if ex==1:
            print "NW315"
            roomrequest="NW315"
        elif ex==2:
            print "S305"
            roomrequest="S305"
    ###########
    def timeselect(self,gx):
        global timerequest
        if gx==1:
            print "7:30 AM"
            timerequest="7:30 AM"
        elif gx==2:
            print "9:00 AM"
            timerequest="9:00 AM"
        elif gx==3:
            print "10:30 AM"
            timerequest="10:30 AM"
        elif gx==4:
            print "12:00 PM"
            timerequest="12:00 PM"
        elif gx==5:
            print "1:30 PM"
            timerequest="1:30 PM"
        elif gx==6:
            print "3:00 PM"
            timerequest="3:00 PM"
        elif gx==7:
            print "4:30 PM"
            timerequest="4:30 PM"
        elif gx==8:
            print "6:00 PM"
            timerequest="6:00 PM"
        elif gx==9:
            print "7:30 PM"
            timerequest="7:30 PM"
def main():
    app = QtGui.QApplication(sys.argv)
    main= Main()
    main.show()
 
    sys.exit(app.exec_())
 
if __name__ == "__main__":
    main()
