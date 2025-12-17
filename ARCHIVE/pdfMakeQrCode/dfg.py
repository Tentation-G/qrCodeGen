import os
import pandas as pd
import segno

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth

# ====== WRAP TEXTE (retour à la ligne selon largeur max) ======
def wrap_text(text, font_name, font_size, max_width):
    words = str(text).split()
    lines = []
    current = ""

    for w in words:
        test = (current + " " + w).strip()
        if stringWidth(test, font_name, font_size) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = w

    if current:
        lines.append(current)
    return lines

# ====== 1) LECTURE EXCEL (Ref + Des) ======
file_path = "../../app/ExcelParsingSample.xlsx"
ref_col = "Ref"
des_col = "Designation"

dfs = pd.read_excel(file_path, sheet_name=None)

pairs = []
for sheet_name, df in dfs.items():
    if ref_col in df.columns and des_col in df.columns:
        sub = df[[ref_col, des_col]].dropna()
        for ref, des in sub.itertuples(index=False, name=None):
            pairs.append((str(ref).strip(), str(des).strip()))

# Dédup simple par Ref
unique = {}
for ref, des in pairs:
    if ref not in unique:
        unique[ref] = des
clean_pairs = list(unique.items())

# ====== 2) PRENDRE LES 12 PREMIERS ======
items = clean_pairs[:13]
if not items:
    raise ValueError("Aucun couple (Ref, Des) trouvé. Vérifie les colonnes Ref/Des et ton fichier Excel.")

# ====== 3) PDF : grille 3x4 ======
pdf_name = "qr_12_couples_3x4.pdf"
c = canvas.Canvas(pdf_name, pagesize=A4)
page_w, page_h = A4

cols, rows = 3, 4

# Marges de page
margin_x = 12 * mm
margin_y = 12 * mm

# Dimensions d'une cellule
cell_w = (page_w - 2 * margin_x) / cols
cell_h = (page_h - 2 * margin_y) / rows

# QR : pour scan 20–30cm, vise ~30–35mm
qr_size = 45 * mm

# Mise en forme texte
font_name = "Helvetica"
font_size = 9
line_height = 4.2 * mm  # hauteur d'une ligne de texte
c.setFont(font_name, font_size)

# Padding interne à la cellule
pad = 4 * mm

# Hauteur réservée au texte
text_area_h = 14 * mm  # ajuste si tu veux +/-
max_lines = int(text_area_h // line_height)

for i, (ref, des) in enumerate(items):
    col = i % cols
    row = i // cols  # 0..3

    # Origine cellule (coin haut-gauche)
    cell_x = margin_x + col * cell_w
    cell_top = page_h - margin_y - row * cell_h

    # Position QR : en haut, centré
    qr_x = cell_x + (cell_w - qr_size) / 2
    qr_y = cell_top - pad - qr_size

    # Générer QR (rouge)
    img_path = f"_tmp_qr_{i}.png"
    segno.make(ref).save(
        img_path,
        scale=8,
        dark="red",      # mets "black" si tu veux + fiable
        light="white",
        border=2
    )
    c.drawImage(img_path, qr_x, qr_y, qr_size, qr_size)
    os.remove(img_path)

    # Zone texte : sous le QR, dans la largeur de la cellule
    label = des  # ou f"{ref} - {des}"
    max_text_w = cell_w - 2 * pad

    lines = wrap_text(label, font_name, font_size, max_text_w)

    # Limiter pour éviter d'empiéter sur la cellule suivante
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        # Ajoute "..." si on coupe
        if lines:
            last = lines[-1]
            while stringWidth(last + "...", font_name, font_size) > max_text_w and len(last) > 0:
                last = last[:-1]
            lines[-1] = (last + "...").strip()

    # Dessiner les lignes centrées
    text_start_y = qr_y - 3 * mm  # petit espace sous QR
    for li, line in enumerate(lines):
        y = text_start_y - li * line_height
        c.drawCentredString(cell_x + cell_w / 2, y, line)

c.save()
print(f"PDF généré : {pdf_name}")
