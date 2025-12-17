import pandas as pd
import segno as sg
import os
from fpdf import FPDF
from utils import *

# Excel Extract and Parse
a =""
file_path = "data_samples/Liste_comptage_233.xlsx"
#file_path = "data_samples/ExcelParsingSample.xlsx"

def xlsx_to_res_des(file_path:str, qr_code_col:str="Reference", lib_col:str="Designation", aimed_sheet:str="Base Article complète")->dict:
    # Init le dict
    ref_des_couple_dict = {}

    dfs = pd.read_excel(file_path, sheet_name=None)

    # Pour chaque feiille du classeur
    for sheet_name, df in dfs.items():
        """
        Base Article complète
        Comptage
        """
        if sheet_name == aimed_sheet:
            # Convertion str + cleanup
            #df.columns = df.columns.str.strip()
            df.columns = df.columns.map(lambda c: str(c).strip())

            if qr_code_col in df.columns and lib_col in df.columns:
                # Pour chaque lignes des colonnes <qr_code_col> et <lib_col>
                for reference, designation in zip(df[qr_code_col], df[lib_col]):
                    # Si ref pas null
                    if pd.notna(reference):
                        ref_des_couple_dict[str(reference)] = str(designation)
    # Return du dict
    return ref_des_couple_dict

# Todo : Plus tard : Pouvoir passer en param la disposition et la taille des qr code (ex : 20mm, 4x4)
def qrCode_lib_grid_pdf_gen(couple_dict:dict, file_name:list="qrCode_List", dispo:int=0)->None:
    """
        :param: couple_dict: dict -> couple_dict[qrCode] = libéllé_associe
        :param: file_name: str
        :param: dispo: int

        :return pdf
    """

    match dispo:
        case 0: # 12/page
            cols = 3
            rows = 4
            qrCode_size = 40
            font_size = 9
            text_spacing = 2
            text_img_spacing = 2
        case 1: # 48/page
            cols = 6
            rows = 8
            qrCode_size = 20
            font_size = 4
            text_spacing = 2
            text_img_spacing = 2
        case 2: # 240/page
            cols = 12
            rows = 20 #(16 base + 4 pour stacker)
            qrCode_size = 10
            font_size = 2
            text_spacing = 1
            text_img_spacing = -1.5

    # ------------ Init var ------------
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(False)
    pdf.add_font("Arial", "", r"C:\Windows\Fonts\arial.ttf")

    temps_qrCode_dir = "_temp"
    outPut_pdf_dir = "_pdfOut"

    #cols = 6
    #rows = 8
    total_item_per_page = cols * rows

    w_margin = 0
    h_margin = 0

    page_w = pdf.w - w_margin
    page_h = pdf.h - h_margin
    cell_w = page_w / cols
    cell_h = page_h / rows

    #qrCode_size = 20

    font_family = "Arial"
    #font_size = 4
    text_align = "C"
    # ----------------------------------
    clean_temp_qr("_temp")

    for i, (ref, des) in enumerate(couple_dict.items()):
        # Si nb par page atteind -> nouvelle page
        if i > 0 and i % total_item_per_page == 0:
            pdf.add_page()
            pdf.set_auto_page_break(False)

        # id de l'item sur sa page [0-total_item_per_page]
        item_id_page = i % total_item_per_page

        col = item_id_page % cols
        row = item_id_page // cols

        coord_x = w_margin + col * cell_w
        coord_y = h_margin + row * cell_h - 2
        pdf.rect(coord_x, coord_y, cell_w, cell_h)

        # Gen QrCode
        qr_code_img_name = os.path.join(temps_qrCode_dir, f"_temp_qr_p{i}.png")
        sg.make(ref).save(qr_code_img_name, scale=6)

        # Si sur la premiere rangé de la page
        if item_id_page < cols:
            pdf.image(qr_code_img_name, coord_x + (cell_w - qrCode_size) / 2, coord_y + 2, qrCode_size)
        else :
            pdf.image(qr_code_img_name, coord_x + (cell_w - qrCode_size) / 2, coord_y + 0.5, qrCode_size)

        # del du png du qr code temp
        #print(f"qrCode {i}/{len(couple_dict)}.")
        print_loading_bar(i, len(couple_dict))
        os.remove(qr_code_img_name)

        # Texte
        if item_id_page < cols:
            pdf.set_xy(coord_x + 3, coord_y + text_img_spacing + qrCode_size + 3)
        else :
            pdf.set_xy(coord_x + 3, coord_y + text_img_spacing-1.5 + qrCode_size + 3)
        pdf.set_font(font_family, size=font_size)
        pdf.multi_cell(cell_w - 6, text_spacing, des, align=text_align)

    # Output File + Name
    pdf.output(os.path.join(outPut_pdf_dir,f"{file_name}TN7.pdf"))
    print(f"\n Process finished")

couple_dict = xlsx_to_res_des(file_path=file_path, aimed_sheet="Comptage")
qrCode_lib_grid_pdf_gen(couple_dict, dispo=2)






