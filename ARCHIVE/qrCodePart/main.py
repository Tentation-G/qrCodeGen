import segno as sg

qrCode = sg.make("https://www.google.com/")

qrCode.save("qrCodeGoogleLink.png")