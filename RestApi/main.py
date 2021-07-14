import requests
import tensorflow
import time
import datetime
from requests.exceptions import ConnectionError
from flask import Flask, render_template, request
from transformers import pipeline
app = Flask(__name__)

RECORDS_NUMBER = 100


def classification(r, labels):
    
    

    # L'utf-8-sig è una variante Python di UTF-8 che ci permette di eliminare, se presenti, eventuali carattere UTF-8 BOM.
    values = r.content.decode('utf-8-sig')

    labels_candidate = labels
    values = values.replace("\ufeff", "")
    values = values.replace("\\", " ")
    values = values.split('\n')
    values.pop()
    dictionary = {}
    occorrenze = {}

    # Crea una lista vuota per ciascuna label
    for label in labels:
        dictionary[label] = []
        occorrenze[label] = 0
    classifier = pipeline("zero-shot-classification")
    labels_number = len(labels)

    # Vengono effettuate le previsioni attraverso il modello.
    # Le previsioni vengono memorizzate nel dizionario.
    for i in range(RECORDS_NUMBER):
        text = values[i]
        result = classifier(text, labels)
        occorrenze[result['labels'][0]] += 1
        for y in range(labels_number):
            label = result['labels'][y]
            score = result['scores'][y]
            dictionary[label].append(score)
    risultati = {}
    for label in labels:
        risultati[label] = sum(dictionary[label]) / RECORDS_NUMBER

    max_score = 0

    for label, score in risultati.items():
        if score > max_score:
            label_predict = label
            max_score = score

    return label_predict, max_score, occorrenze[label_predict]




@app.route('/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return render_template('form.html')

@app.route('/data/', methods = ['POST', 'GET'])
def datas():
    if request.method == 'GET':
        return f""
    if request.method == 'POST':
        form = request.form
        db = form["db"]
        table = form["table"]
        column = form["column"]
        labels = form["labels"]
        ip = form["ip"]
        port = form["port"]
        labels = [elem.strip() for elem in labels.split(',')]
        start = time.time()
        try:
            if ip == "" :
                url = 'http://localhost:' + port + '/?query=SELECT top '  + str(RECORDS_NUMBER) + ' ' + column + ' ' + 'FROM'+ ' ' + db +'.' + table
            else:
               url = 'http://' + ip +':'+ port + '/?query=SELECT top '  + str(RECORDS_NUMBER) + ' ' + column + ' ' + 'FROM'+ ' ' + db +'.' + table
            r = requests.get(url)
            label_predict, max_score, occorrenze = classification(r,labels)
        except ConnectionError:
            return render_template('im.html')
        except IndexError:
            return render_template('indNot.html')
        
        final = time.time() - start
        final = int(float("{:.2f}".format(final)))
        list = [ label_predict,max_score,occorrenze, datetime.timedelta(seconds=final)]
        return render_template('data.html', form_data=list)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)

