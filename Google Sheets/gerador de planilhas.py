import pandas as pd
import random
import re

qtd_por_mes = int(input('Indique a quantidade de linhas por mês >>> '))
meses = input('Indique o número do mês das transações (ou sequência de meses separando o mês inicial e final por vírgula, ex. 6,9 ) >>> ')
if ',' in meses:
    posicao_virgula = meses.rfind(',')
    meses = [int(meses[:posicao_virgula]), int(meses[posicao_virgula+1:])]
else:
    meses=list(meses)

# móveis / eletros
tipos = {'Cama': [800,3000],
         'Cadeira': [80,300],
         'Guarda roupa': [500,1500],
         'Microondas': [200,600],
         'Geladeira': [500, 3000]}

df = pd.DataFrame(columns=['data','tipo','categoria','valor'])

if len(meses) > 1:
    meses = list(range(meses[0],meses[1]+1)) # o último número do range não é incluso na sequência. Por isso fiz +1

id_linha=0
id_mes=0
total_linhas=range(1,qtd_por_mes * len(tipos.keys())+1)

for i in list(total_linhas):
    data_ = f'2022-{meses[id_mes]}-01'
    tipo_ = random.choice(list(tipos.keys()))

    valor_ = random.randint(tipos[tipo_][0], tipos[tipo_][1])
    
    
    if valor_ <= tipos[tipo_][0] + (tipos[tipo_][1] - tipos[tipo_][0])/3:
        categoria_ = 'baixa'
    elif valor_ <= tipos[tipo_][0] + (tipos[tipo_][1] - tipos[tipo_][0])*2/3:
        categoria_ = 'intermediária'
    else: 
        categoria_ = 'alta'

    df.loc[id_linha,:] = [pd.to_datetime(data_,format='%Y-%m-%d').strftime('%Y-%m-%d'),tipo_,categoria_,valor_]

    id_linha+=1

    if id_linha % qtd_por_mes == 0:
        id_mes+=1
        if id_mes == len(meses):
            break

df.to_clipboard(index=None)