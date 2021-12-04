from flask import render_template, request, flash, Markup
from app import app
from MyForms import Form
from DateFilter import *
from StringEquivalent import *
import pandas as pd
import numpy as np
from numpy import inf
import datetime as dt
from datetime import datetime
from dateutil.parser import parse
import plotly.express as px
import random
import math

start_request = []
end_request = []
city_request = []
form_start = []
form_end = []
form_city = []

url1 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/covid-estado-sp.csv'
url2 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/covid-municipios-sp.csv'
url3 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/srag-covid.csv'
url4 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/vacinometro-sp.csv'
url5 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/evolucao-aplicacao-doses.csv'
url6 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/leitos-uti-enfermaria.csv'
url7 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/isolamento-social.csv'
url8 = 'https://raw.githubusercontent.com/SoSoJigsaw/Carcara/main/Aplica%C3%A7%C3%A3o%20Web/' \
       'app/data/vacinacao-estatisticas.csv'

palette = ['rgba(220, 119, 13, 0.8)', 'rgba(248, 172, 91, 0.9)', 'rgba(220, 119, 13, 0.7)', 'rgba(248, 172, 91, 0.7)',
           'rgba(220, 119, 13, 0.9)', 'rgba(220, 119, 13, 0.9)', 'rgba(172, 90, 0, 0.8)', 'rgba(249, 212, 156, 0.8)',
           'rgba(172, 90, 0, 1)', 'rgba(249, 212, 156, 0.9)', 'rgba(220, 119, 13, 0.7)', 'rgba(248, 172, 91, 1)',
           'rgba(249, 212, 156, 1)', 'rgba(220, 119, 13, 1)', 'rgba(249, 212, 156, 0.7)', 'rgba(248, 172, 91, 0.8)']

pops = pd.read_csv(url2, usecols=['Município', 'pop'], dtype={'Município': 'category', 'pop': 'int32'})
duplicates = pops.duplicated(keep='first')
pops = pops[~duplicates]

####################################################################################################################


# ROUTE PÁGINA INICIAL (INDEX)
@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')


####################################################################################################################


# ROUTES INICIAIS DA PÁGINA DOS MUNICÍPIOS
@app.route("/estado", methods=['GET'])
@app.route("/estado/covidsp", methods=['GET'])
def covidsp_main():
    random.shuffle(palette)
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    covidsp = pd.read_csv(url1, dtype={'Total de casos': 'int32', 'Total de óbitos': 'int32',
                                       'Casos por dia': 'int32', 'Óbitos por dia': 'int16'})
    covidsp['Data'] = pd.to_datetime(covidsp['Data'])
    flash_generate(covidsp)

    casost = covidsp['Total de casos'].max()
    casost = ("{:,}".format(casost)).replace(',', '.')
    obitost = covidsp['Total de óbitos'].max()
    obitost = ("{:,}".format(obitost)).replace(',', '.')
    casosult = covidsp['Casos por dia'].iloc[-1]
    casosult = ("{:,}".format(casosult)).replace(',', '.')
    obitosult = covidsp['Óbitos por dia'].iloc[-1]
    obitosult = ("{:,}".format(obitosult)).replace(',', '.')

    # Gráfico casos por dia
    fig1 = px.bar(covidsp, x='Data', y='Casos por dia', color_discrete_sequence=palette,
                  title='<b>Casos por dia no Estado de São Paulo</b>',
                  hover_data=['Data', 'Total de casos', 'Casos por dia'], template='xgridoff')
    fig1.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=2000),
    fig1.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(covidsp['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
    fig1.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                       xaxis_title='', yaxis_title="Casos por dia",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"), barmode='stack',
                       xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
    graf1 = fig1.to_html(full_html=False)

    # Gráfico óbitos por dia
    fig2 = px.bar(covidsp, x='Data', y='Óbitos por dia', color_discrete_sequence=palette,
                  title='<b>Óbitos por dia no Estado de São Paulo</b>',
                  hover_data=['Data', 'Total de óbitos', 'Óbitos por dia'],
                  template='xgridoff')
    fig2.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=100),
    fig2.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(covidsp['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
    fig2.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=100, r=50),
                       xaxis_title='', yaxis_title="Óbitos por dia",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"), barmode='stack',
                       xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
    graf2 = fig2.to_html(full_html=False)

    # Gráfico total de casos
    fig3 = px.line(covidsp.sort_values(by=['Data'], ascending=[True]), x='Data', y='Total de casos',
                   line_shape='linear', template='xgridoff',
                   color_discrete_sequence=palette, title='<b>Crescimento do nº de casos no Estado</b>',
                   hover_data=['Data', 'Total de casos', 'Casos por dia'], line_dash_sequence=['solid'],
                   render_mode='auto')
    fig3.update_traces(line=dict(width=6)),
    fig3.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=500000),
    fig3.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(covidsp['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
    fig3.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=100, r=50),
                       xaxis_title='', yaxis_title="Total de casos",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                       xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
    graf3 = fig3.to_html(full_html=False)
    pop = 46649132  # população do estado de SP
    casos = covidsp['Total de casos'].max()
    inc = casos / (pop - casos) * 100000
    info3 = int("{:.0f}".format(inc))
    info3 = ("{:,}".format(info3)).replace(',', '.')
    if info3 == inf:
        info3 = 0
    if info3 == 'nan':
        info3 = 0

    # Gráfico total de óbitos
    fig4 = px.line(covidsp.sort_values(by=['Data'], ascending=[True]), x='Data', y='Total de óbitos',
                   line_shape='linear', template='xgridoff', color_discrete_sequence=palette,
                   line_dash_sequence=['solid'],
                   render_mode='auto', hover_data=['Data', 'Total de óbitos', 'Óbitos por dia'],
                   title='<b>Crescimento do nº de óbitos no Estado</b>')
    fig4.update_traces(line=dict(width=6)),
    fig4.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=15000),
    fig4.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(covidsp['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
    fig4.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=100, r=50),
                       xaxis_title='', yaxis_title="Total de óbitos",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                       xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
    graf4 = fig4.to_html(full_html=False)
    obtotal = covidsp['Total de óbitos'].max()
    casostotal = covidsp['Total de casos'].max()
    let = (obtotal / casostotal) * 100
    info4 = "{:.2f}".format(let).replace('.', ',')
    if info4 == inf:
        info4 = 0
    if info4 == 'nan':
        info4 = 0

    return render_template('estados.html', form=form, min=mini, max=maxi,
                           graf1_covidsp=graf1, graf2_covidsp=graf2, graf3_covidsp=graf3, graf4_covidsp=graf4,
                           painel1_covidsp=casost, painel2_covidsp=obitost, painel3_covidsp=casosult,
                           painel4_covidsp=obitosult, info3_covidsp=info3, info4_covidsp=info4)


@app.route("/estado/vacina", methods=['GET'])
def evoludose_main():
    random.shuffle(palette)
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    evoludose = pd.read_csv(url5,
                            dtype={'1ª Dose': 'int32', '2ª Dose': 'int32', '3ª Dose': 'int32', 'Dose Única': 'int32'})
    evoludose['Data'] = pd.to_datetime(evoludose['Data'])
    flash_generate(evoludose)

    vact = evoludose['1ª Dose'].sum() + evoludose['2ª Dose'].sum() + evoludose['3ª Dose'].sum() + evoludose['Dose Única'].sum()
    vact = "{:,}".format(vact).replace(',', '.')
    pop = 46649132
    vac2 = evoludose['2ª Dose'].sum() + evoludose['Dose Única'].sum()
    popvac2 = (vac2 * 100) / pop
    popvac2 = "{:.2f}".format(popvac2).replace('.', ',') + '%'
    vac3 = evoludose['3ª Dose'].sum()
    popvac3 = (vac3 * 100) / pop
    popvac3 = "{:.2f}".format(popvac3).replace('.', ',') + '%'
    vacultd = evoludose['1ª Dose'].iloc[-1] + evoludose['2ª Dose'].iloc[-1] + evoludose['3ª Dose'].iloc[-1] + evoludose['Dose Única'].iloc[-1]
    vacultd = "{:,}".format(vacultd).replace(',', '.')

    # Evolução 1ª dose
    fig1 = px.bar(evoludose, x='Data', y='1ª Dose', template='xgridoff',
                  color_discrete_sequence=palette, title='<b>Evolução da aplicação da 1ª dose</b>')
    fig1.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=50000),
    fig1.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(evoludose['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
    fig1.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=100, r=50),
                       xaxis_title='', yaxis_title="Doses aplicadas",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                       xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
    graf1 = fig1.to_html(full_html=False)

    # Evolução 2ª dose
    fig2 = px.bar(evoludose, x='Data', y='2ª Dose', template='xgridoff',
                  color_discrete_sequence=palette, title='<b>Evolução da aplicação da 2ª dose</b>')
    fig2.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=50000),
    fig2.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(evoludose['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
    fig2.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=100, r=50),
                       xaxis_title='', yaxis_title="Doses aplicadas",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                       xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
    graf2 = fig2.to_html(full_html=False)

    # Evolução 3ª dose
    fig3 = px.bar(evoludose, x='Data', y='3ª Dose', template='xgridoff',
                  color_discrete_sequence=palette, title='<b>Evolução da aplicação da 3ª dose</b>')
    fig3.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=20000),
    fig3.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(evoludose['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
    fig3.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=100, r=50),
                       xaxis_title='', yaxis_title="Doses aplicadas",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                       xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
    graf3 = fig3.to_html(full_html=False)

    # Evolução dose única
    fig4 = px.bar(evoludose, x='Data', y='Dose Única', template='xgridoff',
                  color_discrete_sequence=palette, title='<b>Evolução da aplicação da dose única</b>')
    fig4.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=20000),
    fig4.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(evoludose['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
    fig4.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=100, r=50),
                       xaxis_title='Data', yaxis_title="Doses aplicadas",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                       xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
    graf4 = fig4.to_html(full_html=False)

    # Filtros apenas para dados totais
    final = (evoludose['Data'].max() + dt.timedelta(days=1)).strftime('%Y-%m-%d')
    inicial = (evoludose['Data'].max() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
    filterdate = (evoludose['Data'] > inicial) & (evoludose['Data'] < final)
    evoludose = evoludose.loc[filterdate]

    # Comparativo entre doses
    fig5 = px.bar(evoludose, x='Data', y=['1ª Dose', '2ª Dose', '3ª Dose', 'Dose Única'], barmode='group',
                  template='xgridoff',
                  color_discrete_sequence=palette, title='<b>Comparativo entre a aplicação das doses</b>')
    fig5.update_yaxes(showgrid=False, tickmode="linear", tick0=0, dtick=20000),
    fig5.update_layout(autosize=True, height=700, margin=dict(t=85, b=50, l=70, r=50),
                       xaxis_tickangle=360, xaxis_title='', yaxis_title="Doses Aplicadas",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                       legend=dict(title_font=dict(color='white')),
                       xaxis_tickformat='Última atualização: %d de %b de %y', xaxis_hoverformat='%b %d, %Y')
    graf5 = fig5.to_html(full_html=False)

    return render_template('estados.html', form=form, min=mini, max=maxi,
                           graf1_evoludose=graf1, graf2_evoludose=graf2, graf3_evoludose=graf3,
                           graf4_evoludose=graf4, graf5_evoludose=graf5,
                           painel1_evoludose=vact, painel2_evoludose=popvac2, painel3_evoludose=popvac3,
                           painel4_evoludose=vacultd)


@app.route("/estado/leitos", methods=['GET'])
def leitos_main():
    random.shuffle(palette)
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    leitos = pd.read_csv(url6, dtype={'Departamento Regional de Saúde': 'category',
                                      'mm7d da Ocupação dos leitos de UTI e Enfermaria (%)': 'float64',
                                      'Nº de novas internações nos últimos 7 dias': 'int32',
                                      'Pacientes em tratamento na UTI': 'int16',
                                      'Total de leitos de UTI destinados à Covid': 'int16',
                                      'Ocupação dos leitos de UTI e Enfermaria (%)': 'float64',
                                      'Novos casos de internações (UTI e Enfermaria)': 'int16',
                                      'Pacientes em tratamento na Enfermaria': 'int16',
                                      'Total de leitos de Enfermaria destinados à Covid': 'int32'})
    leitos['Data'] = pd.to_datetime(leitos['Data'])
    flash_generate(leitos)
    # Filtro para só aparecer os dados referentes ao Estado de SP como um todo
    leitos = leitos[leitos['Departamento Regional de Saúde'] == 'Estado de São Paulo']

    nint = leitos['Novos casos de internações (UTI e Enfermaria)'].sum()
    nint = "{:,}".format(nint).replace(',', '.')
    tratmed = leitos['Pacientes em tratamento na UTI'] + leitos['Pacientes em tratamento na Enfermaria']
    tratmed = tratmed.mean()
    tratmed = int("{:.0f}".format(tratmed))
    tratmed = "{:,}".format(tratmed).replace(',', '.')
    ocupmed = leitos['Ocupação dos leitos de UTI e Enfermaria (%)'].mean()
    ocupmed = "{:.2f}".format(ocupmed).replace('.', ',')
    leitmed = leitos['Total de leitos de Enfermaria destinados à Covid'] + leitos['Total de leitos de UTI destinados ' \
                                                                                  'à Covid']
    leitmed = leitmed.mean()
    leitmed = int("{:.0f}".format(leitmed))
    leitmed = "{:,}".format(leitmed).replace(',', '.')

    # Ocupação dos leitos de UTI e enfermaria no Estado
    fig1 = px.bar(leitos, x='Data', y='Ocupação dos leitos de UTI e Enfermaria (%)', template='xgridoff',
                  color_discrete_sequence=palette, title='<b>Ocupação dos leitos de UTI e Enfermaria no Estado</b>')
    fig1.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=10),
    fig1.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(leitos['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
    fig1.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=80, r=50),
                       xaxis_title='', yaxis_title="Ocupação dos leitos (%)",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                       xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
    graf1 = fig1.to_html(full_html=False)

    # Número de leitos de UTI e enfermaria no Estado
    fig2 = px.bar(leitos, x='Data',
                  y=['Total de leitos de UTI destinados à Covid', 'Total de leitos de Enfermaria destinados à Covid'],
                  template='xgridoff', title='<b>Total de leitos de UTI e Enfermaria destinados à COVID-19</b>',
                  color_discrete_sequence=palette)
    fig2.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=2500),
    fig2.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(leitos['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
    fig2.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=100, r=50),
                       xaxis_title='', yaxis_title="Leitos destinados à COVID-19",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"), barmode='group',
                       legend=dict(title_font=dict(color='white')),
                       xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
    graf2 = fig2.to_html(full_html=False)
    data = leitos['Data'].max().strftime('%Y-%m-%d')
    utitotal = leitos[leitos['Data'] == data]['Total de leitos de UTI destinados à Covid'].values[0]
    enftotal = leitos[leitos['Data'] == data]['Total de leitos de Enfermaria destinados à Covid'].values[0]
    pop = 46649132
    info2_1 = pop / utitotal
    info2_1 = int("{:.0f}".format(info2_1))
    info2_1 = "{:,}".format(info2_1).replace(',', '.')
    info2_2 = pop / enftotal
    info2_2 = int("{:.0f}".format(info2_2))
    info2_2 = "{:,}".format(info2_2).replace(',', '.')
    if info2_1 == inf:
        info2_1 = 0
    if info2_2 == inf:
        info2_2 = 0
    if info2_1 == 'nan':
        info2_1 = 0
    if info2_2 == 'nan':
        info2_2 = 0

    # Número de pacientes em tratamento na UTI e enfermaria no Estado
    fig3 = px.bar(leitos, x='Data', y=['Pacientes em tratamento na UTI', 'Pacientes em tratamento na Enfermaria'],
                  template='xgridoff', title='<b>Total de pacientes nas UTIs e Enfermarias</b>',
                  color_discrete_sequence=palette)
    fig3.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=2500),
    fig3.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(leitos['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
    fig3.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=100, r=50),
                       xaxis_title='', yaxis_title="Pacientes em tratamento",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"), barmode='group',
                       legend=dict(title_font=dict(color='white')),
                       xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
    graf3 = fig3.to_html(full_html=False)

    # Novas internações por dia no Estado
    fig4 = px.line(leitos.sort_values(by=['Data'], ascending=[True]), x='Data',
                   y='Novos casos de internações (UTI e Enfermaria)', template='xgridoff',
                   color_discrete_sequence=palette, title='<b>Novas internações por dia no Estado</b>')
    fig4.update_traces(line=dict(width=6)),
    fig4.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=500),
    fig4.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(leitos['Data'].min().strftime('%Y-%m-%d'), maxi, freq='MS')),
    fig4.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=100, r=50),
                       xaxis_title='', yaxis_title="Internações (UTI e Enfermaria)",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                       xaxis_tickformat='%b/%y', xaxis_hoverformat='%b %d, %Y')
    graf4 = fig4.to_html(full_html=False)

    return render_template('estados.html', form=form, min=mini, max=maxi,
                           graf1_leitos=graf1, graf2_leitos=graf2, graf3_leitos=graf3, graf4_leitos=graf4,
                           painel1_leitos=nint, painel2_leitos=tratmed, painel3_leitos=ocupmed, painel4_leitos=leitmed,
                           info2_1_leitos=info2_1, info2_2_leitos=info2_2)


