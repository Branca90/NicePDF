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

   ## Installazione

### Crea e attiva un ambiente virtuale:
```bash
python3 -m venv venv
source venv/bin/activate
Installa le dipendenze Python:
```bash
pip install pdf2image pytesseract pillow pandas
Installa le dipendenze di sistema:
```bash
sudo apt update
sudo apt install tesseract-ocr libtesseract-dev poppler-utils
