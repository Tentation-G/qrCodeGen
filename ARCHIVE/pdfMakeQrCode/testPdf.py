import segno
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
import os

# 1️⃣ Générer le QR code
qr = segno.make("https://example.com")
qr_file = "qr.png"
qr.save(qr_file, scale=8)

# 2️⃣ Créer le PDF
c = canvas.Canvas("qr_avec_texte.pdf", pagesize=A4)
page_width, page_height = A4

# Taille et position
qr_size = 50 * mm
x = (page_width - qr_size) / 2
y = (page_height - qr_size) / 2

# Dessiner le QR code
c.drawImage(qr_file, x, y, qr_size, qr_size)

# 3️⃣ Ajouter le texte en dessous
c.setFont("Helvetica", 12)
c.drawCentredString(
    page_width / 2,
    y - 10 * mm,
    "texte : test"
)

# Finaliser
c.save()
os.remove(qr_file)