@app.route("/estado/isolamento-social", methods=['GET'])
def isola_main():
    random.shuffle(palette)
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    isola = pd.read_csv(url7,
                        dtype={'Município': 'category', 'codigo_ibge': 'category', 'Índice de Isolamento (%)': 'int8',
                               'Dia da Semana': 'category'})
    isola['Data'] = pd.to_datetime(isola['Data'])
    # Filtragem padrão para o main:
    isola = isola[isola['Município'] == 'Estado De São Paulo']
    final = (isola['Data'].max() + dt.timedelta(days=1)).strftime('%Y-%m-%d')
    inicial = (isola['Data'].max() - dt.timedelta(days=15)).strftime("%Y-%m-%d")
    filterdate = (isola['Data'] > inicial) & (isola['Data'] < final)
    isola = isola.loc[filterdate]
    flash_generate(isola)

    isomed = isola['Índice de Isolamento (%)'].mean()
    isomed = "{:.2f}".format(isomed).replace('.', ',')
    sem = {}
    for value in isola['Dia da Semana']:
        sem[value] = isola[isola['Dia da Semana'] == value]['Índice de Isolamento (%)'].sum()
    semax = max(sem, key=sem.get)
    semin = min(sem, key=sem.get)
    isodeal = isola[isola['Índice de Isolamento (%)'] >= 50].shape[0]

    # Histórico do indice de isolamento no estado de SP
    fig1 = px.bar(isola, orientation='v', y='Índice de Isolamento (%)', x='Data', color='Dia da Semana',
                  template='xgridoff', title='<b>Índice de Isolamento Social do Estado</b>',
                  color_discrete_sequence=palette)
    fig1.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=10),
    fig1.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(isola['Data'].min().strftime('%Y-%m-%d'),
                                             isola['Data'].max().strftime('%Y-%m-%d'), freq='D')),
    fig1.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=80, r=50),
                       xaxis_title='', yaxis_title="Isolamento Social (%)",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                       xaxis_tickformat='%b %d,<br>%y', xaxis_hoverformat='%b %d, %Y')
    graf1 = fig1.to_html(full_html=False)

    return render_template('estados.html', form=form, min=mini, max=maxi,
                           graf1_isola=graf1, painel1_isola=isomed, painel2_isola=semax,
                           painel3_isola=semin, painel4_isola=isodeal)


######################################################################################################################


