import time

# -------------------------------- BAR 1 --------------------------------

def wave_window(t: int, width: int = 8) -> str:
    WAVE = "▁▂▃▄▅▆▇█▇▆▅▄▃▂▁"
    s = (WAVE * ((width // len(WAVE)) + 3))
    start = t % len(WAVE)
    return s[start:start + width]

def print_loading_bar(qrAct:int, nbTotal:int, barLength:int=100) -> None:

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
    print(f"\r[{bar}] {wave} {percent:3d}% ({qrAct}/{nbTotal})", end="", flush=True)

# -----------------------------------------------------------------------

# -------------------------------- BAR 2 --------------------------------

def print_loading_bar2(qrAct:int, nbTotal:int, barLength:int=100) -> None:
    BANK = "+×"
    if qrAct % 2 == 0 :
        fill_char = BANK[0]
    else :
        fill_char = BANK[1]

    qrAct = min(qrAct, nbTotal) + 1
    progress = (qrAct / nbTotal)

    filled = int(barLength * progress)
    empty = barLength - filled
    bar = ("-" * (filled-1)) + fill_char + (" " * empty)

    percent = round(progress * 100)

    wave = wave_window(qrAct, width=8)
    print(f"\r[{bar}] {wave} {percent:3d}% ({qrAct}/{nbTotal})", end="", flush=True)
# -----------------------------------------------------------------------

max = 73
for i in range(max):
    time.sleep(0.25)
    #time.sleep(0.01)
    print_loading_bar(i, max)
