#imports
from flask import Flask, render_template, request
import nltk
import os

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
model = load_model('/home/Xypherly/mysite/chatbot_model.h5')
import json
import random
intents = json.loads(open('/home/Xypherly/mysite/intents.json').read())
words = pickle.load(open('/home/Xypherly/mysite/words.pkl','rb'))
classes = pickle.load(open('/home/Xypherly/mysite/classes.pkl','rb'))

app = Flask(__name__, template_folder='/home/Xypherly/mysite/template')

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
    
    return str(chatbot_response(str(userText)))

if __name__ == "__main__":
    app.run()
