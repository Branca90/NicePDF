# NICEPDF

NICEPDF è un progetto Python per estrarre tabelle e testo da file PDF, convertendoli in un file JSON strutturato. Utilizza Tesseract OCR per il riconoscimento del testo e supporta la pre-elaborazione delle immagini per migliorare l'accuratezza dell'OCR. Il progetto include un menu interattivo per gestire il flusso di lavoro.

## Funzionalità principali

- **Conversione PDF in immagini**: Converte le pagine di un PDF in immagini PNG utilizzando la libreria `pdf2image`. Le immagini vengono salvate nella directory `temp_images/`.
- **Estrazione di tabelle e testo tramite OCR**: Utilizza Tesseract OCR per estrarre testo e tabelle dalle immagini generate.
- **Pre-elaborazione delle immagini**: Applica filtri (conversione in scala di grigi, aumento del contrasto, sogliatura binaria) tramite Pillow per migliorare la qualità dell'OCR.
- **Output strutturato in JSON**: Salva i dati estratti (tabelle e testo grezzo) in un file `output.json`.

## Requisiti

- **Sistema operativo**: Linux (testato su Ubuntu 18.04)
- **Python**: 3.6 o superiore
- **Tesseract OCR**: Versione 4.1 o superiore
- **Dipendenze di sistema**:
  - `poppler-utils` (necessario per `pdf2image`)
  - `tesseract-ocr` e `libtesseract-dev` (per l'OCR)

## Dipendenze Python

Il progetto utilizza le seguenti librerie Python:

- **`pdf2image`**:
  - **Versione suggerita**: 1.16.3 o superiore
  - **Scopo**: Converte le pagine di un PDF in immagini PNG.
  - **Installazione**: `pip install pdf2image`

- **`pytesseract`**:
  - **Versione suggerita**: 0.3.10 o superiore
  - **Scopo**: Interfaccia Python per Tesseract OCR.
  - **Installazione**: `pip install pytesseract`

- **`Pillow`**:
  - **Versione suggerita**: 9.5.0 o superiore
  - **Scopo**: Manipolazione delle immagini per la pre-elaborazione.
  - **Installazione**: `pip install Pillow`

- **`pandas`**:
  - **Versione suggerita**: 2.0.0 o superiore
  - **Scopo**: Strutturazione dei dati in tabelle.
  - **Installazione**: `pip install pandas`

- **`paddleocr`** (opzionale):
  - **Versione suggerita**: 2.7.0 o superiore
  - **Scopo**: OCR avanzato basato su deep learning.
  - **Installazione**: `pip install paddlepaddle paddleocr`

## Installazione

1. **Clona il repository**:
   ```bash
   git clone git@github.com:Branca90/NicePDF.git
   cd NicePDF
# Crea e attiva un ambiente virtuale

```bash
python3 -m venv venv
source venv/bin/activate
```

# Installa le dipendenze Python

```bash
pip install pdf2image pytesseract pillow pandas
```

# Installa le dipendenze di sistema

```bash
sudo apt update
sudo apt install tesseract-ocr libtesseract-dev poppler-utils
```

# Utilizzo

Il progetto utilizza un unico script principale: `nicepdf.py`. Offre un menu interattivo per gestire il flusso di lavoro:

```bash
python3 src/nicepdf.py
```

## Opzioni

1. Converte il PDF in immagini PNG e le salva in `temp_images/`.
2. Estrae tabelle e testo dalle immagini in `temp_images/` e crea `output.json`.
3. Esce dal programma.

# Esempio

Assicurati che un file PDF sia presente in `data/sample.pdf`.

Esegui il programma e seleziona l'opzione 1 per convertire il PDF in immagini.

Seleziona l'opzione 2 per estrarre i dati e generare `output.json`.

# Comandi utili

Ecco alcuni comandi utili per lavorare con il progetto:

## Attiva l'ambiente virtuale

```bash
source venv/bin/activate
```

## Disattiva l'ambiente virtuale

```bash
deactivate
```

## Installa tutte le dipendenze in un colpo solo (senza PaddleOCR)

```bash
pip install pdf2image pytesseract pillow pandas
```

## Installa PaddleOCR (solo per desktop con AVX)

```bash
pip install paddlepaddle paddleocr
```

## Verifica le librerie installate

```bash
pip list
```

## Esegui lo script principale

```bash
python3 src/nicepdf.py
```

## Rimuovi tutte le immagini temporanee (se necessario)

```bash
rm -rf temp_images/*
```

## Controlla lo stato del repository Git

```bash
git status
```

## Push delle modifiche su GitHub

```bash
git add .
git commit -m "Descrizione delle modifiche"
git push origin main
```

# Funzionalità di Tesseract utilizzate

NICEPDF si basa su Tesseract OCR per il riconoscimento del testo. Di seguito sono elencate le funzionalità di Tesseract che utilizziamo e il loro scopo:

## Riconoscimento del testo (`image_to_string`)

Utilizzata nella funzione `extract_raw_text` per estrarre testo grezzo da un'immagine.

Serve per convertire immagini di testo (es. pagine scansionate) in testo leggibile, utile quando non ci sono tabelle strutturate.

Configurazione: `--psm 3 --dpi 300` (modalità di segmentazione automatica con risoluzione stimata).

## Estrazione dei dati con coordinate (`image_to_data`)

Utilizzata nella funzione `extract_table_with_ocr` per estrarre testo insieme alle sue coordinate (left, top, width, height).

Serve per ricostruire tabelle identificando la posizione del testo nell'immagine, permettendo di separare righe e colonne.

Configurazione: `--psm 6 --dpi 300` (assume un blocco di testo uniforme, ottimale per tabelle).

## Supporto multilingue

Tesseract supporta oltre 100 lingue, ma nel nostro script usiamo `lang="eng"` per il riconoscimento in inglese.

Può essere configurato per altre lingue (es. `lang="ita"` per l'italiano) se necessario.

## Pre-elaborazione delle immagini

Anche se Tesseract ha funzionalità interne di pre-elaborazione, noi utilizziamo Pillow per migliorare la qualità delle immagini prima di passarle a Tesseract (es. conversione in scala di grigi, aumento del contrasto, sogliatura binaria).

Questo migliora l'accuratezza dell'OCR, specialmente per PDF scansionati di bassa qualità.
