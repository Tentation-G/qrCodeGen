import pandas as pd
import segno as sg

# Excel Extract and Parse
file_path = "../../app/ExcelParsingSample.xlsx"
ref_col = "Ref"
des_col = "Des"
neededCol_list = []

dfs = pd.read_excel(file_path, sheet_name=None)

for sheet_name, df in dfs.items():
    if ref_col in df.columns:
        print(f"\n--- {sheet_name} ---")
        print(df[ref_col])
        neededCol_list.extend(df[ref_col].dropna().tolist())

print(f"Uncleaned list      :{neededCol_list}")
print(f"Uncleaned list len  :{len(neededCol_list)}")

cleaned_neededCol_list = list(set(neededCol_list))
print(f"Cleaned list        :{cleaned_neededCol_list}")
print(f"Cleaned list len    :{len(neededCol_list)}")

# QR Code Gen
"""
qrCode_list

for ref in cleaned_neededCol_list:
    qrCode = sg.make(ref)
    qrCode_list.append(qrCode)
qrCode.save("qrCodeGoogleLink.png")
"""







