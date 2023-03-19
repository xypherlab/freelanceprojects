#imports
from flask import Flask, render_template, request
import nltk
import os
import pandas as pd
print("####################NLTK VERSION#################"+str(nltk.__version__))


from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
#nltk.download('punkt')
#nltk.download('wordnet')
import pickle
import numpy as np
from keras import backend as K
from keras.models import load_model
print(K.backend())
model = load_model('chatbot_model.h5')
import json
import random
intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))

app = Flask(__name__, template_folder='template')

#define app routes
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get")
#function for the bot response
def get_bot_response():
    #userText = request.args.get('msg')
    def clean_up_sentence(sentence):
        sentence_words = nltk.word_tokenize(sentence)
        sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
        return sentence_words

    # return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

    def bow(sentence, words, show_details=True):
        # tokenize the pattern
        sentence_words = clean_up_sentence(sentence)
        # bag of words - matrix of N words, vocabulary matrix
        print(sentence_words)
        bag = [0]*len(words)
        for s in sentence_words:
            for i,w in enumerate(words):
                if w == s:
                    # assign 1 if current word is in the vocabulary position
                    bag[i] = 1
                    if show_details:
                        print ("found in bag: %s" % w)
        return(np.array(bag))

    def predict_class(sentence, model):
        # filter out predictions below a threshold
        p = bow(sentence, words,show_details=True)
        res = model.predict(np.array([p]))[0]
        ERROR_THRESHOLD = 0.25
        results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
        # sort by strength of probability
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
        return return_list

    def getResponse(ints, intents_json):
        tag = ints[0]['intent']
        list_of_intents = intents_json['intents']
        for i in list_of_intents:
            if(i['tag']== tag):
                result = random.choice(i['responses'])
                break
        return result

    def chatbot_response(msg):
        ints = predict_class(msg, model)
        res = getResponse(ints, intents)
        
        return res
    userText = request.args.get('msg')
    print("User Message: "+userText)
    print(str(chatbot_response(str(userText))))
    
    if str(chatbot_response(str(userText)))=="FEU - Institute of Technology Floor Directory":
        a = pd.read_csv("floordirectory.csv")
        html_file = a.to_html()
        datasent=html_file
        #datasent="FEU - Institute of Technology Floor Directory"
    elif str(chatbot_response(str(userText)))=="FEU - Institute of Technology Registration Directory":
        datasent='<p><strong>FEU - Institute of Technology Registration Directory</strong></p><table border = "1" style="width:100%"> \
       <tr> <td><strong>2 Easy Enrollment Steps For Freshmen</strong><br></td>  </tr>\
       <tr> <td><strong>1.	Register and Pay</strong><br>\
        •	Register at <a href="https://bit.ly/MILESOnlineRegistrationForm" target="_blank">https://bit.ly/MILESOnlineRegistrationForm</a><br>\
                   •	Pay reservation fee via online payment transfers, here are our accredited banks (BPI, BDO, Robinsons Bank, Land Bank of the Philippines, Metrobank, and Gcash)<br>\
                   •	Email the Deposit slip at reservations@feutech.edu.ph <br>\
                   <strong>2.	Get Ready</strong><br>\
                   •	Accomplish Admissions forms at <a href="https://tinyurl.com/FEUTECHFORMS" target="_blank">https://tinyurl.com/FEUTECHFORMS</a><br>\
                   •	Submit complete requirements online at glsosa@feutech.edu.ph<br>\
                   •	Receive portal portal password via email.<br>\
       </td><strong>3 Easy Enrollment Steps for Upperclassmen</strong></tr>\
       tr> <td><strong>1.	Register</strong><br>\
       •	Access student portal.<br>\
       •	Select courses and schedule via OSES<br>\
       <strong>2.	Pay</strong><br>\
       •	For tuition fee payment, you may deposit to the following bank accounts or via Gcash bank transfer(available in Apps Store)<br>\
       •	Kindly email scanned copy or picture of the deposit slip, bills payment, BPI or Gcash confirmation with the following details to onlinesupport_ao@feutech.edu.ph.<br>\
       •	Student Name<br>\
       •	Student Number<br>\
       •	Remarks/Notes<br>\
       <strong>3.	Get Ready</strong><br>\
       •	Select learning mode via student portal.<br>\
       •	View COR via Student portal.<br>\
       </td><strong>4 Easy Enrollment Steps for Transferees</strong></tr>\
       tr> <td><strong>1.	Register</strong><br>\
        •	Register at <a href="https://bit.ly/MILESOnlineRegistrationForm" target="_blank">https://bit.ly/MILESOnlineRegistrationForm</a><br>\
       <strong>2.	Crediting</strong><br>\
       •	For crediting of subjects, submit admissions form with soft copies of the following to glsosa@feutech.edu.ph:<br>\
       •	Copy of grades/TOR<br>\
       •	Course Description<br>\
       •	Credited subjects will be advised via email.<br>\
       <strong>3.	Pay</strong><br>\
       •	Pay reservation fee via online payment transfers, here are our accredited banks (BPI, BDO, Robinsons Bank, Land Bank of the Philippines, Metrobank, and Gcash)<br>\
       •	Email the Deposit slip at reservations@feutech.edu.ph<br>\
       <strong>4.	Get Ready</strong><br>\
       •	Accomplish Admissions form at <a href="https://tinyurl.com/FEUTECHFORMS" target="_blank">https://tinyurl.com/FEUTECHFORMS</a><br>\
       •	Receive portal password via email<br>\
       </table>'
        
    elif str(chatbot_response(str(userText)))=="FEU - Institute of Technology Payments' Directory":
        datasent='<p><strong>FEU - Institute of Technology Payments’ Directory</strong></p><table border = "1" style="width:100%"> \
       <tr> <td><strong>SERVICES</strong></td> <td><strong>LINK/EMAIL/CONTACT</strong></td> </tr>\
       <tr> <td>For admissions</td> <td>info@feutech.edu.ph</td> </tr>\
       <tr> <td>For tuition fee and balance</td> <td>onlinesupport_ao@feutech.edu.ph</td> </tr>\
       <tr> <td>For upperclassmen enrollment and scholarship </td> <td>onlinesupport_ro@feutech.edu.ph</td> </tr>\
       <tr> <td>Please visit the link below for payment methods.</td> <td><a href="https://www.feutech.edu.ph/admission/feu-tech-bank-details/" target="_blank">https://www.feutech.edu.ph/admission/feu-tech-bank-details/</a></td> </tr>\
       <tr> <td>Bank of the Philippine Islands - Morayta Branch - Online / Over the Counter : CASH Deposit Only - For OLD and NEW Students</td> <td>Account Name : East Asia Computer Center Inc<br>Account No.: 1581-00-2218</td> </tr>\
       <tr> <td>Bank of the Philippine Islands - Morayta Branch -Online / Over the Counter : CASH ONLY -For OLD Students Only</td> <td>Account Name : FEU – East Asia College<br>Account No.: 1581-00-1246</td> </tr>\
       <tr> <td>Robinsons Bank - Main Office Branch -Online / Over the Counter : CASH Deposit Only -For OLD and NEW Students</td> <td>Account Name : East Asia Computer Center Inc<br>Account No.: 1000-30-1000-17409</td> </tr>\
       <tr> <td>Land Bank of the Philippines - España Branch -Over the Counter : CASH Deposit Only -For OLD and NEW Students </td> <td>Account Name : East Asia Computer Center Inc<br>Account No.: 3721-0063-19</td> </tr>\
       <tr> <td>Banco De Oro - Recto Branch -Online / Over the Counter : CASH Deposit Only -For OLD and NEW Students</td> <td>Account Name : East Asia Computer Center Inc<br>Account No.: 0000-2000-7515</td> </tr>\
       <tr> <td>Metrobank - Morayta Branch -Online / Over the Counter : CASH Deposit Only -For OLD and NEW Students</td> <td>Account Name : East Asia Computer Center Inc<br>Account No.: 184-7-18450897-0</td> </tr>\
       <tr> <td colspan="2" text-align: center;>GCASH Bank</td></tr>\
       <tr> <td>BPI</td> <td>Account Name: FEU Institute of Technology<br>Account Number: 1581002218</td> </tr>\
       <tr> <td>BDO</td> <td>Account Name: FEU Institute of Technology<br>Account Number: 000020007515</td> </tr>\
       <tr> <td>Metrobank</td> <td>Account Name: FEU Institute of Technology<br>Account Number: 1847184508970</td> </tr>\
       <tr> <td>Lankbank</td> <td>Account Name: FEU Institute of Technology<br>Account Number: 3721006319</td> </tr>\
       <tr> <td>Robinsons Bank</td> <td>Account Name: FEU Institute of Technology<br>Account Number: 100030100017409</td> </tr>\
       <tr> <td colspan="2"><p>Gcash Procedure<br><br>Log in<br>Bank Transfer<br>Choose Bank<br>Fill out (Amount, Account Name, Account Number and Email Address)<br>Send Money<br>Review and Confirm</p></td> </tr>\
       </table>'
    elif str(chatbot_response(str(userText)))=="Milesâ€™s component":
       datasent='<p><strong>MILES Components</strong></p><table border = "1" style="width:100%"> \
       <tr> <td><strong>[MAIN]</strong></td> <td>A PowerPoint presentation for the whole module including its subtopics (uploaded in Canvas in pdf format).</td>  </tr>\
       <tr> <td><strong>[POWERPOINT]</strong> <td>A PowerPoint presentation for the respective subtopic (uploaded in Canvas in pdf format)..</td> </tr>\
       <tr> <td><strong>[VIDEO]</strong> <td>A recorded discussion for the respective subtopic</td> </tr>\
       <tr> <td><strong>[FORMATIVE] </strong> <td>An unrecorded quiz-type assessment of the acquired knowledge for each subtopic/module</td> </tr>\
       <tr> <td><strong>[SUPPLEMENTARY]</strong> <td>An additional material to strengthen your knowledge for each subtopic/module</td> </tr>\
       <tr> <td><strong>[CONSULTATION]</strong> <td>An online-based meeting with your teacher.</td> </tr>\
       <tr> <td><strong>[GUIDE]</strong> <td>A study guide/reviewer that you should read before taking the summative assessment.</td> </tr>\
       <tr> <td><strong>[PREPARATION]</strong> <td>An activity (e.g., tutorial) to be conducted prior to taking the summative assessment</td> </tr>\
       <tr> <td><strong>[SUMMATIVE]</strong> <td>A recorded assessment via a quiz-type, project-based, or, hands-on method at the end of each module</td> </tr>\
       <tr> <td><strong>[TECHNICAL]</strong> <td>A recorded assessment via a hands-on or output-based activity</td> </tr>\
       <tr> <td><strong>[REVIEW] </strong> <td>A link to a topic from your previous course  that you may use as a reviewer.</td> </tr>\
       <tr> <td><strong>[ADVANCED]</strong> <td>A link to a topic from a future course  that you may use to advance your knowledge</td> </tr>\
       <tr> <td><strong>[FINAL]</strong> <td>A recorded assessment via a quiz-type, project-based, or, hands-on method at the end of the course.</td> </tr>\
       </table>'
    elif str(chatbot_response(str(userText)))=="EECE Course":
        a = pd.read_csv("eececourse.csv")
        html_file = a.to_html()
        datasent=html_file
    elif str(chatbot_response(str(userText)))=="Juan Dela Cruz Schedule":
        a = pd.read_csv("jdcschedule.csv")
        html_file = a.to_html()
        datasent="<p><strong>Doc. Engr. Juan Dela Cruz</strong><br></p>"+html_file+"<p><br>https://meet.google.com/vdr-repu-zjh?pli=1&authuser=1></p>"+"<p>JuanDelaCruz@gmail.com</p>"


    elif str(chatbot_response(str(userText)))=="Pedro Matapang Schedule":
        a = pd.read_csv("pmschedule.csv")
        html_file = a.to_html()
        datasent="<p><strong>Engr. Pedro Matapang</strong><br></p>"+html_file+"<p><br>https://meet.google.com/vdr-repu-zjh?pli=1&authuser=2></p>"+"<p>Engr.PedroMagtapang01@gmail.com</p>"
    elif str(chatbot_response(str(userText)))=="Maria Gonda Schedule":
        a = pd.read_csv("mgschedule.csv")
        html_file = a.to_html()
        datasent="<p><strong>Engr. Maria Gonda</strong><br></p>"+html_file+"<p><br>https://meet.google.com/vdr-repu-zjh?pli=1&authuser=3></p>"+"<p>MariaG@gmail.com</p>"
    elif str(chatbot_response(str(userText)))=="Professor Schedule":
        a = pd.read_csv("jdcschedule.csv")
        html_filea = a.to_html()
        

        a = pd.read_csv("pmschedule.csv")
        html_fileb = a.to_html()
        

        a = pd.read_csv("mgschedule.csv")
        html_filec = a.to_html()
        datasent="<p><strong>Doc. Engr. Juan Dela Cruz</strong><br></p>"+html_filea+"<p><br><strong>Engr. Pedro Matapang</strong></p>"+"<br>"+html_fileb+"<p><br><strong>Engr. Maria Gonda</strong></p>"+"<br>"+html_filec

        
    elif str(chatbot_response(str(userText)))=="Registar Schedule":
        datasent='<table border = "1" style="width:100%"> \
       <tr> <td><strong>Registrar Office</strong></td> <td><strong>Monday - Saturday 08:00 - 15:00</strong></td>  </tr>\
       </table>'
    elif str(chatbot_response(str(userText)))=="Cashier Schedule":
        datasent='<table border = "1" style="width:100%"> \
       <tr> <td><strong>Cashier</strong></td> <td><strong>Monday - Saturday 08:00 - 15:00</strong></td>  </tr>\
       </table>'
    else:
        datasent=str(chatbot_response(str(userText)))
    
    #<tr> <td></td> <td></td> </tr>\
    #<a href="https://www.feutech.edu.ph/admission/feu-tech-bank-details/" target="_blank">https://www.feutech.edu.ph/admission/feu-tech-bank-details/</a>
    return datasent

if __name__ == "__main__":
    app.run()
