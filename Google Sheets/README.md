# Python e Google Sheets
Suponha que você receba uma planilha com preços da concorrência de setembro com as colunas data | tipo | categoria | preço concorrência | e te peçam para juntar numa outra planilha com dados históricos, com as colunas | tipo | categoria | preço concorrência | preço interno |, tudo no Google Sheets.
Repare que na coluna de setembro falta a coluna de preço interno, que pode ser incluída por uma planilha dimensão com os preços mensais da sua empresa para todos os produtos da concorrência.

![image](https://github.com/user-attachments/assets/43f3594c-03f2-4f57-b0a1-3575b3aa3763)


<h3>Como as bibliotecas do Python interagem com o Google Sheets </h3>
<hr>
Uma API é uma forma de permitir que diferentes sistemas se comuniquem entre si. <br>
A biblioteca OAuth 2.0 garante segurança ao acessar conteúdos protegidos, como o Google Sheets, dando acesso à determinada conta sem usar o login e senha. <br>
Uma vez liberado o acesso por meio do OAuth 2.0, o gspread funciona como meio para acessar o Google Sheets. <br>
Essa comunicação se dá por meio de requisições, que são solicitações com padrões definidos. Por exemplo, as requisições GET/POST/PUT são usadas para ler, enviar e atualizar dados, respectivamente. O gspread traduz os comandos do Python para a linguagem própria da requisição.

<h3>Caso prático</h3>
<hr>
<p>Para gerar as planilhas de setembro e a compilada, usei o programa 'gerador de planilhas.py'.</p>
<p>Para gerar a planilha dimensão, usei o programa 'planilha dimensao.py'.</p>
<br>
<p>O programa da automação é o 'gspread_prática.py', que segue o passo a passo:</p>

<ol>
    <li>Acesso às 3 planilhas do Google Sheets por meio de uma credencial do meu e-mail, que permite acesso aos arquivos. Isso é feito por uma biblioteca do Google.</li>
    <li>Extração das informações de cada uma das 3 tabelas.</li>
    <li>Aplicação das fórmulas: primeiramente, um concatenado na planilha dimensão e na de setembro, e depois o PROCX na tabela de setembro puxando o preço interno da tabela dimensão, por meio dos concatenados.</li>
    <li>Colagem dos valores do PROCX e exclusão das colunas concatenadas.</li>
    <li>Junção da tabela de setembro com a tabela com dados históricos.</li>
<br>
Vale ressaltar que a aplicação das fórmulas foi feita pela função batch_update do gspread, que envia uma única requisição ao API do Google Sheets com a aplicação da fórmula em todas as linhas de uma única vez, melhorando a performance do programa, uma vez que há um limite de requisições por minuto. <br>

  <li>Colagem dos valores do PROCX e exclusão as colunas concatenadas</li>
  <li>Junção da tabela de setembro com a tabela com dados históricos</li>
</ol>

<h3>Resultado</h3>
<hr>
Dados de setembro incluídos na planilha de dados compilados. <br>
https://github.com/brunoserp/Python-w-gsheets/blob/main/tabela%20final.jpg
