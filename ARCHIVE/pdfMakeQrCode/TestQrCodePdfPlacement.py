from fpdf import FPDF
import segno
import os

pdf = FPDF()
pdf.add_page()

cols, rows = 3, 4
items_per_page = cols * rows

page_w = pdf.w - 20
page_h = pdf.h - 20
cell_w = page_w / cols
cell_h = page_h / rows

qr_size = 40  # mm

items = [
    ("REF001", "Designation assez longue pour tester le retour à la ligne automatique"),
] * 13 + [("REF002", "Autre designation")]

for i, (ref, des) in enumerate(items):

    # --- NOUVELLE PAGE APRES 12 ---
    if i > 0 and i % items_per_page == 0:
        pdf.add_page()

    # index LOCAL à la page (0..11)
    local_i = i % items_per_page

    col = local_i % cols
    row = local_i // cols

    x = 10 + col * cell_w
    y = 10 + row * cell_h

    # QR
    img = f"_qr_{i}.png"
    segno.make(ref).save(img, scale=6)
    pdf.image(img, x + (cell_w - qr_size) / 2, y + 5, qr_size)
    os.remove(img)

    # Texte WRAPPÉ automatiquement
    pdf.set_xy(x + 3, y + 5 + qr_size + 3)
    pdf.set_font("Helvetica", size=9)
    pdf.multi_cell(cell_w - 6, 4, des, align="C")

nb = 3.2
pdf.output(f"qr_12_{nb}.pdf")
