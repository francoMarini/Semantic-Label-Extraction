# Semantic Label Extraction

Al momento, una delle fonti di dati più importanti viene rappresentata dalle pagine web :chart_with_upwards_trend::earth_asia:  \
Le migliaia di informazioni contenute al loro interno possono essere estratte e memorizzate all’interno di un database NoSQL: in questo modo, in futuro, potranno essere utilizzate per effettuare interessanti analisi. 

Tipicamente però, questi dati risultano essere sporchi ed individuare automaticamente a quale attributo dell’entità fanno riferimento non è per niente facile :dizzy_face:

:bulb: Per contrastare questo problema, abbiamo pensato di realizzare un tool che permetta di identificare il **contenuto semantico** dei campi relativi ad una specifica tabella. 



## Come utilizzare l'interfaccia web
Per usare l'interfaccia web:
- Collegarsi da una prima shell al server dove si trova il DB tramite ssh tunneling utilizzando il comando: 
```
ssh -L 8123:speedup.dia.uniroma3.it:8123 -N bigdata2021@speedup.dia.uniroma3.it
```
- Posizionarsi da una seconda shell nella cartella RestApi
- Aprire il file config.env e impostare l'indirizzo ip del server e la porta
- Avviare la WebApi tramite il comando: python main.py
- Collegarsi a [http://127.0.0.1:5000](http://127.0.0.1:5000) 

\
Se non si disponesse delle dipendenze necessarie procedere in questo modo:
- Installare virtualenv per creare una sandbox nella propria cartella di progetto con tutte le dipendenze necessarie ( pip install virtualenv)
- Spostarsi nella tabella e creare un ambiente virtuale isolato (venv myenv)
- Attivare l'ambiente virtuale (source myenv/bin/activate)
- Installare ora tutte le librerie necessarie indicate nel file *requirements.txt*: esse verranno installate solo nel nuovo ambiente virtuale precedentemente attivato (pip install -r requirements.txt)
- Per disattivare l'ambiente virtuale utilizzare il comando *deactive*

## Anteprima 
<img src="https://github.com/francoMarini/Semantic-Label-Extraction/blob/main/RestApi/static/anteprima.JPG" alt="Anteprima Interfaccia" width="800" />
