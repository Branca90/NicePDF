import camelot
import pytesseract
from PIL import Image, ImageEnhance, ImageFilter
from pdf2image import convert_from_path
import pandas as pd
import json
import os
import glob

# Aumenta il limite di Pillow per evitare DecompressionBombError
Image.MAX_IMAGE_PIXELS = 1000000000

def pdf_to_images(pdf_path, output_dir="temp_images", image_format="PNG"):
    """
    Converte un PDF in immagini e le salva nella directory specificata.
    
    Args:
        pdf_path (str): Percorso del file PDF da convertire.
        output_dir (str): Directory dove salvare le immagini (default: temp_images).
        image_format (str): Formato delle immagini (default: PNG).
    """
    # Crea la directory temp_images se non esiste
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Converto {pdf_path} in immagini {image_format}...")
    
    # Converti il PDF in immagini
    images = convert_from_path(pdf_path, dpi=150)  # DPI ridotto per evitare problemi
    
    # Salva ogni immagine
    for i, image in enumerate(images):
        image_path = os.path.join(output_dir, f"page-{i+1:03d}.{image_format.lower()}")
        image.save(image_path, image_format)
        print(f"Salvata immagine: {image_path}")

def preprocess_image(image):
    print("Pre-elaborazione dell'immagine con Pillow...")
    gray = image.convert("L")
    enhancer = ImageEnhance.Contrast(gray)
    gray = enhancer.enhance(2.0)
    gray = gray.point(lambda x: 0 if x < 128 else 255, "1")
    return gray

def extract_raw_text(image):
    print("Estrazione con Tesseract...")
    processed_image = preprocess_image(image)
    return pytesseract.image_to_string(processed_image, lang="eng", config="--psm 3 --dpi 300")

def extract_table_with_ocr(image):
    print("Estrazione con OCR per tabelle...")
    processed_image = preprocess_image(image)
    ocr_result = pytesseract.image_to_data(processed_image, output_type=pytesseract.Output.DICT, lang="eng", config="--psm 6 --dpi 300")
    words = ocr_result['text']
    left = ocr_result['left']
    top = ocr_result['top']
    width = ocr_result['width']
    height = ocr_result['height']
    
    print(f"Parole estratte con Tesseract: {words}")
    
    cells = []
    current_cell = []
    last_left = left[0] if left else 0
    last_top = top[0] if top else 0
    
    for i in range(len(words)):
        if words[i].strip():
            if abs(top[i] - last_top) > 20:
                if current_cell:
                    cells.append(" ".join(current_cell))
                current_cell = [words[i]]
                last_top = top[i]
                last_left = left[i]
            elif abs(left[i] - last_left) > 80:
                if current_cell:
                    cells.append(" ".join(current_cell))
                current_cell = [words[i]]
                last_left = left[i]
            else:
                current_cell.append(words[i])
    
    if current_cell:
        cells.append(" ".join(current_cell))
    
    print(f"Celle estratte: {cells}")
    
    rows = []
    current_row = []
    table_headers = ["Date", "Symbol", "Type", "Quantity", "Price", "Side", "Value", "Fees", "Commission"]
    is_table = False
    table_rows = []
    
    for cell in cells:
        if any(header in cell for header in table_headers):
            is_table = True
            if current_row:
                rows.append(current_row)
            current_row = [cell]
        elif is_table:
            current_row.append(cell)
            if len(current_row) >= 9:
                table_rows.append(current_row)
                current_row = []
        else:
            current_row.append(cell)
            if len(current_row) >= 10:
                rows.append(current_row)
                current_row = []
    
    if current_row:
        if is_table:
            table_rows.append(current_row)
        else:
            rows.append(current_row)
    
    print(f"Righe non tabellari: {rows}")
    print(f"Righe tabellari: {table_rows}")
    
    all_tables = []
    if rows:
        df = pd.DataFrame(rows)
        all_tables.append(df)
        print(f"Tabella non strutturata creata: {df}")
    if table_rows:
        df = pd.DataFrame(table_rows)
        all_tables.append(df)
        print(f"Tabella strutturata creata: {df}")
    
    return all_tables

