import os
from pathlib import Path

import pandas as pd
import segno as sg

from fpdf import FPDF
from io import BytesIO

from .utils import *

import time
start = time.perf_counter()

BASE_DIR = Path(__file__).resolve().parent

file_path = "data_samples/Liste_comptage_233.xlsx"
#file_path = "data_samples/ExcelParsingSample.xlsx"
def xlsx_to_res_des(
        file_path:str,
        qr_code_col:str="Reference",
        lib_col:str="Designation",
        aimed_sheet:str="Comptage",
    )->dict[str,str]:

    #start_xlsx_to_res_des = time.perf_counter()
    # Init le dict
    ref_des_couple_dict = {}

    dfs = pd.read_excel(file_path, sheet_name=None)

    # Pour chaque feiille du classeur
    for sheet_name, df in dfs.items():
        """
        Test pour les deux feuilles ci dessous
        Base Article complète
        Comptage
        """
        if sheet_name == aimed_sheet:
            # Convertion str + cleanup
            df.columns = df.columns.map(lambda c: str(c).strip())

            if qr_code_col in df.columns and lib_col in df.columns:
                # Pour chaque lignes des colonnes <qr_code_col> et <lib_col>
                for reference, designation in zip(df[qr_code_col], df[lib_col]):
                    # Si ref pas null
                    if pd.notna(reference):
                        ref_des_couple_dict[str(reference)] = str(designation)
    # Return du dict
    #end_xlsx_to_res_des = time.perf_counter()
    #print(f"Temps xlsx_to_res_des : {end_xlsx_to_res_des - start_xlsx_to_res_des:.3f} secondes")
    return ref_des_couple_dict

def qrCode_lib_grid_pdf_gen(couple_dict:dict, file_name:list="qrCode_List", dispo:int=0, need_output:bool=True,)->None:

    match dispo:
        case 0: # 12/page
            cols, rows = 3, 4
            qrCode_size, font_size = 40, 9
            text_spacing, text_img_spacing = 2, 2
        case 1: # 99/page
            cols, rows = 9, 11
            qrCode_size, font_size = 20, 3.5
            text_spacing, text_img_spacing = 1.75, -2
        case 2: # 260/page
            cols, rows = 13, 20
            qrCode_size, font_size = 10, 2
            text_spacing, text_img_spacing = 1, -1.5


    # ------------ Init var ------------
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(False)
    pdf.add_font("Arial", "", r"C:\Windows\Fonts\arial.ttf")

    outPut_pdf_dir = "_pdfOut"
    os.makedirs(outPut_pdf_dir, exist_ok=True)


    total_item_per_page = cols * rows

    w_margin = 0
    h_margin = 0

    page_w = pdf.w - w_margin
    page_h = pdf.h - h_margin
    cell_w = page_w / cols
    cell_h = page_h / rows

    font_family = "Arial"
    text_align = "C"
    # ----------------------------------

    for i, (ref, des) in enumerate(couple_dict.items()):
        if i > 0 and i % total_item_per_page == 0:
            pdf.add_page()
            pdf.set_auto_page_break(False)

        item_id_page = i % total_item_per_page
        col = item_id_page % cols
        row = item_id_page // cols

        coord_x = w_margin + col * cell_w
        coord_y = h_margin + row * cell_h

        pdf.rect(coord_x, coord_y, cell_w, cell_h)

        # QR code en mémoire (PNG)
        buf = BytesIO()
        sg.make(ref).save(buf, kind="png", scale=6, border=2)
        buf.seek(0)

        pdf.image(
            buf,
            coord_x + (cell_w - qrCode_size) / 2,
            coord_y + 0.5,
            qrCode_size
        )

        print_loading_bar(i, len(couple_dict), barLib="Creation du pdf")

        pdf.set_xy(coord_x + 3, coord_y + text_img_spacing - 1.5 + qrCode_size + 3)
        pdf.set_font(font_family, size=font_size)
        pdf.multi_cell(cell_w - 6, text_spacing, des, align=text_align)

    complete_file_name = f"{file_name}SpeedTest-2.4.T1pdf"

    if need_output:
        pdf.output(os.path.join(outPut_pdf_dir, complete_file_name))

    print(f"\n Process <{complete_file_name}> finished")

if __name__ == "__main__":
    couple_dict = xlsx_to_res_des(file_path=file_path)
    qrCode_lib_grid_pdf_gen(couple_dict, dispo=1, need_output=False,)

    #qrCodeGen(couple_dict)
    #clean_temp_qr("_temp")

    end = time.perf_counter()
    print(f"Temps Total : {end - start:.3f} secondes")













