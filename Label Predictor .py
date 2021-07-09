#!/usr/bin/env python
# coding: utf-8

# # Semantic Label Extraction

# Nel seguente codice cercheremo di analizzare i dati estratti dalle pagine web. \
# Più precisamente, a partire da dati organizzati in formato "tabellare" all'interno di un database (*ClickHouse*), il nostro obiettivo sarà quello di identificare un'**etichetta** per ciascun campo, al fine di stabilirne il contenuto. 

# ## Caricamento dati 

# I dati vengono richiesti al Server ClickHouse tramite delle richieste GET. \
# Per farlo Python sfrutta la libreria *requests*.
# 
# L'utente in questa applicazione dovrà specificare:
# * La tabella e la rispettiva colonna da analizzare. 
# * Le labels candidate.

# In[1]:


#Tabella da analizzare
tabella = input("Inserire il nome della tabella che si vuole analizzare:  ")

#Colonna da analizzare
colonna= input("Di quale colonna vuoi trovare il contenuto semantico?   ")


# In[2]:


#Questo parametro indica il numero di valori che devo analizzare per stabilire l'etichetta corretta.
RECORDS_NUMBER= 100


# In[3]:


#Viene definita la richiesta GET da inviare al Server
url= 'http://localhost:8123/?query=SELECT top ' + str(RECORDS_NUMBER) + ' ' + tabella + ' ' + 'FROM extracted_data.' + tabella


# In[81]:


import requests
from requests.exceptions import ConnectionError
url='http://localhost:8123/?query=SELECT top 100 iill FROM extracted_data.c5e54033df0a4d17801808da46506300'

try:
    r = requests.get(url)
except ConnectionError:
        print("Il collegamento al database non è attivo.")

        
#L'utf-8-sig è una variante Python di UTF-8 che ci permette di eliminare, se presenti, eventuali carattere UTF-8 BOM.
values= r.content.decode('utf-8-sig')


#Controllo i parametri inseriti dall'utente
if (values[6:8]=='60'):
    print("ATTENZIONE! La tabella indicata non esiste.")
elif (values[6:8]=='47'):
    print("ATTENZIONE! La colonna indicata non esiste.")
else:
    print("I dati sono stati caricati correttamente.")


# In[72]:


#Labels 
labels_candidate = input("Inserire le labels candidate (separate da una virgola):  ")


# In[71]:


labels = labels_candidate.replace(", " or " ," ,  "-").split("-")


# In[82]:


#labels=['food', 'football', 'year']


# ## Preprocessing dei dati 

# In[83]:


#In alcuni casi (non sempre) possono essere presenti sequenze di caratteri che aggiungono rumore ai dati.
#Ci siamo occupati di identificarli ed eliminarli.

values = values.replace("\ufeff", "")
values = values.replace("\\", " ")


# In[84]:


#Rapido sguardo ai dati
values


# In[85]:


#Realizziamo una lista in cui ciascun elemento corrisponde ad un singolo valore del campo specificato.
values=values.split('\n')
values.pop()


# In[50]:


values


# # Previsione label

# In[73]:


#!pip install transformers datasets


# In[86]:


#Struttura: dictionary[label] -> [89%, 93%, 97%, 32%, 99% , ...]
dictionary={}


# In[87]:


#Sruttura ausiliaria: permette di stabilire il numero di volte in cui ciascuna etichetta è stata predetta
occorrenze={}


# In[88]:


#Crea una lista vuota per ciascuna label
for label in labels:
    dictionary[label]=[]
    occorrenze[label]=0


# In[89]:


from transformers import pipeline

classifier = pipeline("zero-shot-classification")
    


# In[90]:


labels_number= len(labels)

#Vengono effettuate le previsioni attraverso il modello.
#Le previsioni vengono memorizzate nel dizionario.
for i in range(RECORDS_NUMBER):
    text = values[i]
    result=classifier(text, labels)
    occorrenze[result['labels'][0]]+=1
    for y in range(labels_number):
        label= result['labels'][y]
        score= result['scores'][y]
        dictionary[label].append(score)
    


# In[103]:


risultati={}
for label in labels:
    risultati[label]= sum(dictionary[label])/RECORDS_NUMBER

max_score= 0

for label, score in risultati.items():  
    if score > max_score:
        label_predict=label
        max_score=score

print("Etichetta predetta: %s \n\n\n" % label_predict)
print("Grado di affidabilità: %.3f\n" % max_score)
print("%d/%d -> Questa etichetta è stata predetta %d volte, considerando %d diversi campioni." 
      % (occorrenze[label_predict], RECORDS_NUMBER, occorrenze[label_predict], RECORDS_NUMBER))


# In[104]:


#dictionary[label_predict]


# In[105]:


#occorrenze[label_predict]

