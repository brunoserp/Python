import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

'''PASSO A PASSO:
# REQUISIÇÃO DE ACESSO À MINHA CONTA AO API DO GOOGLE SHEETS
# ACESSAR AS TABELAS
    # ABRIR PLANILHAS PELO ID DE CADA URL DAS PLANILHAS (entre o /d/ e /edit)
    # ABRIR AS ABAS (PRIMEIRA DE CADA PLANILHA)
    # SELECIONAR TODA A TABELA DE CADA UMA DAS 3 PLANILHAS

# APLICAÇÃO DAS FÓRMULAS PARA PUXAR O PREÇO INTERNO PARA SET/24
    # TABELA DIMENSÃO: CONCATENAR DATA, TIPO E CATEGORIA NA TABELA DIMENSÃO (COM TODOS OS PREÇOS POR DATA/TIPO/CATEGORIA)
    # TABELA FATO: CONCATENAR DATA, TIPO E CATEGORIA NA TABELA DIMENSÃO (COM TODOS OS PREÇOS POR DATA/TIPO/CATEGORIA) E DEPOIS FAZER PROCX
    # COLAR VALORES RESULTANTES DO PROCX
    # APAGAR O CONCAT NAS DUAS TABELAS
# CONCATENAR A TABELA DE SET/24 NA TABELA COMPILADA
'''

# =======================================================================================================================================
# REQUISIÇÃO DE ACESSO À MINHA CONTA AO API DO GOOGLE SHEETS
# =======================================================================================================================================
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file(r'C:\Users\bserpellone\Desktop\Python\github\google sheets\credentials.json',scopes=scopes)
client = gspread.authorize(creds)

# =======================================================================================================================================
# ABRIR PLANILHAS PELO ID DE CADA URL DAS PLANILHAS (entre o /d/ e /edit)
# =======================================================================================================================================
sheet_id_compilado = '1tEFl5TbhNO61Cez5txJjCRHnivhaNGy9iiShCdR-FKc' 
compilado = client.open_by_key(sheet_id_compilado)  

sheet_id_atual = '18TAjn1hNOCPKnN_PEQLiFw4wskJkshsxqopESsmRhLQ'
atual = client.open_by_key(sheet_id_atual)

sheet_id_dimensao = '13dKW9ByGACjHAHp4PidWAB269AEAE5I8dPEf9I-m5Wk' 
dimensao = client.open_by_key(sheet_id_dimensao)

# =======================================================================================================================================
# ABRIR AS ABAS (PRIMEIRA DE CADA PLANILHA)
# =======================================================================================================================================
aba_compilada = compilado.sheet1
aba_atual = atual.sheet1
aba_dimensao = dimensao.sheet1

# =======================================================================================================================================
# SELECIONAR TODA A TABELA DE CADA UMA DAS 3 PLANILHAS
# =======================================================================================================================================
dados_compilados = aba_compilada.get_all_values() # get_all_values() transforma cada linha numa lista
dados_atuais = aba_atual.get_all_values() 
dados_dimensao = aba_dimensao.get_all_values()
# =======================================================================================================================================

# =======================================================================================================================================
# =======================================================================================================================================
# APLICAÇÃO DAS FÓRMULAS PARA PUXAR O PREÇO INTERNO PARA SET/24
# =======================================================================================================================================
# =======================================================================================================================================

# =======================================================================================================================================
# TABELA DIMENSÃO: CONCATENAR DATA, TIPO E CATEGORIA NA TABELA DIMENSÃO (COM TODOS OS PREÇOS POR DATA/TIPO/CATEGORIA)
# =======================================================================================================================================
updates_dimensao=[]
for i in range(2, len(dados_dimensao) + 1):  # para cada linha, desde a primeira até a última de cada planilha
    formula_concat = f'=A{i}&"_"&B{i}&"_"&C{i}'
    updates_dimensao.append({"range": f'E{i}', # onde aplicar a fórmula, coluna E para todas as linhas
                             "values": [[formula_concat]]})
# atualizar células com a fórmula acima
aba_dimensao.batch_update(updates_dimensao, value_input_option='USER_ENTERED') 

# =======================================================================================================================================
# TABELA FATO: CONCATENAR DATA, TIPO E CATEGORIA NA TABELA DIMENSÃO (COM TODOS OS PREÇOS POR DATA/TIPO/CATEGORIA) E DEPOIS FAZER PROCX
# =======================================================================================================================================
updates_fato_concat=[]
updates_fato_procx=[]
link_dimensao= r'https://docs.google.com/spreadsheets/d/13dKW9ByGACjHAHp4PidWAB269AEAE5I8dPEf9I-m5Wk'
nome_aba_dimensao = dimensao.sheet1.title

for i in range(2, len(dados_atuais) + 1):  
    # CONCAT
    formula_concat = f'=A{i}&"_"&B{i}&"_"&C{i}'
    updates_fato_concat.append({"range": f'F{i}', "values": [[formula_concat]]})
    
    # PROCX
    formula_procx = (f'=PROCX(F{i};'                                                 # FÓRMULA SEMELHANTE À:
                    f'IMPORTRANGE("{link_dimensao}";"{nome_aba_dimensao}!E:E");'     #   =PROCX(F1;'tbl dimensão preço interno'!E:E;'tbl dimensão preço interno'!D:D)
                    f'IMPORTRANGE("{link_dimensao}"; "{nome_aba_dimensao}!D:D"))')   #  O IMPORTRANGE no Google Sheets serve para vincular com outra planilha (arquivo)   
    updates_fato_procx.append({"range": f'E{i}', "values": [[formula_procx]]})

aba_atual.batch_update(updates_fato_concat, value_input_option='USER_ENTERED')     
aba_atual.batch_update(updates_fato_procx, value_input_option='USER_ENTERED') 

# =======================================================================================================================================
# COLAR VALORES RESULTANTES DO PROCX
# =======================================================================================================================================
valores_procx = aba_atual.get('E2:E')
aba_atual.batch_update([{
    "range": "E2:E",
    "values": valores_procx}], value_input_option='RAW')

aba_atual.update(range_name='E1',values=[['preço interno']],value_input_option='RAW')

# =======================================================================================================================================
# APAGAR O CONCAT NAS DUAS TABELAS
# =======================================================================================================================================
# apagar coluna concat das 2 abas
# aba_dimensao.batch_clear(["E1:E"])  
# aba_atual.batch_clear(["F1:F"])  

# =======================================================================================================================================
# CONCATENAR A TABELA DE SET/24 NA TABELA COMPILADA
# =======================================================================================================================================
# concatenar as 2 tabelas na tabela dados_compilados:
dados_compilados.extend(dados_atuais[1:]) 
aba_compilada.update(range_name='A1', values=dados_compilados)

