



def wave_window(t: int, width: int = 8) -> str:
    WAVE = "▁▂▃▄▅▆▇█▇▆▅▄▃▂▁"
    s = (WAVE * ((width // len(WAVE)) + 3))
    start = t % len(WAVE)
    return s[start:start + width]

def print_loading_bar(qrAct:int, nbTotal:int, barLength:int=100, barLib:str="") -> None:
    qrAct = min(qrAct, nbTotal) + 1
    progress = (qrAct / nbTotal)

    filled = int(barLength * progress)
    empty = barLength - filled
    bar = ("█" * filled) + ("░" * empty)

    percent = round(progress * 100)

    if qrAct >= nbTotal:
        percent = 100
        bar = "█" * barLength

    wave = wave_window(qrAct, width=8)
    #bar = wave_window(qrAct, width=qrAct) + "-" * empty
    print(f"\r[{bar}] {wave} {percent:3d}% ({qrAct}/{nbTotal}) [{barLib}]", end="", flush=True)

def format_loading_bar(qrAct: int, nbTotal: int, barLength: int = 100, space_between:int=0) -> str:
    #qrAct -> avancement
    qrAct = min(qrAct, nbTotal - 1)

    progress = (qrAct + 1) / nbTotal if nbTotal else 0

    filled = int(barLength * progress)
    empty = barLength - filled
    bar = ("█" * filled) + ("░" * empty)

    percent = round(progress * 100)

    wave = wave_window(qrAct, width=8) if qrAct > 0 else "▁"*8

    #return f"[{bar}] {wave} {percent:3d}% ({qrAct+1:3d}/{nbTotal:3d})"
    return f" {{{bar}}} {wave} {percent:03d}% ({(qrAct+1):03d}/{nbTotal:03d})"

def print_couple_dict(ref_des_couple_dict):
    # Max len for format spacing
    max_len = max(len(k) for k in ref_des_couple_dict)
    space_fill = ""

    # Affichage des couples du dict
    print("\n----------------------------- Liste des Couples -----------------------------")
    for ref, des in ref_des_couple_dict.items():
        if len(ref) < max_len:
            space_fill = " " * (max_len - len(ref) + 1)
        else :
            space_fill = " "

        print(f"{ref}{space_fill}: {des}")
    print("-----------------------------------------------------------------------------")
    print(f"Nb couples :{len(ref_des_couple_dict)}")
    print("-----------------------------------------------------------------------------")

# Test
#couple_dict = xlsx_to_res_des(file_path)
#print_couple_dict(couple_dict)