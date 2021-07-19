# Semantic-Label-Extraction

Per usare l'interfaccia web:
- Collegarsi da una prima shell al server dove si trova il DB tramite ssh tunneling tramite il comando: ssh -L 8123:speedup.dia.uniroma3.it:8123 -N bigdata2021@speedup.dia.uniroma3.it inserendo la password personale
- Posizionarsi da una seconda shell nella cartella RestApi
- Avviare la WebApi tramite il comando: python main.py
- Collegarsi a [http://127.0.0.1:5000](http://127.0.0.1:5000)

Se non si disponesse delle dipendenze necessarie procedere in questo modo:
- Installare virtualenv per creare una sandbox nella propria cartella di progetto con tutte le dipendenze necessarie. ( pip install virtualenv)
- Spostarsi nella tabella e creare un ambiente virtuale isolato. (venv myenv)
- Attivare l'ambiente virtuale (source myenv/bin/activate)
- Installare ora tutte le librerie necessarie indicate nel file requirements.txt: esse verranno installate solo nel nuovo ambiente virtuale precedentemente attivato (pip install -r requirements.txt)
- Per disattivare l'ambiente virtuale -> deactive