# ROUTES DE PESQUISA NA PÁGINA DO ESTADO
@app.route("/estado/covidsp/search", methods=['POST', 'GET'])
def covidsp_search():
    random.shuffle(palette)
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        if request.form['startdate_field'] != '':
            start_request.append(parse(request.form['startdate_field'], dayfirst=True).strftime('%Y-%m-%d'))
            print(f'O start agora eh {start_request[-1]}')
            form_start.append(request.form['startdate_field'])
        else:
            start_request.append('dumby')
            form_start.append('')
        if request.form['enddate_field'] != '':
            end_request.append(parse(request.form['enddate_field'], dayfirst=True).strftime('%Y-%m-%d'))
            print(f'O end agora eh {end_request[-1]}')
            form_end.append(request.form['enddate_field'])
        else:
            end_request.append('dumby')
            form_end.append('')

    covidsp = covidsp_alt = pd.read_csv(url1, dtype={'Total de casos': 'int32', 'Total de óbitos': 'int32',
                                                     'Casos por dia': 'int32', 'Óbitos por dia': 'int16'})
    covidsp['Data'] = pd.to_datetime(covidsp['Data'])
    covidsp_alt['Data'] = pd.to_datetime(covidsp_alt['Data'])
    covidsp = date_filter_sp(covidsp, start_request, end_request)
    df_len = len(covidsp)
    print(f'O período da pesquisa é de {df_len} dias.')
    data = painel_date_filter(covidsp_alt, df_len, start_request, end_request)

    if not isinstance(covidsp, pd.DataFrame):
        return covidsp
    else:
        casost = covidsp['Total de casos'].max()
        casost = ("{:,}".format(casost)).replace(',', '.')
        obitost = covidsp['Total de óbitos'].max()
        obitost = ("{:,}".format(obitost)).replace(',', '.')
        try:
            casosult = covidsp['Casos por dia'].iloc[-1]
            casosult = ("{:,}".format(casosult)).replace(',', '.')
        except IndexError:
            casosult = covidsp['Casos por dia'].max()
            casosult = ("{:,}".format(casosult)).replace(',', '.')
        try:
            obitosult = covidsp['Óbitos por dia'].iloc[-1]
            obitosult = ("{:,}".format(obitosult)).replace(',', '.')
        except IndexError:
            obitosult = covidsp['Óbitos por dia'].max()
            obitosult = ("{:,}".format(obitosult)).replace(',', '.')

        # Gráfico casos por dia
        fig1 = px.bar(covidsp, x='Data', y='Casos por dia', color_discrete_sequence=palette,
                      title='<b>Casos por dia no Estado de São Paulo</b>',
                      hover_data=['Data', 'Total de casos', 'Casos por dia'],
                      template='xgridoff')
        fig1.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=2000),
        fig1.update_xaxes(tickangle=-45),
        fig1.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=100, r=50),
                           xaxis_title='', yaxis_title="Casos por dia",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"), barmode='stack',
                           xaxis_tickformat='%b %d,<br>%y', xaxis_hoverformat='%b %d, %Y')
        graf1 = fig1.to_html(full_html=False)
        casos = covidsp['Casos por dia'].sum()
        casos7 = data['Casos por dia'].sum()
        x = (casos * 100) / casos7 - 100
        info1 = "{:.2f}".format(x).replace('.', ',')
        if info1 == inf:
            info1 = 0
        if len(covidsp) > int(len(data)*150/100):
            info1 = 0
        if info1 == 'nan':
            info1 = 0
        try:
            varinit = data['Data'].min().strftime('%d/%m/%Y')
        except ValueError:
            varinit = covidsp['Data'].min().strftime('%d/%m/%Y')
        try:
            varend = data['Data'].max().strftime('%d/%m/%Y')
        except ValueError:
            varend = covidsp['Data'].max().strftime('%d/%m/%Y')
        if varinit == covidsp['Data'].min().strftime('%d/%m/%Y') and varend == covidsp['Data'].max().strftime('%d/%m/%Y'):
            info1 = ''
        else:
            info1 = Markup(f'<button class="hide-dado" onclick="dadosComp1()">Dados Complementares</button> '
                           f'<p id="df1" style="display: none">Variação de casos em comparação ao período anterior — '
                           f'{len(data)} dia(s) atrás <br>({varinit}~{varend}): <br> <span>{info1}%</span></p>')

        # Gráfico óbitos diários
        fig2 = px.bar(covidsp, x='Data', y='Óbitos por dia', color_discrete_sequence=palette,
                      title='<b>Óbitos por dia no Estado de São Paulo</b>',
                      hover_data=['Data', 'Total de óbitos', 'Óbitos por dia'],
                      template='xgridoff')
        fig2.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=100),
        fig2.update_xaxes(tickangle=-45),
        fig2.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                           xaxis_title='', yaxis_title="Óbitos por dia",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"), barmode='stack',
                           xaxis_tickformat='%b %d,<br>%y', xaxis_hoverformat='%b %d, %Y')
        graf2 = fig2.to_html(full_html=False)
        obi = covidsp['Óbitos por dia'].sum()
        obi7 = data['Óbitos por dia'].sum()
        x = (obi * 100) / obi7 - 100
        info2 = "{:.2f}".format(x).replace('.', ',')
        if info2 == inf:
            info2 = 0
        if len(covidsp) > int(len(data)*150/100):
            info2 = 0
        if info2 == 'nan':
            info2 = 0
        try:
            varinit = data['Data'].min().strftime('%d/%m/%Y')
        except ValueError:
            varinit = covidsp['Data'].min().strftime('%d/%m/%Y')
        try:
            varend = data['Data'].max().strftime('%d/%m/%Y')
        except ValueError:
            varend = covidsp['Data'].max().strftime('%d/%m/%Y')
        if varinit == covidsp['Data'].min().strftime('%d/%m/%Y') and varend == covidsp['Data'].max().strftime(
                '%d/%m/%Y'):
            info2 = ''
        else:
            info2 = Markup(f'<button class="hide-dado" onclick="dadosComp2()">Dados Complementares</button> '
                           f'<p id="df2" style="display: none">Variação de óbitos em comparação ao período anterior — '
                           f'{len(data)} dia(s) atrás <br>({varinit}~{varend}): <br> <span>{info2}%</span></p>')

        # Gráfico total de casos
        fig3 = px.line(covidsp.sort_values(by=['Data'], ascending=[True]), x='Data', y='Total de casos',
                       line_shape='linear', template='xgridoff',
                       color_discrete_sequence=palette, title='<b>Crescimento do nº de casos no Estado</b>',
                       hover_data=['Data', 'Total de casos', 'Casos por dia'], line_dash_sequence=['solid'],
                       render_mode='auto')
        fig3.update_traces(line=dict(width=6)),
        fig3.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=500000),
        fig3.update_xaxes(tickangle=-45),
        fig3.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=100, r=40),
                           xaxis_title='', yaxis_title="Total de casos",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                           xaxis_tickformat='%b %d,<br>%y', xaxis_hoverformat='%b %d, %Y')
        graf3 = fig3.to_html(full_html=False)
        pop = 46649132  # população do estado de SP
        casos = covidsp['Total de casos'].max()
        inc = casos / (pop - casos) * 100000
        info3 = int("{:.0f}".format(inc))
        info3 = ("{:,}".format(info3)).replace(',', '.')
        if info3 == inf:
            info3 = 0
        if info3 == 'nan':
            info3 = 0

        # Gráfico total de óbitos
        fig4 = px.line(covidsp.sort_values(by=['Data'], ascending=[True]), x='Data', y='Total de óbitos',
                       line_shape='linear', template='xgridoff', color_discrete_sequence=palette,
                       line_dash_sequence=['solid'],
                       render_mode='auto', hover_data=['Data', 'Total de óbitos', 'Óbitos por dia'],
                       title='<b>Crescimento do nº de óbitos no Estado</b>')
        fig4.update_traces(line=dict(width=6)),
        fig4.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=15000),
        fig4.update_xaxes(tickangle=-45),
        fig4.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=100, r=40),
                           xaxis_title='', yaxis_title="Total de óbitos",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                           xaxis_tickformat='%b %d,<br>%y', xaxis_hoverformat='%b %d, %Y')
        graf4 = fig4.to_html(full_html=False)
        obtotal = covidsp['Total de óbitos'].max()
        casostotal = covidsp['Total de casos'].max()
        let = (obtotal / casostotal) * 100
        info4 = "{:.2f}".format(let).replace('.', ',')
        if info4 == inf:
            info4 = 0
        if info4 == 'nan':
            info4 = 0

        return render_template('estados.html', form=form, min=mini, max=maxi,
                               start=form_start[-1], end=form_end[-1],
                               graf1_covidsp=graf1, graf2_covidsp=graf2, graf3_covidsp=graf3, graf4_covidsp=graf4,
                               painel1_covidsp=casost, painel2_covidsp=obitost, painel3_covidsp=casosult,
                               painel4_covidsp=obitosult, info1_covidsp=info1, info2_covidsp=info2,
                               info3_covidsp=info3, info4_covidsp=info4)


