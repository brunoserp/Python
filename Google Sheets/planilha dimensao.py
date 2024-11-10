import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import random

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file(r'C:\Users\bserpellone\Desktop\Python\github\google sheets\credentials.json',scopes=scopes)
client = gspread.authorize(creds)

# abrir planilhas
sheet_id_compilado = '1tEFl5TbhNO61Cez5txJjCRHnivhaNGy9iiShCdR-FKc' 
compilado = client.open_by_key(sheet_id_compilado)  

sheet_id_atual = '18TAjn1hNOCPKnN_PEQLiFw4wskJkshsxqopESsmRhLQ'
atual = client.open_by_key(sheet_id_atual)

# abrir as abas. Supondo que seja sempre a primeira
aba_compilada = compilado.sheet1
aba_atual = atual.sheet1

df_compilada = pd.DataFrame(aba_compilada.get_all_records())
df_atual = pd.DataFrame(aba_atual.get_all_records())

df_comp = pd.concat([df_compilada,df_atual])
df_comp = df_comp.groupby(['data','tipo','categoria'])['valor'].mean().reset_index()
df_comp['preço'] = df_comp.apply(lambda row: random.choice([row['valor'] - row['valor']*0.1, row['valor'] + row['valor']*0.1]),axis=1)
df_comp.to_clipboard(index=None,sep='|')

