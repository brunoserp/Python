import gspread
from google.oauth2.service_account import Credentials

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file(r'C:\Users\bserpellone\Desktop\Python\github\google sheets\credentials.json',scopes=scopes)
client = gspread.authorize(creds)

# abrir planilhas
sheet_id_compilado = '1tEFl5TbhNO61Cez5txJjCRHnivhaNGy9iiShCdR-FKc' 
compilado = client.open_by_key(sheet_id_compilado)  

sheet_id_atual = '18TAjn1hNOCPKnN_PEQLiFw4wskJkshsxqopESsmRhLQ'
atual = client.open_by_key(sheet_id_atual)

sheet_id_dimensao = '13dKW9ByGACjHAHp4PidWAB269AEAE5I8dPEf9I-m5Wk' 
dimensao = client.open_by_key(sheet_id_dimensao)


# abrir as abas. Supondo que seja sempre a primeira
aba_compilada = compilado.sheet1
aba_atual = atual.sheet1
aba_dimensao = dimensao.sheet1

# selecionar toda a tabela de cada aba
dados_compilados = aba_compilada.get_all_values() # get_all_values() transforma cada linha numa lista
dados_atuais = aba_atual.get_all_values() 
dados_dimensao = aba_dimensao.get_all_values()

# puxar a informação de preço praticado para a aba do mes atual
updates_dimensao=[]
updates_atual=[]
# fazer um concatenado nas 2 planilhas para ser o conteúdo em comum para a fórmula
for i in range(2, len(dados_dimensao) + 1):  # A partir da linha 2
    formula_concat = f'=A{i}&"_"&B{i}&"_"&C{i}'
    #dados_dimensao.update(range_name=f'F{i}', values=[[formula_concat]], value_input_option='USER_ENTERED')
    '''updates_dimensao.append({
        "range": f'F{i}', 
        "values": [[formula_concat]]
    })'''

#aba_dimensao.batch_update(updates_dimensao, value_input_option='USER_ENTERED')

nome_aba_dimensao = dimensao.sheet1.title
for i in range(2, len(dados_atuais) + 1):  # A partir da linha 2
    formula_concat = f'=A{i}&"_"&B{i}&"_"&C{i}'
    formula_procx = (f'=PROCX(F{i};'
                    f'IMPORTRANGE("https://docs.google.com/spreadsheets/d/13dKW9ByGACjHAHp4PidWAB269AEAE5I8dPEf9I-m5Wk"; "{nome_aba_dimensao}!F:F");'
                    f'IMPORTRANGE("https://docs.google.com/spreadsheets/d/13dKW9ByGACjHAHp4PidWAB269AEAE5I8dPEf9I-m5Wk"; "{nome_aba_dimensao}!D:D"))')
    aba_atual.update(f'E{i}', [[formula_procx]], value_input_option='USER_ENTERED')
    '''updates_atual.append({
        "range": f'E{i}',  # Mudando a coluna onde a fórmula PROCX será inserida
        "values": [[formula_procx]]
    })


# apagar coluna concat das 2 abas
aba_dimensao.batch_update([{
    "range": f"F2:F",
    "values": [[]]  }])

aba_atual.batch_update([{
    "range": f"F2:F",
    "values": [[]]  }])'''

# concatenar as 2 tabelas na tabela dados_compilados:
#dados_compilados.extend(dados_atuais) # concatena as abas
print(pd.DataFrame(dados_atuais))
#aba_compilada.update('A1', dados_compilados) # atualiza a aba com os dados concatenados