@app.route("/estado/vacina/search", methods=['POST', 'GET'])
def evoludose_search():
    random.shuffle(palette)
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        if request.form['startdate_field'] != '':
            start_request.append(parse(request.form['startdate_field'], dayfirst=True).strftime('%Y-%m-%d'))
            print(f'O start agora eh {start_request[-1]}')
            form_start.append(request.form['startdate_field'])
        else:
            start_request.append('dumby')
            form_start.append('')
        if request.form['enddate_field'] != '':
            end_request.append(parse(request.form['enddate_field'], dayfirst=True).strftime('%Y-%m-%d'))
            print(f'O end agora eh {end_request[-1]}')
            form_end.append(request.form['enddate_field'])
        else:
            end_request.append('dumby')
            form_end.append('')

    evoludose = evoludose_alt = pd.read_csv(url5,
                                            dtype={'1ª Dose': 'int32', '2ª Dose': 'int32', '3ª Dose': 'int32',
                                                   'Dose Única': 'int32'})
    evoludose['Data'] = pd.to_datetime(evoludose['Data'])
    evoludose_alt['Data'] = pd.to_datetime(evoludose_alt['Data'])
    datavac = date_end_filter(evoludose, end_request)
    evoludose = date_filter_sp(evoludose, start_request, end_request)
    df_len = len(evoludose)
    print(f'O período da pesquisa é de {df_len} dias.')
    data = painel_date_filter(evoludose_alt, df_len, start_request, end_request)

    if not isinstance(evoludose, pd.DataFrame):
        return evoludose
    else:
        vact = evoludose['1ª Dose'].sum() + evoludose['2ª Dose'].sum() + evoludose['3ª Dose'].sum() + evoludose['Dose Única'].sum()
        vact = "{:,}".format(vact).replace(',', '.')
        pop = 46649132
        vac2 = datavac['2ª Dose'].sum() + datavac['Dose Única'].sum()
        popvac2 = (vac2 * 100) / pop
        popvac2 = "{:.2f}".format(popvac2).replace('.', ',') + '%'
        vac3 = datavac['3ª Dose'].sum()
        popvac3 = (vac3 * 100) / pop
        popvac3 = "{:.2f}".format(popvac3).replace('.', ',') + '%'
        try:
            vacultd = evoludose['1ª Dose'].iloc[-1] + evoludose['2ª Dose'].iloc[-1] + evoludose['3ª Dose'].iloc[-1] + evoludose['Dose Única'].iloc[-1]
            vacultd = "{:,}".format(vacultd).replace(',', '.')
        except IndexError:
            vacultd = evoludose['1ª Dose'].max() + evoludose['2ª Dose'].max() + evoludose['3ª Dose'].max() + evoludose['Dose Única'].max()
            vacultd = "{:,}".format(vacultd).replace(',', '.')

        # Evolução 1ª dose
        fig1 = px.bar(evoludose, x='Data', y='1ª Dose', template='xgridoff',
                      color_discrete_sequence=palette, title='<b>Evolução da aplicação da 1ª dose</b>')
        fig1.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=50000),
        fig1.update_xaxes(tickangle=-45),
        fig1.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=70, r=50),
                           xaxis_title='', yaxis_title="Doses aplicadas",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                           xaxis_tickformat='%b %d,<br>%y', xaxis_hoverformat='%b %d, %Y')
        graf1 = fig1.to_html(full_html=False)
        dose = evoludose['1ª Dose'].sum()
        dose7 = data['1ª Dose'].sum()
        evol = (dose * 100) / dose7 - 100
        info1 = "{:.2f}".format(evol).replace('.', ',')
        if info1 == inf:
            info1 = 0
        if len(evoludose) > int(len(data) * 150 / 100):
            info1 = 0
        if info1 == 'nan':
            info1 = 0
        try:
            varinit = data['Data'].min().strftime('%d/%m/%Y')
        except ValueError:
            varinit = evoludose['Data'].min().strftime('%d/%m/%Y')
        try:
            varend = data['Data'].max().strftime('%d/%m/%Y')
        except ValueError:
            varend = evoludose['Data'].max().strftime('%d/%m/%Y')
        if varinit == evoludose['Data'].min().strftime('%d/%m/%Y') and varend == evoludose['Data'].max().strftime('%d/%m/%Y'):
            info1 = ''
        else:
            info1 = Markup(f'<button class="hide-dado" onclick="dadosComp5()">Dados Complementares</button> '
                           f'<p id="df5" style="display: none">Variação na aplicação de primeira dose em comparação ao '
                           f'período anterior — {len(data)} dia(s) atrás <br> ({varinit}~{varend}): <br> '
                           f'<span>{info1}%</span></p>')

        # Evolução 2ª dose
        fig2 = px.bar(evoludose, x='Data', y='2ª Dose', template='xgridoff',
                      color_discrete_sequence=palette, title='<b>Evolução da aplicação da 2ª dose</b>')
        fig2.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=50000),
        fig2.update_xaxes(tickangle=-45),
        fig2.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=100, r=50),
                           xaxis_title='', yaxis_title="Doses aplicadas",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                           xaxis_tickformat='%b %d,<br>%y', xaxis_hoverformat='%b %d, %Y')
        graf2 = fig2.to_html(full_html=False)
        dose = evoludose['2ª Dose'].sum()
        dose7 = data['2ª Dose'].sum()
        evol = (dose * 100) / dose7 - 100
        info2 = "{:.2f}".format(evol).replace('.', ',')
        if info2 == inf:
            info2 = 0
        if len(evoludose) > int(len(data) * 150 / 100):
            info2 = 0
        if info2 == 'nan':
            info2 = 0
        try:
            varinit = data['Data'].min().strftime('%d/%m/%Y')
        except ValueError:
            varinit = evoludose['Data'].min().strftime('%d/%m/%Y')
        try:
            varend = data['Data'].max().strftime('%d/%m/%Y')
        except ValueError:
            varend = evoludose['Data'].max().strftime('%d/%m/%Y')
        if varinit == evoludose['Data'].min().strftime('%d/%m/%Y') and varend == evoludose['Data'].max().strftime('%d/%m/%Y'):
            info2 = ''
        else:
            info2 = Markup(f'<button class="hide-dado" onclick="dadosComp6()">Dados Complementares</button> '
                           f'<p id="df6" style="display: none">Variação na aplicação de segunda dose em comparação ao '
                           f'período anterior — {len(data)} dia(s) atrás <br> ({varinit}~{varend}): <br> '
                           f'<span>{info2}%</span></p>')

        # Evolução 3ª dose
        fig3 = px.bar(evoludose, x='Data', y='3ª Dose', template='xgridoff',
                      color_discrete_sequence=palette, title='<b>Evolução da aplicação da 3ª dose</b>')
        fig3.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=20000),
        fig3.update_xaxes(tickangle=-45),
        fig3.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=100, r=50),
                           xaxis_title='', yaxis_title="Doses aplicadas",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                           xaxis_tickformat='%b %d,<br>%y', xaxis_hoverformat='%b %d, %Y')
        graf3 = fig3.to_html(full_html=False)
        dose = evoludose['3ª Dose'].sum()
        dose7 = data['3ª Dose'].sum()
        evol = (dose * 100) / dose7 - 100
        info3 = "{:.2f}".format(evol).replace('.', ',')
        if info3 == inf:
            info3 = 0
        if len(evoludose) > int(len(data) * 150 / 100):
            info3 = 0
        if info3 == 'nan':
            info3 = 0
        try:
            varinit = data['Data'].min().strftime('%d/%m/%Y')
        except ValueError:
            varinit = evoludose['Data'].min().strftime('%d/%m/%Y')
        try:
            varend = data['Data'].max().strftime('%d/%m/%Y')
        except ValueError:
            varend = evoludose['Data'].max().strftime('%d/%m/%Y')
        if varinit == evoludose['Data'].min().strftime('%d/%m/%Y') and varend == evoludose['Data'].max().strftime('%d/%m/%Y'):
            info3 = ''
        else:
            info3 = Markup(f'<button class="hide-dado" onclick="dadosComp7()">Dados Complementares</button> '
                           f'<p id="df7" style="display: none">Variação na aplicação de terceira dose em comparação ao '
                           f'período anterior — {len(data)} dia(s) atrás <br> ({varinit}~{varend}): <br> '
                           f'<span>{info3}%</span></p>')

        # Evolução dose única
        fig4 = px.bar(evoludose, x='Data', y='Dose Única', template='xgridoff',
                      color_discrete_sequence=palette, title='<b>Evolução da aplicação da dose única</b>')
        fig4.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=20000),
        fig4.update_xaxes(tickangle=-45),
        fig4.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=70, r=50),
                           xaxis_title='', yaxis_title="Doses aplicadas",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                           xaxis_tickformat='%b %d,<br>%y', xaxis_hoverformat='%b %d, %Y')
        graf4 = fig4.to_html(full_html=False)
        dose = evoludose['Dose Única'].sum()
        dose7 = data['Dose Única'].sum()
        evol = (dose * 100) / dose7 - 100
        info4 = "{:.2f}".format(evol).replace('.', ',')
        if info4 == inf:
            info4 = 0
        if len(evoludose) > int(len(data) * 150 / 100):
            info4 = 0
        if info4 == 'nan':
            info4 = 0
        try:
            varinit = data['Data'].min().strftime('%d/%m/%Y')
        except ValueError:
            varinit = evoludose['Data'].min().strftime('%d/%m/%Y')
        try:
            varend = data['Data'].max().strftime('%d/%m/%Y')
        except ValueError:
            varend = evoludose['Data'].max().strftime('%d/%m/%Y')
        if varinit == evoludose['Data'].min().strftime('%d/%m/%Y') and varend == evoludose['Data'].max().strftime('%d/%m/%Y'):
            info4 = ''
        else:
            info4 = Markup(f'<button class="hide-dado" onclick="dadosComp8()">Dados Complementares</button> '
                           f'<p id="df8" style="display: none">Variação na aplicação de doses únicas em comparação ao '
                           f'período anterior — {len(data)} dia(s) atrás <br> ({varinit}~{varend}): <br> '
                           f'<span>{info4}%</span></p>')

        # Filtros apenas para dados totais
        final = (evoludose['Data'].max() + dt.timedelta(days=1)).strftime('%Y-%m-%d')
        inicial = (evoludose['Data'].max() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
        filterdate = (evoludose['Data'] > inicial) & (evoludose['Data'] < final)
        evoludose = evoludose.loc[filterdate]

        # Comparativo entre doses
        fig5 = px.bar(evoludose, x='Data', y=['1ª Dose', '2ª Dose', '3ª Dose', 'Dose Única'], barmode='group',
                      template='xgridoff', title='<b>Comparativo entre a aplicação das doses</b>',
                      color_discrete_sequence=palette)
        fig5.update_yaxes(showgrid=False, tickmode="linear", tick0=0, dtick=20000),
        fig5.update_layout(autosize=True, height=700, margin=dict(t=85, b=50, l=100, r=50),
                           xaxis_tickangle=360, xaxis_title='', yaxis_title="Doses Aplicadas",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                           legend=dict(title_font=dict(color='white')),
                           xaxis_tickformat='Última atualização: %d de %b de %y', xaxis_hoverformat='%b %d, %Y')
        graf5 = fig5.to_html(full_html=False)
        return render_template('estados.html', form=form, min=mini, max=maxi,
                               start=form_start[-1], end=form_end[-1],
                               graf1_evoludose=graf1, graf2_evoludose=graf2, graf3_evoludose=graf3,
                               graf4_evoludose=graf4, graf5_evoludose=graf5,
                               painel1_evoludose=vact, painel2_evoludose=popvac2, painel3_evoludose=popvac3,
                               painel4_evoludose=vacultd, info1_evoludose=info1, info2_evoludose=info2,
                               info3_evoludose=info3, info4_evoludose=info4)


@app.route("/estado/leitos/search", methods=['POST', 'GET'])
def leitos_search():
    random.shuffle(palette)
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        if request.form['startdate_field'] != '':
            start_request.append(parse(request.form['startdate_field'], dayfirst=True).strftime('%Y-%m-%d'))
            print(f'O start agora eh {start_request[-1]}')
            form_start.append(request.form['startdate_field'])
        else:
            start_request.append('dumby')
            form_start.append('')
        if request.form['enddate_field'] != '':
            end_request.append(parse(request.form['enddate_field'], dayfirst=True).strftime('%Y-%m-%d'))
            print(f'O end agora eh {end_request[-1]}')
            form_end.append(request.form['enddate_field'])
        else:
            end_request.append('dumby')
            form_end.append('')

    leitos = leitos_alt = pd.read_csv(url6, dtype={'Departamento Regional de Saúde': 'category',
                                                   'mm7d da Ocupação dos leitos de UTI e Enfermaria (%)': 'float64',
                                                   'Nº de novas internações nos últimos 7 dias': 'int32',
                                                   'Pacientes em tratamento na UTI': 'int16',
                                                   'Total de leitos de UTI destinados à Covid': 'int16',
                                                   'Ocupação dos leitos de UTI e Enfermaria (%)': 'float64',
                                                   'Novos casos de internações (UTI e Enfermaria)': 'int16',
                                                   'Pacientes em tratamento na Enfermaria': 'int16',
                                                   'Total de leitos de Enfermaria destinados à Covid': 'int32'})
    leitos['Data'] = pd.to_datetime(leitos['Data'])
    leitos_alt['Data'] = pd.to_datetime(leitos_alt['Data'])
    leitos = date_filter_sp(leitos, start_request, end_request)
    df_len = len(leitos)
    print(f'O período da pesquisa é de {df_len} dias.')
    data = painel_date_filter(leitos_alt, df_len, start_request, end_request)

    if not isinstance(leitos, pd.DataFrame):
        return leitos
    else:
        # Filtro para só aparecer os dados referentes ao Estado de SP como um todo
        leitos = leitos[leitos['Departamento Regional de Saúde'] == 'Estado de São Paulo']
        data = data[data['Departamento Regional de Saúde'] == 'Estado de São Paulo']

        nint = leitos['Novos casos de internações (UTI e Enfermaria)'].sum()
        nint = "{:,}".format(nint).replace(',', '.')
        tratmed = leitos['Pacientes em tratamento na UTI'] + leitos['Pacientes em tratamento na Enfermaria']
        tratmed = tratmed.mean()
        tratmed = int("{:.0f}".format(tratmed))
        tratmed = "{:,}".format(tratmed).replace(',', '.')
        ocupmed = leitos['Ocupação dos leitos de UTI e Enfermaria (%)'].mean()
        ocupmed = "{:.2f}".format(ocupmed).replace('.', ',')
        leitmed = leitos['Total de leitos de Enfermaria destinados à Covid'] + leitos['Total de leitos de UTI ' \
                                                                                      'destinados à Covid']
        leitmed = leitmed.mean()
        leitmed = int("{:.0f}".format(leitmed))
        leitmed = "{:,}".format(leitmed).replace(',', '.')

        # Ocupação dos leitos de UTI e enfermaria no Estado
        fig1 = px.bar(leitos, x='Data', y='Ocupação dos leitos de UTI e Enfermaria (%)', template='xgridoff',
                      color_discrete_sequence=palette, title='<b>Ocupação dos leitos de UTI e Enfermaria no Estado</b>')
        fig1.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=10),
        fig1.update_xaxes(tickangle=-45),
        fig1.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=80, r=50),
                           xaxis_title='', yaxis_title="Ocupação dos leitos (%)",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                           xaxis_tickformat='%b %d,<br>%y', xaxis_hoverformat='%b %d, %Y')
        graf1 = fig1.to_html(full_html=False)

        # Número de leitos de UTI e enfermaria no Estado
        fig2 = px.bar(leitos, x='Data', y=['Total de leitos de UTI destinados à Covid',
                                           'Total de leitos de Enfermaria destinados à Covid'], template='xgridoff',
                      color_discrete_sequence=palette,
                      title='<b>Total de leitos de UTI e Enfermaria destinados à COVID-19</b>')
        fig2.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=2500),
        fig2.update_xaxes(tickangle=-45),
        fig2.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=100, r=50),
                           xaxis_title='', yaxis_title="Leitos destinados à COVID-19",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"), barmode='group',
                           legend=dict(title_font=dict(color='white')),
                           xaxis_tickformat='%b %d,<br>%y', xaxis_hoverformat='%b %d, %Y')
        graf2 = fig2.to_html(full_html=False)
        dataleitos = leitos['Data'].max().strftime('%Y-%m-%d')
        utitotal = leitos[leitos['Data'] == dataleitos]['Total de leitos de UTI destinados à Covid'].values[0]
        enftotal = leitos[leitos['Data'] == dataleitos]['Total de leitos de Enfermaria destinados à Covid'].values[0]
        pop = 46649132
        info2_1 = pop / utitotal
        info2_1 = int("{:.0f}".format(info2_1))
        info2_1 = "{:,}".format(info2_1).replace(',', '.')
        info2_2 = pop / enftotal
        info2_2 = int("{:.0f}".format(info2_2))
        info2_2 = "{:,}".format(info2_2).replace(',', '.')
        if info2_1 == inf:
            info2_1 = 0
        if info2_2 == inf:
            info2_2 = 0
        if info2_1 == 'nan':
            info2_1 = 0
        if info2_2 == 'nan':
            info2_2 = 0

        # Número de pacientes em tratamento na UTI e enfermaria no Estado
        fig3 = px.bar(leitos, x='Data', y=['Pacientes em tratamento na UTI', 'Pacientes em tratamento na Enfermaria'],
                      template='xgridoff', title='<b>Total de pacientes nas UTIs e Enfermarias</b>',
                      color_discrete_sequence=palette)
        fig3.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=2500),
        fig3.update_xaxes(tickangle=-45),
        fig3.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=100, r=50),
                           xaxis_title='', yaxis_title="Pacientes em tratamento",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"), barmode='group',
                           legend=dict(title_font=dict(color='white')),
                           xaxis_tickformat='%b %d,<br>%y', xaxis_hoverformat='%b %d, %Y')
        graf3 = fig3.to_html(full_html=False)

        # Novas internações por dia no Estado
        fig4 = px.line(leitos.sort_values(by=['Data'], ascending=[True]), x='Data',
                       y='Novos casos de internações (UTI e Enfermaria)', template='xgridoff',
                       color_discrete_sequence=palette, title='<b>Novas internações por dia no Estado</b>')
        fig4.update_traces(line=dict(width=6)),
        fig4.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=500),
        fig4.update_xaxes(tickangle=-45),
        fig4.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=100, r=50),
                           xaxis_title='', yaxis_title="Internações (UTI e Enfermaria)",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                           xaxis_tickformat='%b %d,<br>%y', xaxis_hoverformat='%b %d, %Y')
        graf4 = fig4.to_html(full_html=False)
        inter = leitos['Novos casos de internações (UTI e Enfermaria)'].sum()
        inter7 = data['Novos casos de internações (UTI e Enfermaria)'].sum()
        interna = (inter * 100) / inter7 - 100
        info4 = "{:.2f}".format(interna).replace('.', ',')
        if info4 == inf:
            info4 = 0
        if len(leitos) > int(len(data) * 150 / 100):
            info4 = 0
        if info4 == 'nan':
            info4 = 0
        try:
            varinit = data['Data'].min().strftime('%d/%m/%Y')
        except ValueError:
            varinit = leitos['Data'].min().strftime('%d/%m/%Y')
        try:
            varend = data['Data'].max().strftime('%d/%m/%Y')
        except ValueError:
            varend = leitos['Data'].max().strftime('%d/%m/%Y')
        if varinit == leitos['Data'].min().strftime('%d/%m/%Y') and varend == leitos['Data'].max().strftime('%d/%m/%Y'):
            info4 = ''
        else:
            info4 = Markup(f'<button class="hide-dado" onclick="dadosComp13()">Dados Complementares</button> '
                           f'<p id="df13" style="display: none">Variação no número de internações em comparação ao '
                           f'período anterior — {len(data)} dia(s) atrás <br> ({varinit}~{varend}): <br> '
                           f'<span>{info4}%</span></p>')

        return render_template('estados.html', form=form, min=mini, max=maxi,
                               start=form_start[-1], end=form_end[-1],
                               graf1_leitos=graf1, graf2_leitos=graf2, graf3_leitos=graf3, graf4_leitos=graf4,
                               painel1_leitos=nint, painel2_leitos=tratmed, painel3_leitos=ocupmed,
                               painel4_leitos=leitmed,
                               info2_1_leitos=info2_1, info2_2_leitos=info2_2, info4_leitos=info4)


