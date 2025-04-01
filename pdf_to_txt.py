import fitz  # PyMuPDF

pdf_path = "Jim Knopf und Lukas der Lokomotivführer -- Ende, Michael -- 2012 -- Thienemann_ in der Thienemann-Esslinger Verlag GmbH.pdf"
txt_path = "im Knopf und Lukas der Lokomotivführer.txt"

doc = fitz.open(pdf_path)
with open(txt_path, "w", encoding="utf-8") as f_out:
    for page in doc:
        text = page.get_text()
        f_out.write(text + "\n")