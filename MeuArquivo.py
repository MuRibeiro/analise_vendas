import pandas as pd
import win32com.client as win32

tabela_vendas = pd.read_excel('Vendas.xlsx')

pd.set_option('display.max_columns', None)

faturamento = tabela_vendas[['ID Loja', 'Valor Final']].groupby('ID Loja').sum()
print(faturamento)

vendas_lojas = tabela_vendas[['ID Loja', 'Quantidade']].groupby('ID Loja').sum()
print(vendas_lojas)

ticket_medio = (faturamento['Valor Final'] / vendas_lojas['Quantidade']).to_frame()
ticket_medio = ticket_medio.rename(columns={0: 'Ticket Médio'})
print(ticket_medio)

outlook = win32.Dispatch('outlook.application')
mail = outlook.CreateItem(0)
mail.To = 'britojuliana1998@gmail.com'
mail.Subject = 'Relatório de vendas por loja'
mail.HTMLBody = f'''
<p>Prezados,</p>

<p>Segue o relatório de vendas por cada loja.<p>

<p>Faturamento:</p>
{faturamento.to_html(formatters={'Valor Final': 'R${:,.2f}'.format})}

<p>Quantidade vendida:</p>
{vendas_lojas.to_html()}

<p>Ticket médio em cada loja:</p>
{ticket_medio.to_html(formatters={'Ticket Médio': 'R${:,.2f}'.format})}

<p>Qualquer dúvida estou à disposição</p>

<p>Att</p>
<p>Murilo Ribeiro</p>
'''

mail.Send()