@app.route("/estado/isolamento-social/search", methods=['POST', 'GET'])
def isola_search():
    random.shuffle(palette)
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        if request.form['startdate_field'] != '':
            start_request.append(parse(request.form['startdate_field'], dayfirst=True).strftime('%Y-%m-%d'))
            print(f'O start agora eh {start_request[-1]}')
            form_start.append(request.form['startdate_field'])
        else:
            start_request.append('dumby')
            form_start.append('')
        if request.form['enddate_field'] != '':
            end_request.append(parse(request.form['enddate_field'], dayfirst=True).strftime('%Y-%m-%d'))
            print(f'O end agora eh {end_request[-1]}')
            form_end.append(request.form['enddate_field'])
        else:
            end_request.append('dumby')
            form_end.append('')

    isola = pd.read_csv(url7,
                        dtype={'Município': 'category', 'codigo_ibge': 'category',
                               'Índice de Isolamento (%)': 'int8',
                               'Dia da Semana': 'category'})
    isola['Data'] = pd.to_datetime(isola['Data'])
    isola = date_filter_sp(isola, start_request, end_request)

    if not isinstance(isola, pd.DataFrame):
        return isola
    else:
        # Filtragem padrão para o search:
        isola = isola[isola['Município'] == 'Estado De São Paulo']

        isomed = isola['Índice de Isolamento (%)'].mean()
        isomed = "{:.2f}".format(isomed).replace('.', ',')
        sem = {}
        for value in isola['Dia da Semana']:
            sem[value] = isola[isola['Dia da Semana'] == value]['Índice de Isolamento (%)'].sum()
        semax = max(sem, key=sem.get)
        semin = min(sem, key=sem.get)
        isodeal = isola[isola['Índice de Isolamento (%)'] >= 50].shape[0]

        # Histórico do indice de isolamento no estado de SP
        fig1 = px.bar(isola, orientation='v', y='Índice de Isolamento (%)', x='Data', color='Dia da Semana',
                      template='xgridoff', title='<b>Índice de Isolamento Social do Estado</b>',
                      color_discrete_sequence=palette)
        fig1.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=10),
        fig1.update_xaxes(tickangle=-45),
        fig1.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=80, r=50),
                           xaxis_title='', yaxis_title="Isolamento Social (%)",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                           xaxis_tickformat='%b %d,<br>%y', xaxis_hoverformat='%b %d, %Y')
        graf1 = fig1.to_html(full_html=False)

        return render_template('estados.html', form=form, min=mini, max=maxi,
                               start=form_start[-1], end=form_end[-1],
                               graf1_isola=graf1, painel1_isola=isomed, painel2_isola=semax,
                               painel3_isola=semin, painel4_isola=isodeal)


####################################################################################################################