def clean_json(tables):
    print("Pulizia del JSON...")
    print(f"Tabelle prima della pulizia: {tables}")
    cleaned_tables = []
    for table in tables:
        if isinstance(table, list) and all(isinstance(row, dict) for row in table):
            cleaned_table = []
            for row in table:
                cleaned_row = {}
                idx = 0
                for key, value in row.items():
                    if value is not None:
                        if isinstance(value, str) and "\n" in value:
                            split_values = value.split("\n")
                            for split_value in split_values:
                                if split_value.strip():
                                    cleaned_row[str(idx)] = split_value.strip()
                                    idx += 1
                        else:
                            cleaned_row[str(idx)] = value
                            idx += 1
                cleaned_table.append(cleaned_row)
            cleaned_tables.append(cleaned_table)
        else:
            table_dict = table.to_dict(orient="records")
            cleaned_table = []
            for row in table_dict:
                cleaned_row = {}
                idx = 0
                for i in range(len(row)):
                    value = row[str(i)]
                    if value is not None:
                        if isinstance(value, str) and "\n" in value:
                            split_values = value.split("\n")
                            for split_value in split_values:
                                if split_value.strip():
                                    cleaned_row[str(idx)] = split_value.strip()
                                    idx += 1
                        else:
                            cleaned_row[str(idx)] = value
                            idx += 1
                cleaned_table.append(cleaned_row)
            cleaned_tables.append(cleaned_table)
    print(f"Tabelle pulite: {cleaned_tables}")
    return cleaned_tables

def process_images_to_json(image_dir="temp_images"):
    all_tables = []
    
    # Cerca tutte le immagini nella directory temp_images
    image_files = sorted(glob.glob(os.path.join(image_dir, "page-*.png")))
    if not image_files:
        print(f"Errore: Nessuna immagine trovata in {image_dir}. Esegui prima l'opzione 1 per convertire il PDF in immagini.")
        return
    
    # Processa ogni immagine
    for image_path in image_files:
        print(f"\nElaborazione immagine: {image_path}")
        image = Image.open(image_path)
        
        # Prova a estrarre tabelle con OCR
        tables = extract_table_with_ocr(image)
        for df in tables:
            if df is not None:
                df = df.dropna(axis=1, how='all')
                table_dict = df.to_dict(orient="records")
                all_tables.append(table_dict)
        
        # Se non ci sono tabelle, estrai testo grezzo
        if not tables:
            print("Nessuna tabella trovata con OCR, estraggo testo grezzo...")
            raw_text = extract_raw_text(image)
            if raw_text.strip():
                lines = raw_text.split('\n')
                rows = [[line.strip()] for line in lines if line.strip()]
                if rows:
                    df = pd.DataFrame(rows)
                    table_dict = df.to_dict(orient="records")
                    all_tables.append(table_dict)
                    print(f"Testo grezzo convertito in tabella: {df}")
    
    # Pulisci e salva il JSON
    all_tables = clean_json(all_tables)
    
    os.makedirs("output", exist_ok=True)
    output_path = "output/output.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(all_tables, f, indent=4, ensure_ascii=False)
    
    if os.path.exists(output_path):
        print(f"Conversione completata! File JSON creato in {output_path}")
    else:
        print("Errore: il file JSON non è stato creato.")

def main_menu():
    pdf_path = "data/sample.pdf"
    
    while True:
        print("\n=== NicePDF Menu ===")
        print("1. Converti PDF in immagini PNG (salva in temp_images)")
        print("2. Crea output.json (estrai tabelle dalle immagini in temp_images)")
        print("3. Esci")
        choice = input("Seleziona un'opzione (1-3): ")
        
        if choice == "1":
            # Verifica che il file PDF esista
            if not os.path.exists(pdf_path):
                print(f"Errore: {pdf_path} non esiste. Assicurati che il file PDF sia presente nella directory 'data/'.")
            else:
                pdf_to_images(pdf_path, image_format="PNG")
        elif choice == "2":
            process_images_to_json()
        elif choice == "3":
            print("Uscita dal programma.")
            break
        else:
            print("Opzione non valida. Riprova.")

if __name__ == "__main__":
    main_menu()