# ROUTES INICIAIS DA PÁGINA DOS MUNICÍPIOS
@app.route("/municipios", methods=['GET'])
@app.route("/municipios/covidsp", methods=['GET'])
def covidmuni_main():
    random.shuffle(palette)
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    covidmuni = pd.read_csv(url2, dtype={'Município': 'category', 'codigo_ibge': 'category', 'Total de Casos': 'int32',
                                         'Novos Casos': 'int16', 'Total de Óbitos': 'int32', 'Novos Óbitos': 'int16',
                                         'Mesorregião': 'category', 'Microrregião': 'category', 'pop': 'int32'})
    covidmuni['Data'] = pd.to_datetime(covidmuni['Data'])
    correct = covidmuni['Data'] < '2021-11-29'
    covidmuni = covidmuni.loc[correct]
    # Filtragem padrão dos dataframes com município em 'main' functions:
    covidmuni = covidmuni_alt = covidmuni.query(
        "Município == 'São José dos Campos' | Município == 'Taubaté' | Município == 'Jacareí' | Município == "
        "'Lorena' | Município == 'Pindamonhangaba' | Município == 'Caraguatatuba' | Município == "
        "'Guaratinguetá' | Município == 'Caçapava' | Município == 'Ubatuba' | Município == 'São Sebastião'")
    final = (covidmuni['Data'].max() + dt.timedelta(days=1)).strftime('%Y-%m-%d')
    inicial = (covidmuni['Data'].max() - dt.timedelta(days=15)).strftime("%Y-%m-%d")
    filterdate = (covidmuni['Data'] > inicial) & (covidmuni['Data'] < final)
    covidmuni = covidmuni.loc[filterdate]
    flash_generate(covidmuni)
    flash(Markup(f'<h1 class="cidades"> Dados das dez maiores cidades do Vale do Paraíba. Para acessar outras cidades, '
                 f'faça uma pesquisa personalizada.</h1>'))
    df_len = covidmuni['Data'].nunique()
    print(f'O período da pesquisa é de {df_len} dias.')
    covidmuni_alt['Data'] = pd.to_datetime(covidmuni_alt['Data'])
    perioinicial = df_len + 1
    periofinal = df_len - 1
    inicial = pd.to_datetime(covidmuni['Data'].min(), format='%Y-%m-%d')
    inicial = (inicial - dt.timedelta(days=perioinicial)).strftime("%Y-%m-%d")
    final = pd.to_datetime(covidmuni['Data'].max(), format='%Y-%m-%d')
    final = (final - dt.timedelta(days=periofinal)).strftime("%Y-%m-%d")
    filterdate = (covidmuni_alt['Data'] > inicial) & (covidmuni_alt['Data'] < final)
    data = covidmuni_alt.loc[filterdate]

    casost = covidmuni['Total de Casos'].max()
    casost = ("{:,}".format(casost)).replace(',', '.')
    obitost = covidmuni['Total de Óbitos'].max()
    obitost = ("{:,}".format(obitost)).replace(',', '.')
    try:
        casosult = covidmuni['Novos Casos'].iloc[-1]
        casosult = ("{:,}".format(casosult)).replace(',', '.')
    except IndexError:
        casosult = covidmuni['Novos Casos'].max()
        casosult = ("{:,}".format(casosult)).replace(',', '.')
    try:
        obitosult = covidmuni['Novos Óbitos'].iloc[-1]
        obitosult = ("{:,}".format(obitosult)).replace(',', '.')
    except IndexError:
        obitosult = covidmuni['Novos Óbitos'].max()
        obitosult = ("{:,}".format(obitosult)).replace(',', '.')

    # Casos diários por município
    fig1 = px.bar(covidmuni, x='Data', y='Novos Casos', color='Município', hover_data=['Novos Casos'],
                  color_discrete_sequence=palette,
                  title='<b>Casos confirmados por dia e por Município</b>', template='xgridoff')
    fig1.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=150),
    fig1.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(covidmuni['Data'].min().strftime('%Y-%m-%d'),
                                             covidmuni['Data'].max().strftime('%Y-%m-%d'), freq='D')),
    fig1.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=70, r=50),
                       xaxis_title='', yaxis_title="Novos Casos",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"), barmode='stack',
                       xaxis_tickformat='%b %d,<br>%y', xaxis_hoverformat='%b %d, %Y')
    graf1 = fig1.to_html(full_html=False)
    munis = {}
    for value in covidmuni['Município']:
        munis[value] = covidmuni[covidmuni['Município'] == value]['Novos Casos'].sum()
        casos7 = data[data['Município'] == value]['Novos Casos'].sum()
        x = (munis[value] * 100) / casos7 - 100
        x = "{:.2f}".format(x).replace('.', ',')
        if x == inf:
            x = 0
        if len(covidmuni) > int(len(data) * 150 / 100):
            x = 0
        if x == 'nan':
            x = 0
        munis[value] = x
    try:
        varinit = data['Data'].min().strftime('%d/%m/%Y')
    except ValueError:
        varinit = covidmuni['Data'].min().strftime('%d/%m/%Y')
    try:
        varend = data['Data'].max().strftime('%d/%m/%Y')
    except ValueError:
        varend = covidmuni['Data'].max().strftime('%d/%m/%Y')
    if varinit == covidmuni['Data'].min().strftime('%d/%m/%Y') and varend == covidmuni['Data'].max().strftime('%d/%m/%Y'):
        info1 = ''
    else:
        info1 = ['{} <span>{}%</span> <br> <br>'.format(key, value) for key, value in munis.items()]
        info1 = ''.join(str(e) for e in info1)
        info1 = Markup(f'<p id="df1" style="display: none">Variação de casos em comparação ao período anterior — '
                       f'{df_len} dia(s) atrás <br> ({varinit}~{varend}): <br> <br><span>{info1}</span></p>')

    # Óbitos diários por município
    fig2 = px.bar(covidmuni, x='Data', y='Novos Óbitos', color='Município', hover_data=['Novos Óbitos'],
                  color_discrete_sequence=palette,
                  title='<b>Óbitos confirmados por dia e por Município</b>', template='xgridoff')
    fig2.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=25),
    fig2.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(covidmuni['Data'].min().strftime('%Y-%m-%d'),
                                             covidmuni['Data'].max().strftime('%Y-%m-%d'), freq='D')),
    fig2.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=80, r=50),
                       xaxis_title='', yaxis_title="Novos Óbitos",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"), barmode='stack',
                       xaxis_tickformat='%b %d,<br>%y', xaxis_hoverformat='%b %d, %Y')
    graf2 = fig2.to_html(full_html=False)
    munis = {}
    for value in covidmuni['Município']:
        munis[value] = covidmuni[covidmuni['Município'] == value]['Novos Óbitos'].sum()
        obi7 = data[data['Município'] == value]['Novos Óbitos'].sum()
        x = (munis[value] * 100) / obi7 - 100
        x = "{:.2f}".format(x).replace('.', ',')
        if x == inf:
            x = 0
        if len(covidmuni) > int(len(data) * 150 / 100):
            x = 0
        if x == 'nan':
            x = 0
        munis[value] = x
    try:
        varinit = data['Data'].min().strftime('%d/%m/%Y')
    except ValueError:
        varinit = covidmuni['Data'].min().strftime('%d/%m/%Y')
    try:
        varend = data['Data'].max().strftime('%d/%m/%Y')
    except ValueError:
        varend = covidmuni['Data'].max().strftime('%d/%m/%Y')
    if varinit == covidmuni['Data'].min().strftime('%d/%m/%Y') and varend == covidmuni['Data'].max().strftime('%d/%m/%Y'):
        info2 = ''
    else:
        info2 = ['{} <span>{}%</span> <br> <br>'.format(key, value) for key, value in munis.items()]
        info2 = ''.join(str(e) for e in info2)
        info2 = Markup(f'<p id="df2" style="display: none">Variação de óbitos em comparação ao período anterior — '
                       f'{df_len} dia(s) atrás <br> ({varinit}~{varend}): <br> <br><span>{info2}</span></p>')

    # Filtros apenas para dados totais
    final = (covidmuni['Data'].max() + dt.timedelta(days=1)).strftime('%Y-%m-%d')
    inicial = (covidmuni['Data'].max() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
    filterdate = (covidmuni['Data'] > inicial) & (covidmuni['Data'] < final)
    covidmuni = covidmuni.loc[filterdate]
    covidmuni = covidmuni.query(
        "Município == 'São José dos Campos' | Município == 'Taubaté' | Município == 'Jacareí' | Município == "
        "'Lorena' | Município == 'Pindamonhangaba' | Município == 'Caraguatatuba' | Município == "
        "'Guaratinguetá' | Município == 'Caçapava' | Município == 'Ubatuba' | Município == 'São Sebastião'")

    # Total de mortes por município
    fig3 = px.pie(covidmuni, values='Total de Óbitos', names='Município', color='Município',
                  title='<b>Comparativo entre o total de óbitos por Município</b>', template='xgridoff',
                  color_discrete_sequence=palette)
    fig3.update_xaxes(type='date')
    fig3.update_layout(autosize=True)
    fig3.update_yaxes(showgrid=False),
    fig3.update_layout(autosize=True, height=700, margin=dict(t=85, b=45, l=250, r=250),
                       xaxis_tickangle=360,
                       xaxis_title='', yaxis_title="Total de Óbitos",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"))
    graf3 = fig3.to_html(full_html=False)
    munis = {}
    for value in covidmuni['Município']:
        obtotal = covidmuni[covidmuni['Município'] == value]['Total de Óbitos'].max()
        casostotal = covidmuni[covidmuni['Município'] == value]['Total de Casos'].max()
        let = (obtotal / casostotal) * 100
        let = "{:.2f}".format(let).replace('.', ',')
        if let == inf:
            let = 0
        if let == 'nan':
            let = 0
        munis[value] = let
    info3 = ['{} <span>{}%</span> <br> <br>'.format(key, value) for key, value in munis.items()]
    info3 = ''.join(str(e) for e in info3)
    info3 = Markup(f'<p id="df3" style="display: none">Taxa de letalidade no período: '
                   f'<br> <br><span>{info3}</span></p>')

    # Total de casos por município
    fig4 = px.pie(covidmuni, values='Total de Casos', names='Município', color='Município',
                  title='<b>Comparativo entre o total de casos por Município</b>', template='xgridoff',
                  color_discrete_sequence=palette)
    fig4.update_xaxes(type='date')
    fig4.update_layout(autosize=True)
    fig4.update_yaxes(showgrid=False),
    fig4.update_layout(autosize=True, height=700, margin=dict(t=85, b=45, l=250, r=250),
                       xaxis_tickangle=360,
                       xaxis_title='', yaxis_title="Total de Casos",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"))
    graf4 = fig4.to_html(full_html=False)
    munis = {}
    for value in covidmuni['Município']:
        pop = covidmuni[covidmuni['Município'] == value]['pop'].max()
        casos = covidmuni[covidmuni['Município'] == value]['Total de Casos'].max()
        inc = int(casos / (pop - casos) * 100000)
        inc = int("{:.0f}".format(inc))
        inc = ("{:,}".format(inc)).replace(',', '.')
        if inc == inf:
            inc = 0
        if inc == 'nan':
            inc = 0
        munis[value] = inc
    info4 = ['{} <span>{}</span> <br> <br>'.format(key, value) for key, value in munis.items()]
    info4 = ''.join(str(e) for e in info4)
    info4 = Markup(f'<p id="df4" style="display: none">Incidência de casos a cada 100 mil habitantes no '
                   f'período: <br> <br><span>{info4}</span></p>')

    return render_template('municipios.html', form=form, min=mini, max=maxi,
                           graf1_covidmuni=graf1, graf2_covidmuni=graf2, graf3_covidmuni=graf3, graf4_covidmuni=graf4,
                           painel1_covidmuni=casost, painel2_covidmuni=obitost, painel3_covidmuni=casosult,
                           painel4_covidmuni=obitosult,
                           info1_covidmuni=info1, info2_covidmuni=info2, info3_covidmuni=info3, info4_covidmuni=info4)


@app.route("/municipios/vacina", methods=['GET'])
def vacina_main():
    random.shuffle(palette)
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    covidsp = pd.read_csv(url1, usecols=['Data'])
    covidsp['Data'] = pd.to_datetime(covidsp['Data'])
    lastupdate = covidsp['Data'].max().strftime("%d/%m/%Y")
    vacina = pd.read_csv(url4,
                         dtype={'Município': 'category', '1ª Dose': 'int32', '2ª Dose': 'int32', '3ª Dose': 'int32',
                                'Dose Única': 'int32', 'Doses Distribuídas': 'int32'})
    flash(Markup(f'<h1 class="vacinometro">Totalização da campanha vacinal por Município '
                 f'<span>(última atualização: {lastupdate})</span></h1>'))

    # Filtro só para 'main' functions:
    vacina = vacina.query(
        "Município == 'São José dos Campos' | Município == 'Taubaté' | Município == 'Jacareí' | Município == "
        "'Lorena' | Município == 'Pindamonhangaba' | Município == 'Caraguatatuba' | Município == "
        "'Guaratinguetá' | Município == 'Caçapava' | Município == 'Ubatuba' | Município == 'São Sebastião'")
    flash(Markup(f'<h1 class="cidades"> Dados das dez maiores cidades do Vale do Paraíba. Para acessar outras cidades, '
                 f'faça uma pesquisa personalizada.</h1>'))

    vact = vacina['1ª Dose'].sum() + vacina['2ª Dose'].sum() + vacina['3ª Dose'].sum() + vacina['Dose Única'].sum()
    vact = "{:,}".format(vact).replace(',', '.')
    vacdf = painel_filter(pops, city_request)
    pop = vacdf['pop'].sum()
    vac2 = vacina['2ª Dose'].sum() + vacina['Dose Única'].sum()
    popvac2 = (vac2 * 100) / pop
    popvac2 = "{:.2f}".format(popvac2).replace('.', ',') + '%'
    vac3 = vacina['3ª Dose'].sum()
    popvac3 = (vac3 * 100) / pop
    popvac3 = "{:.2f}".format(popvac3).replace('.', ',') + '%'
    distr = vacina['Doses Distribuídas'].sum()
    distr = "{:,}".format(distr).replace(',', '.')

    # Comparação entre municípios de aplicação das doses
    fig1 = px.histogram(vacina, x='Município', y=['1ª Dose', '2ª Dose', '3ª Dose', 'Dose Única'], barmode='group',
                        template='xgridoff', title='<b>Aplicação das doses por Município</b>',
                        color_discrete_sequence=palette)
    fig1.update_layout(legend_title_text='Dose Aplicada')
    fig1.update_yaxes(showgrid=False, tickmode="linear", tick0=0, dtick=1000000),
    fig1.update_xaxes(tickangle=-45),
    fig1.update_layout(autosize=True, height=700, margin=dict(t=85, b=185, l=70, r=50),
                       xaxis_title='', yaxis_title="Doses Aplicadas",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"))
    graf1 = fig1.to_html(full_html=False)

    # Comparação entre municípios de doses distribuídas
    fig2 = px.histogram(vacina, x='Doses Distribuídas', y='Município', orientation='h', template='xgridoff',
                        color_discrete_sequence=palette, title='<b>Doses distribuídas por Município</b>')
    fig2.update_xaxes(showgrid=False, tickmode="linear", tick0=0, dtick=2500000),
    fig2.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=185, r=0),
                       xaxis_title='Doses Distribuídas', yaxis_title="",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"))
    graf2 = fig2.to_html(full_html=False)
    munis = {}
    for value in vacina['Município']:
        vac1 = vacina[vacina['Município'] == value]['1ª Dose'].max()
        vac2 = vacina[vacina['Município'] == value]['2ª Dose'].max()
        vac3 = vacina[vacina['Município'] == value]['3ª Dose'].max()
        vac4 = vacina[vacina['Município'] == value]['Dose Única'].max()
        vac = vac1 + vac2 + vac3 + vac4
        dist = vacina[vacina['Município'] == value]['Doses Distribuídas'].max()
        distvac = (vac * 100) / dist
        distvac = "{:.2f}".format(distvac).replace('.', ',')
        if distvac == inf:
            distvac = 0
        if distvac == 'nan':
            distvac = 0
        munis[value] = distvac
    info2 = ['{} <span>{}%</span> <br> <br>'.format(key, value) for key, value in munis.items()]
    info2 = ''.join(str(e) for e in info2)
    info2 = Markup(f'<p id="df6" style="display: none">Eficácia na aplicação de doses distribuídas: <br> <br>'
                   f'<span>{info2}</span></p>')

    return render_template('municipios.html', form=form, min=mini, max=maxi,
                           graf1_vacina=graf1, graf2_vacina=graf2, painel1_vacina=vact, painel2_vacina=popvac2,
                           painel3_vacina=popvac3, painel4_vacina=distr,
                           info2_vacina=info2)


@app.route("/municipios/isolamento-social", methods=['GET'])
def isolamuni_main():
    random.shuffle(palette)
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    isola = pd.read_csv(url7,
                        dtype={'Município': 'category', 'codigo_ibge': 'category', 'Índice de Isolamento (%)': 'int8',
                               'Dia da Semana': 'category'})
    isola['Data'] = pd.to_datetime(isola['Data'])
    # Filtragem padrão para o main:
    isola = isola.query(
        "Município == 'São José dos Campos' | Município == 'Taubaté' | Município == 'Jacareí' | Município == "
        "'Lorena' | Município == 'Pindamonhangaba' | Município == 'Caraguatatuba' | Município == "
        "'Guaratinguetá' | Município == 'Caçapava' | Município == 'Ubatuba' | Município == 'São Sebastião'")
    final = (isola['Data'].max() + dt.timedelta(days=1)).strftime('%Y-%m-%d')
    inicial = (isola['Data'].max() - dt.timedelta(days=15)).strftime("%Y-%m-%d")
    filterdate = (isola['Data'] > inicial) & (isola['Data'] < final)
    isola = isola.loc[filterdate]
    flash_generate(isola)
    flash(Markup(f'<h1 class="cidades"> Dados das dez maiores cidades do Vale do Paraíba. Para acessar outras cidades, '
                 f'faça uma pesquisa personalizada.</h1>'))

    isomed = isola['Índice de Isolamento (%)'].mean()
    isomed = "{:.2f}".format(isomed).replace('.', ',')
    sem = {}
    for value in isola['Dia da Semana']:
        sem[value] = isola[isola['Dia da Semana'] == value]['Índice de Isolamento (%)'].sum()
    semax = max(sem, key=sem.get)
    semin = min(sem, key=sem.get)
    isodeal = isola[isola['Índice de Isolamento (%)'] >= 50].shape[0]

    # Histórico do indice de isolamento nos municipios sp
    fig1 = px.bar(isola, orientation='v', y='Índice de Isolamento (%)', x='Data', color='Município',
                  color_discrete_sequence=palette, title='<b>Índice de Isolamento Social por Município</b>')
    fig1.update_yaxes(showgrid=False, tickmode="linear", tick0=0, dtick=25),
    fig1.update_xaxes(tickangle=-45,
                      tickvals=pd.date_range(isola['Data'].min().strftime('%Y-%m-%d'),
                                             isola['Data'].max().strftime('%Y-%m-%d'), freq='D')),
    fig1.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                       hovermode="x unified", xaxis_title='', yaxis_title="Isolamento Social (%)",
                       plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                       title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                       font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                       xaxis_tickformat='%b %d,<br>%y', xaxis_hoverformat='%b %d, %Y')
    graf1 = fig1.to_html(full_html=False)
    munis = {}
    for value in isola['Município']:
        iso = isola[isola['Município'] == value]['Índice de Isolamento (%)'].mean()
        iso = "{:.2f}".format(iso).replace('.', ',')
        if iso == inf:
            iso = 0
        if iso == 'nan':
            iso = 0
        munis[value] = iso
    info1 = ['{} <span>{}%</span> <br> <br>'.format(key, value) for key, value in munis.items()]
    info1 = ''.join(str(e) for e in info1)
    info1 = Markup(f'<p id="df7" style="display: none">Média do índice de isolamento social no período: '
                   f'<br> <br><span>{info1}</span></p>')

    return render_template('municipios.html', form=form, min=mini, max=maxi, graf1_isola=graf1,
                           painel1_isola=isomed, painel2_isola=semax, painel3_isola=semin, painel4_isola=isodeal,
                           info1_isola=info1)


###################################################################################################################


# ROUTES DE PESQUISA NA PÁGINA DOS MUNICÍPIOS
@app.route("/municipios/covidsp/search", methods=['POST', 'GET'])
def covidmuni_search():
    random.shuffle(palette)
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        if request.form['startdate_field'] != '':
            start_request.append(parse(request.form['startdate_field'], dayfirst=True).strftime('%Y-%m-%d'))
            print(f'O start agora eh {start_request[-1]}')
            form_start.append(request.form['startdate_field'])
        else:
            start_request.append('dumby')
            form_start.append('')
        if request.form['enddate_field'] != '':
            end_request.append(parse(request.form['enddate_field'], dayfirst=True).strftime('%Y-%m-%d'))
            print(f'O end agora eh {end_request[-1]}')
            form_end.append(request.form['enddate_field'])
        else:
            end_request.append('dumby')
            form_end.append('')
        if request.form['municipio_field'] != '':
            city_request.append(str(request.form.get('municipio_field')))
            print(f'As últimas cidades pesquisadas são agora: {city_request[-1]}')
            form_city.append(str(city_request[-1]))
        else:
            city_request.append('dumby')
            form_city.append('')

    covidmuni = pd.read_csv(url2, dtype={'Município': 'category', 'codigo_ibge': 'category',
                                         'Total de Casos': 'int32', 'Novos Casos': 'int16',
                                         'Total de Óbitos': 'int32', 'Novos Óbitos': 'int16',
                                         'Mesorregião': 'category', 'Microrregião': 'category',
                                         'pop': 'int32'})
    covidmuni['Data'] = pd.to_datetime(covidmuni['Data'])
    correct = covidmuni['Data'] < '2021-11-29'
    covidmuni = covidmuni_alt = covidmuni.loc[correct]
    covidmuni_alt['Data'] = pd.to_datetime(covidmuni_alt['Data'])
    covidmuni = date_filter_mun(covidmuni, start_request, end_request)
    try:
        df_len = covidmuni['Data'].nunique()
        print(f'O período da pesquisa é de {df_len} dias.')
        data = painel_date_filter(covidmuni_alt, df_len, start_request, end_request)
        data = painel_filter(data, city_request)
    except TypeError:
        pass

    if not isinstance(covidmuni, pd.DataFrame):
        return covidmuni
    else:
        covidmuni = city_filter_all(covidmuni, city_request)

        if not isinstance(covidmuni, pd.DataFrame):
            return covidmuni
        else:
            casost = covidmuni['Total de Casos'].max()
            casost = ("{:,}".format(casost)).replace(',', '.')
            obitost = covidmuni['Total de Óbitos'].max()
            obitost = ("{:,}".format(obitost)).replace(',', '.')
            try:
                casosult = covidmuni['Novos Casos'].iloc[-1]
                casosult = ("{:,}".format(casosult)).replace(',', '.')
            except IndexError:
                casosult = covidmuni['Novos Casos'].max()
                casosult = ("{:,}".format(casosult)).replace(',', '.')
            try:
                obitosult = covidmuni['Novos Óbitos'].iloc[-1]
                obitosult = ("{:,}".format(obitosult)).replace(',', '.')
            except IndexError:
                obitosult = covidmuni['Novos Óbitos'].max()
                obitosult = ("{:,}".format(obitosult)).replace(',', '.')

            # Casos diários por município
            fig1 = px.bar(covidmuni, x='Data', y='Novos Casos', color='Município',
                          hover_data=['Novos Casos', 'Total de Casos'],
                          color_discrete_sequence=palette,
                          title='<b>Casos confirmados por dia e por Município</b>', template='xgridoff')
            fig1.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)'),
            fig1.update_xaxes(tickangle=-45),
            fig1.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=70, r=50),
                               xaxis_title='', yaxis_title="Novos Casos",
                               plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                               title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                               font=dict(size=18, color='#dc770d', family="Helvetica, neue"), barmode='stack',
                               xaxis_tickformat='%b %d,<br>%y', xaxis_hoverformat='%b %d, %Y')
            graf1 = fig1.to_html(full_html=False)
            munis = {}
            for value in covidmuni['Município']:
                munis[value] = covidmuni[covidmuni['Município'] == value]['Novos Casos'].sum()
                casos7 = data[data['Município'] == value]['Novos Casos'].sum()
                x = (munis[value] * 100) / casos7 - 100
                x = "{:.2f}".format(x).replace('.', ',')
                if x == inf:
                    x = 0
                if len(covidmuni) > int(len(data) * 150 / 100):
                    x = 0
                if x == 'nan':
                    x = 0
                munis[value] = x
            try:
                varinit = data['Data'].min().strftime('%d/%m/%Y')
            except ValueError:
                varinit = covidmuni['Data'].min().strftime('%d/%m/%Y')
            try:
                varend = data['Data'].max().strftime('%d/%m/%Y')
            except ValueError:
                varend = covidmuni['Data'].max().strftime('%d/%m/%Y')
            if varinit == covidmuni['Data'].min().strftime('%d/%m/%Y') and varend == covidmuni['Data'].max().strftime('%d/%m/%Y'):
                info1 = ''
            else:
                info1 = ['{} <span>{}%</span> <br> <br>'.format(key, value) for key, value in munis.items()]
                info1 = ''.join(str(e) for e in info1)
                info1 = Markup(f'<p id="df1" style="display: none">Variação de casos em comparação ao período '
                               f'anterior — {df_len} dia(s) atrás <br> ({varinit}~{varend}): <br> <br>'
                               f'<span>{info1}</span></p>')

            # Óbitos diários por município
            fig2 = px.bar(covidmuni, x='Data', y='Novos Óbitos', color='Município',
                          hover_data=['Novos Casos', 'Total de Casos'],
                          color_discrete_sequence=palette,
                          title='<b>Óbitos confirmados por dia e por Município</b>', template='xgridoff')
            fig2.update_yaxes(showgrid=True, gridcolor='rgba(0, 0, 0, 0.2)', tickmode="linear", tick0=0, dtick=25),
            fig2.update_xaxes(tickangle=-45),
            fig2.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=80, r=50),
                               xaxis_title='', yaxis_title="Novos Óbitos",
                               plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                               title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                               font=dict(size=18, color='#dc770d', family="Helvetica, neue"), barmode='stack',
                               xaxis_tickformat='%b %d,<br>%y', xaxis_hoverformat='%b %d, %Y')
            graf2 = fig2.to_html(full_html=False)
            munis = {}
            for value in covidmuni['Município']:
                munis[value] = covidmuni[covidmuni['Município'] == value]['Novos Óbitos'].sum()
                obi7 = data[data['Município'] == value]['Novos Óbitos'].sum()
                x = (munis[value] * 100) / obi7 - 100
                x = "{:.2f}".format(x).replace('.', ',')
                if x == inf:
                    x = 0
                if len(covidmuni) > int(len(data) * 150 / 100):
                    x = 0
                if x == 'nan':
                    x = 0
                munis[value] = x
            try:
                varinit = data['Data'].min().strftime('%d/%m/%Y')
            except ValueError:
                varinit = covidmuni['Data'].min().strftime('%d/%m/%Y')
            try:
                varend = data['Data'].max().strftime('%d/%m/%Y')
            except ValueError:
                varend = covidmuni['Data'].max().strftime('%d/%m/%Y')
            if varinit == covidmuni['Data'].min().strftime('%d/%m/%Y') and varend == covidmuni['Data'].max().strftime(
                    '%d/%m/%Y'):
                info2 = ''
            else:
                info2 = ['{} <span>{}%</span> <br> <br>'.format(key, value) for key, value in munis.items()]
                info2 = ''.join(str(e) for e in info2)
                info2 = Markup(f'<p id="df2" style="display: none">Variação de óbitos em comparação ao período '
                               f'anterior — {df_len} dia(s) atrás <br> ({varinit}~{varend}): <br> <br>'
                               f'<span>{info2}</span></p>')

            # Filtros apenas para dados totais
            final = (covidmuni['Data'].max() + dt.timedelta(days=1)).strftime('%Y-%m-%d')
            inicial = (covidmuni['Data'].max() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
            filterdate = (covidmuni['Data'] > inicial) & (covidmuni['Data'] < final)
            covidmuni = covidmuni.loc[filterdate]

            # Total de mortes por município
            fig3 = px.pie(covidmuni, values='Total de Óbitos', names='Município', color='Município',
                          title='<b>Comparativo do total de óbitos por Município</b>', template='xgridoff',
                          color_discrete_sequence=palette)
            fig3.update_xaxes(type='date')
            fig3.update_layout(autosize=True)
            fig3.update_yaxes(showgrid=False),
            fig3.update_layout(autosize=True, height=700, margin=dict(t=85, b=45, l=250, r=250),
                               xaxis_tickangle=360,
                               xaxis_title='', yaxis_title="Total de Óbitos",
                               plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                               title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                               font=dict(size=18, color='#dc770d', family="Helvetica, neue"))
            graf3 = fig3.to_html(full_html=False)
            munis = {}
            for value in covidmuni['Município']:
                obtotal = covidmuni[covidmuni['Município'] == value]['Total de Óbitos'].max()
                casostotal = covidmuni[covidmuni['Município'] == value]['Total de Casos'].max()
                if casostotal == 0:
                    munis[value] = 0
                else:
                    let = (obtotal / casostotal) * 100
                    let = "{:.2f}".format(let).replace('.', ',')
                    if let == inf:
                        let = 0
                    if let == 'nan':
                        let = 0
                    munis[value] = let
            info3 = ['{} <span>{}%</span> <br> <br>'.format(key, value) for key, value in munis.items()]
            info3 = ''.join(str(e) for e in info3)
            info3 = Markup(f'<p id="df3" style="display: none">Taxa de letalidade no período: '
                           f'<br> <br><span>{info3}</span></p>')

            # Total de casos por município
            fig4 = px.pie(covidmuni, values='Total de Casos', names='Município', color='Município',
                          title='<b>Comparativo do total de casos por Município</b>', template='xgridoff',
                          color_discrete_sequence=palette)
            fig4.update_xaxes(type='date')
            fig4.update_layout(autosize=True)
            fig4.update_yaxes(showgrid=False),
            fig4.update_layout(autosize=True, height=700, margin=dict(t=85, b=45, l=250, r=250),
                               xaxis_tickangle=360,
                               xaxis_title='', yaxis_title="Total de Casos",
                               plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                               title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                               font=dict(size=18, color='#dc770d', family="Helvetica, neue"))
            graf4 = fig4.to_html(full_html=False)
            munis = {}
            for value in covidmuni['Município']:
                pop = covidmuni[covidmuni['Município'] == value]['pop'].max()
                casos = covidmuni[covidmuni['Município'] == value]['Total de Casos'].max()
                inc = int(casos / (pop - casos) * 100000)
                inc = int("{:.0f}".format(inc))
                inc = ("{:,}".format(inc)).replace(',', '.')
                if inc == inf:
                    inc = 0
                if inc == 'nan':
                    inc = 0
                munis[value] = inc
            info4 = ['{} <span>{}</span> <br> <br>'.format(key, value) for key, value in munis.items()]
            info4 = ''.join(str(e) for e in info4)
            info4 = Markup(f'<p id="df4" style="display: none">Incidência de casos a cada 100 mil habitantes no '
                           f'período: <br> <br><span>{info4}</span></p>')

            return render_template('municipios.html', form=form, min=mini, max=maxi,
                                   start=form_start[-1], end=form_end[-1], city=form_city[-1],
                                   graf1_covidmuni=graf1, graf2_covidmuni=graf2, graf3_covidmuni=graf3,
                                   graf4_covidmuni=graf4, info1_covidmuni=info1, painel1_covidmuni=casost,
                                   painel2_covidmuni=obitost, painel3_covidmuni=casosult, painel4_covidmuni=obitosult,
                                   info2_covidmuni=info2, info3_covidmuni=info3, info4_covidmuni=info4)


@app.route("/municipios/vacina/search", methods=['POST', 'GET'])
def vacina_search():
    random.shuffle(palette)
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    covidsp = pd.read_csv(url1, usecols=['Data'])
    covidsp['Data'] = pd.to_datetime(covidsp['Data'])
    lastupdate = covidsp['Data'].max().strftime("%d/%m/%Y")
    if request.method == 'POST':
        if request.form['startdate_field'] != '':
            start_request.append(parse(request.form['startdate_field'], dayfirst=True).strftime('%Y-%m-%d'))
            print(f'O start agora eh {start_request[-1]}')
            form_start.append(request.form['startdate_field'])
        else:
            start_request.append('dumby')
            form_start.append('')
        if request.form['enddate_field'] != '':
            end_request.append(parse(request.form['enddate_field'], dayfirst=True).strftime('%Y-%m-%d'))
            print(f'O end agora eh {end_request[-1]}')
            form_end.append(request.form['enddate_field'])
        else:
            end_request.append('dumby')
            form_end.append('')
        if request.form['municipio_field'] != '':
            city_request.append(str(request.form.get('municipio_field')))
            print(f'As últimas cidades pesquisadas são agora: {city_request[-1]}')
            form_city.append(str(city_request[-1]))
        else:
            city_request.append('dumby')
            form_city.append('')

    vacina = pd.read_csv(url4,
                         dtype={'Município': 'category', '1ª Dose': 'int32', '2ª Dose': 'int32', '3ª Dose': 'int32',
                                'Dose Única': 'int32', 'Doses Distribuídas': 'int32'})
    flash(Markup(f'<h1 class="vacinometro">Totalização da campanha vacinal por Município '
                 f'<span>(última atualização: {lastupdate})</span></h1>'))
    vacina = city_filter_all(vacina, city_request)

    if not isinstance(vacina, pd.DataFrame):
        return vacina
    else:
        vact = vacina['1ª Dose'].sum() + vacina['2ª Dose'].sum() + vacina['3ª Dose'].sum() + vacina['Dose Única'].sum()
        vact = "{:,}".format(vact).replace(',', '.')
        vacdf = painel_filter(pops, city_request)
        pop = vacdf['pop'].sum()
        vac2 = vacina['2ª Dose'].sum() + vacina['Dose Única'].sum()
        popvac2 = (vac2 * 100) / pop
        popvac2 = "{:.2f}".format(popvac2).replace('.', ',') + '%'
        vac3 = vacina['3ª Dose'].sum()
        popvac3 = (vac3 * 100) / pop
        popvac3 = "{:.2f}".format(popvac3).replace('.', ',') + '%'
        distr = vacina['Doses Distribuídas'].sum()
        distr = "{:,}".format(distr).replace(',', '.')

        # Comparação entre municípios de aplicação das doses
        fig1 = px.histogram(vacina, x='Município', y=['1ª Dose', '2ª Dose', '3ª Dose', 'Dose Única'], barmode='group',
                            template='xgridoff', title='<b>Aplicação das doses por Município</b>',
                            color_discrete_sequence=palette)
        fig1.update_layout(legend_title_text='Dose Aplicada')
        fig1.update_yaxes(showgrid=False, tickmode="linear", tick0=0, dtick=1000000),
        fig1.update_xaxes(tickangle=-45),
        fig1.update_layout(autosize=True, height=700, margin=dict(t=85, b=185, l=70, r=50),
                           xaxis_title='', yaxis_title="Doses Aplicadas",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"))
        graf1 = fig1.to_html(full_html=False)

        # Comparação entre municípios de doses distribuídas
        fig2 = px.histogram(vacina, x='Doses Distribuídas', y='Município', orientation='h', template='xgridoff',
                            color_discrete_sequence=palette, title='<b>Doses distribuídas por Município</b>')
        fig2.update_xaxes(showgrid=False, tickmode="linear", tick0=0, dtick=2500000),
        fig2.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=225, r=30),
                           xaxis_title='Doses Distribuídas', yaxis_title="",
                           plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                           title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                           font=dict(size=18, color='#dc770d', family="Helvetica, neue"))
        graf2 = fig2.to_html(full_html=False)
        munis = {}
        for value in vacina['Município']:
            vac1 = vacina[vacina['Município'] == value]['1ª Dose'].max()
            vac2 = vacina[vacina['Município'] == value]['2ª Dose'].max()
            vac3 = vacina[vacina['Município'] == value]['3ª Dose'].max()
            vac4 = vacina[vacina['Município'] == value]['Dose Única'].max()
            vac = vac1 + vac2 + vac3 + vac4
            dist = vacina[vacina['Município'] == value]['Doses Distribuídas'].max()
            distvac = (vac * 100) / dist
            distvac = "{:.2f}".format(distvac).replace('.', ',')
            if distvac == inf:
                distvac = 0
            if distvac == 'nan':
                distvac = 0
            munis[value] = distvac
        info2 = ['{} <span>{}%</span> <br> <br>'.format(key, value) for key, value in munis.items()]
        info2 = ''.join(str(e) for e in info2)
        info2 = Markup(f'<p id="df6" style="display: none">Eficácia na aplicação de doses distribuídas: <br> <br>'
                       f'<span>{info2}</span></p>')

        return render_template('municipios.html', form=form, min=mini, max=maxi,
                               start=form_start[-1], end=form_end[-1], city=form_city[-1],
                               graf1_vacina=graf1, graf2_vacina=graf2, painel1_vacina=vact, painel2_vacina=popvac2,
                               painel3_vacina=popvac3, painel4_vacina=distr,
                               info2_vacina=info2)


@app.route("/municipios/isolamento-social/search", methods=['POST', 'GET'])
def isolamuni_search():
    random.shuffle(palette)
    form = Form()
    mini = '2020-02-26'
    maxi = datetime.now().strftime('%Y-%m-%d')
    if request.method == 'POST':
        if request.form['startdate_field'] != '':
            start_request.append(parse(request.form['startdate_field'], dayfirst=True).strftime('%Y-%m-%d'))
            print(f'O start agora eh {start_request[-1]}')
            form_start.append(request.form['startdate_field'])
        else:
            start_request.append('dumby')
            form_start.append('')
        if request.form['enddate_field'] != '':
            end_request.append(parse(request.form['enddate_field'], dayfirst=True).strftime('%Y-%m-%d'))
            print(f'O end agora eh {end_request[-1]}')
            form_end.append(request.form['enddate_field'])
        else:
            end_request.append('dumby')
            form_end.append('')
        if request.form['municipio_field'] != '':
            city_request.append(str(request.form.get('municipio_field')))
            print(f'As últimas cidades pesquisadas são agora: {city_request[-1]}')
            form_city.append(str(city_request[-1]))
        else:
            city_request.append('dumby')
            form_city.append('')

    isola = pd.read_csv(url7,
                        dtype={'Município': 'category', 'codigo_ibge': 'category', 'Índice de Isolamento (%)': 'int8',
                               'Dia da Semana': 'category'})
    isola['Data'] = pd.to_datetime(isola['Data'])
    isola = date_filter_mun(isola, start_request, end_request)

    if not isinstance(isola, pd.DataFrame):
        return isola
    else:
        isola = city_filter_all(isola, city_request)

        if not isinstance(isola, pd.DataFrame):
            return isola
        else:
            # Filtragem padrão para o search:
            isola = isola[isola['Município'] != 'Estado De São Paulo']

            isomed = isola['Índice de Isolamento (%)'].mean()
            isomed = "{:.2f}".format(isomed).replace('.', ',')
            sem = {}
            for value in isola['Dia da Semana']:
                sem[value] = isola[isola['Dia da Semana'] == value]['Índice de Isolamento (%)'].sum()
            semax = max(sem, key=sem.get)
            semin = min(sem, key=sem.get)
            isodeal = isola[isola['Índice de Isolamento (%)'] >= 50].shape[0]

            # Histórico do indice de isolamento nos municipios sp
            fig1 = px.bar(isola, orientation='v', y='Índice de Isolamento (%)', x='Data', color='Município',
                          template='xgridoff', title='<b>Índice de Isolamento Social por Município</b>',
                          color_discrete_sequence=palette)
            fig1.update_yaxes(showgrid=False, tickmode="linear", tick0=0, dtick=25),
            fig1.update_xaxes(tickangle=-45),
            fig1.update_layout(autosize=True, height=700, margin=dict(t=85, b=90, l=90, r=50),
                               hovermode="x unified", xaxis_title='', yaxis_title="Isolamento Social (%)",
                               plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                               title_font=dict(size=32, color='#dc770d', family="Helvetica, neue"),
                               font=dict(size=18, color='#dc770d', family="Helvetica, neue"),
                               xaxis_tickformat='%b %d,<br>%y', xaxis_hoverformat='%b %d, %Y')
            graf1 = fig1.to_html(full_html=False)
            munis = {}
            for value in isola['Município']:
                iso = isola[isola['Município'] == value]['Índice de Isolamento (%)'].mean()
                iso = "{:.2f}".format(iso).replace('.', ',')
                if iso == inf:
                    iso = 0
                if iso == 'nan':
                    iso = 0
                munis[value] = iso
            info1 = ['{} <span>{}%</span> <br> <br>'.format(key, value) for key, value in munis.items()]
            info1 = ''.join(str(e) for e in info1)
            info1 = Markup(f'<p id="df7" style="display: none">Média do índice de isolamento social no período: '
                           f'<br> <br><span>{info1}</span></p>')

            return render_template('municipios.html', form=form, min=mini, max=maxi,
                                   start=form_start[-1], end=form_end[-1], city=form_city[-1],
                                   graf1_isola=graf1, painel1_isola=isomed, painel2_isola=semax, painel3_isola=semin,
                                   painel4_isola=isodeal, info1_isola=info1)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, threaded=True, debug=True)
