# Gráficos referentes a /ESTADO/COVIDSP, function MAIN e SEARCH

# Gráfico casos por dia
fig1 = px.bar(covidsp, x='Data', y='Casos por dia', color_discrete_sequence=['#f8ac5b'],
             title='Casos por dia no Estado de São Paulo', hover_data=['Data', 'Total de casos', 'Casos por dia'],
             template='xgridoff')
fig1.update_yaxes(showgrid=False),
fig1.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                   xaxis_tickangle=360,
                   xaxis_title='', yaxis_title="Casos por dia",
                   plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                   title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                   font=dict(size=18, color='#dc770d'), barmode='stack')
graf1 = fig1.to_html(full_html=False)


# Gráfico óbitos diários
fig2 = px.bar(covidsp, x='Data', y='Óbitos por dia', color_discrete_sequence=['#f8ac5b'],
             title='Óbitos por dia no Estado de São Paulo', hover_data=['Data', 'Total de óbitos', 'Óbitos por dia'],
             template='xgridoff')
fig2.update_yaxes(showgrid=False),
fig2.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                   xaxis_tickangle=360,
                   xaxis_title='', yaxis_title="Óbitos por dia",
                   plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                   title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                   font=dict(size=18, color='#dc770d'), barmode='stack')
graf2 = fig2.to_html(full_html=False)


# Gráfico total de casos
fig3 = px.line(covidsp.sort_values(by=['Data'], ascending=[True]), x='Data', y='Total de casos', line_shape='linear', template='xgridoff', 
               color_discrete_sequence=['#ac5a00'], title='Crescimento do nº de casos no Estado',   
               hover_data=['Data', 'Total de casos', 'Casos por dia'], line_dash_sequence=['solid'], 
               render_mode='auto')
fig3.update_yaxes(showgrid=False),
fig3.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50), 
                   xaxis_tickangle=360,
                   xaxis_title='', yaxis_title="Total de casos",
                   plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                   title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                   font=dict(size=18, color='#dc770d'))
graf3 = fig3.to_html(full_html=False)


# Gráfico total de óbitos 
fig4 = px.line(covidsp.sort_values(by=['Data'], ascending=[True]), x='Data', y='Total de óbitos', 
               line_shape='linear', template='xgridoff', color_discrete_sequence=['#ac5a00'], line_dash_sequence=['solid'], 
               render_mode='auto', hover_data=['Data', 'Total de óbitos', 'Óbitos por dia'], 
               title='Crescimento do nº de óbitos no Estado')
fig4.update_yaxes(showgrid=False),
fig4.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50), 
                   xaxis_tickangle=360,
                   xaxis_title='', yaxis_title="Total de óbitos",
                   plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                   title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                   font=dict(size=18, color='#dc770d'))
graf4 = fig4.to_html(full_html=False)



----------------------------------------------------------------------------------------------------------------------

# Gráficos referentes a /MUNICIPIOS/COVIDSP, function MAIN

# Filtragem padrão dos dataframes com município em 'main' functions:
final = (covidmuni['Data'].max() + dt.timedelta(days=1)).strftime('%Y-%m-%d')
inicial = (covidmuni['Data'].max() - dt.timedelta(days=16)).strftime("%Y-%m-%d")
filterdate = (covidmuni['Data'] > inicial) & (covidmuni['Data'] < final)
covidmuni = covidmuni.loc[filterdate]
covidmuni = covidmuni.query("Município == 'São Paulo' | Município == 'São José dos Campos' | Município == 'Caçapava' | Município == 'Jacareí' | Município == 'Campinas' | Município == 'São José do Rio Preto' | Município == 'Ribeirão Preto' | Município == 'Sorocaba' | Município == 'São Bernardo do Campo' | Município == 'Santo André'")


# Casos diários por município
fig1 = px.bar(covidmuni, x='Data', y='Novos Casos', color='Município', hover_data=['Novos Casos'], 
              color_discrete_sequence=['#f8ac5b', '#faad54', '#fbae4d', '#fdaf45', '#feb03d', '#ffb134', '#ffb329', '#ffb41a', 
                                       '#ffb600', '#ac5a00', '#b76300', '#c16c00', '#cc7601', '#d67f01', '#e18900', '#eb9300', 
                                       '#f59e00', '#ffa800'],
                   title='Casos confirmados por dia e por Município', template='xgridoff')
fig1.update_yaxes(showgrid=False),
fig1.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                   xaxis_tickangle=360,
                   xaxis_title='', yaxis_title="Novos Casos",
                   plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                   title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                   font=dict(size=18, color='#dc770d'), barmode='stack')
graf1 = fig1.to_html(full_html=False)


# Óbitos diários por município
fig2 = px.bar(covidmuni, x='Data', y='Novos Óbitos', color='Município', hover_data=['Novos Óbitos'], 
              color_discrete_sequence=['#f8ac5b', '#faad54', '#fbae4d', '#fdaf45', '#feb03d', '#ffb134', '#ffb329', '#ffb41a', 
                                       '#ffb600', '#ac5a00', '#b76300', '#c16c00', '#cc7601', '#d67f01', '#e18900', '#eb9300', 
                                       '#f59e00', '#ffa800'],
              title='Óbitos confirmados por dia e por Município', template='xgridoff')
fig2.update_yaxes(showgrid=False),
fig2.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                   xaxis_tickangle=360,
                   xaxis_title='', yaxis_title="Novos Óbitos",
                   plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                   title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                   font=dict(size=18, color='#dc770d'), barmode='stack')
graf2 = fig2.to_html(full_html=False)


# Filtros apenas para dados totais
final = (covidmuni['Data'].max() + dt.timedelta(days=1)).strftime('%Y-%m-%d')
inicial = (covidmuni['Data'].max() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
filterdate = (covidmuni['Data'] > inicial) & (covidmuni['Data'] < final)
covidmuni = covidmuni.loc[filterdate]
covidmuni = covidmuni.query("Município == 'São Paulo' | Município == 'São José dos Campos' | Município == 'Caçapava' | Município == 'Jacareí' | Município == 'Campinas' | Município == 'São José do Rio Preto' | Município == 'Ribeirão Preto' | Município == 'Sorocaba' | Município == 'São Bernardo do Campo' | Município == 'Santo André'")


# Total de mortes por município
fig3 = px.pie(covidmuni, values='Total de Óbitos', names='Município', color='Município', title='Comparativo entre o total de óbitos por Município', template='xgridoff', 
              color_discrete_sequence=['#f8ac5b', '#faad54', '#fbae4d', '#fdaf45', '#feb03d', '#ffb134', '#ffb329', '#ffb41a', 
                                       '#ffb600', '#ac5a00', '#b76300', '#c16c00', '#cc7601', '#d67f01', '#e18900', '#eb9300', 
                                       '#f59e00', '#ffa800'])
fig3.update_xaxes(type='date')
fig3.update_layout(autosize=True)
fig3.update_yaxes(showgrid=False),
fig3.update_layout(margin=dict(t=80, b=40, l=85, r=50), 
                   xaxis_tickangle=360,
                   xaxis_title='', yaxis_title="Total de Óbitos",
                   plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                   title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                   font=dict(size=18, color='#dc770d'))
graf3 = fig3.to_html(full_html=False)


# Total de casos por município
fig4 = px.pie(covidmuni, values='Total de Casos', names='Município', color='Município', title='Comparativo entre o total de casos por Município', template='xgridoff', 
              color_discrete_sequence=['#f8ac5b', '#faad54', '#fbae4d', '#fdaf45', '#feb03d', '#ffb134', '#ffb329', '#ffb41a', 
                                       '#ffb600', '#ac5a00', '#b76300', '#c16c00', '#cc7601', '#d67f01', '#e18900', '#eb9300', 
                                       '#f59e00', '#ffa800'])
fig4.update_xaxes(type='date')
fig4.update_layout(autosize=True)
fig4.update_yaxes(showgrid=False),
fig4.update_layout(margin=dict(t=80, b=40, l=85, r=50), 
                   xaxis_tickangle=360,
                   xaxis_title='', yaxis_title="Total de Casos",
                   plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                   title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                   font=dict(size=18, color='#dc770d'))
graf4 = fig4.to_html(full_html=False)


-------------------------------------------------------------------------------------------------------


# Gráficos referentes a /MUNICIPIOS/COVIDSP, function SEARCH


# Casos diários por município
fig1 = px.bar(covidmuni, x='Data', y='Novos Casos', color='Município', hover_data=['Novos Casos', 'Total de Casos'], 
              color_discrete_sequence=['#f8ac5b', '#faad54', '#fbae4d', '#fdaf45', '#feb03d', '#ffb134', '#ffb329', '#ffb41a', 
                                       '#ffb600', '#ac5a00', '#b76300', '#c16c00', '#cc7601', '#d67f01', '#e18900', '#eb9300', 
                                       '#f59e00', '#ffa800'],
              title='Casos confirmados por dia e por Município', template='xgridoff')
fig1.update_yaxes(showgrid=False),
fig1.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                   xaxis_tickangle=360,
                   xaxis_title='', yaxis_title="Novos Casos",
                   plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                   title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                   font=dict(size=18, color='#dc770d'), barmode='stack')
graf1 = fig1.to_html(full_html=False)


# Óbitos diários por município
fig2 = px.bar(covidmuni, x='Data', y='Novos Óbitos', color='Município', hover_data=['Novos Casos', 'Total de Casos'], 
              color_discrete_sequence=['#f8ac5b', '#faad54', '#fbae4d', '#fdaf45', '#feb03d', '#ffb134', '#ffb329', '#ffb41a', 
                                       '#ffb600', '#ac5a00', '#b76300', '#c16c00', '#cc7601', '#d67f01', '#e18900', '#eb9300', 
                                       '#f59e00', '#ffa800'],
              title='Óbitos confirmados por dia e por Município', template='xgridoff')
fig2.update_yaxes(showgrid=False),
fig2.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                   xaxis_tickangle=360,
                   xaxis_title='', yaxis_title="Novos Óbitos",
                   plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                   title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                   font=dict(size=18, color='#dc770d'), barmode='stack')
graf2 = fig2.to_html(full_html=False)


# Filtros apenas para dados totais
final = (covidmuni['Data'].max() + dt.timedelta(days=1)).strftime('%Y-%m-%d')
inicial = (covidmuni['Data'].max() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
filterdate = (covidmuni['Data'] > inicial) & (covidmuni['Data'] < final)
covidmuni = covidmuni.loc[filterdate]


# Total de mortes por município
fig3 = px.pie(covidmuni, values='Total de Óbitos', names='Município', color='Município', title='Comparativo do total de óbitos por Município', template='xgridoff', 
              color_discrete_sequence=['#f8ac5b', '#faad54', '#fbae4d', '#fdaf45', '#feb03d', '#ffb134', '#ffb329', '#ffb41a', 
                                       '#ffb600', '#ac5a00', '#b76300', '#c16c00', '#cc7601', '#d67f01', '#e18900', '#eb9300', 
                                       '#f59e00', '#ffa800'])
fig3.update_xaxes(type='date')
fig3.update_yaxes(showgrid=False),
fig3.update_layout(autosize=True)
fig3.update_layout(margin=dict(t=80, b=40, l=85, r=50), 
                   xaxis_tickangle=360,
                   xaxis_title='Data', yaxis_title="Total de Óbitos",
                   plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                   title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                   font=dict(size=18, color='#dc770d'))
graf3 = fig3.to_html(full_html=False)



# Total de casos por município
fig4 = px.pie(covidmuni, values='Total de Casos', names='Município', color='Município', title='Comparativo do total de casos por Município', template='xgridoff', 
              color_discrete_sequence=['#f8ac5b', '#faad54', '#fbae4d', '#fdaf45', '#feb03d', '#ffb134', '#ffb329', '#ffb41a', 
                                       '#ffb600', '#ac5a00', '#b76300', '#c16c00', '#cc7601', '#d67f01', '#e18900', '#eb9300', 
                                       '#f59e00', '#ffa800'])
fig4.update_xaxes(type='date')
fig4.update_layout(autosize=True)
fig4.update_yaxes(showgrid=False),
fig4.update_layout(margin=dict(t=80, b=40, l=85, r=50),
                   xaxis_tickangle=360,
                   xaxis_title='Data', yaxis_title="Total de Casos",
                   plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                   title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                   font=dict(size=18, color='#dc770d'))
graf4 = fig4.to_html(full_html=False)


-----------------------------------------------------------------------------------------

# Gráficos referentes a /MUNICIPIOS/VACINA, function MAIN

# Filtro só para 'main' functions:
vacina = vacina.query("Município == 'São Paulo' | Município == 'Guarulhos' | Município == 'Caçapava' | Município == 'Jacareí' | Município == 'Campinas' | Município == 'São Bernardo Do Campo' | Município == 'Osasco' | Município == 'Santo André' | Município == 'São José Dos Campos' | Município == 'Sorocaba'")


# Comparação entre municípios de aplicação das doses
fig1 = px.histogram(vacina, x='Município', y=['1ª Dose', '2ª Dose', '3ª Dose', 'Dose Única'], barmode='group', template='xgridoff', 
                    color_discrete_sequence=['#f8ac5b', '#faad54', '#fbae4d', '#fdaf45', '#feb03d', '#ffb134', '#ffb329', '#ffb41a', 
                                             '#ffb600', '#ac5a00', '#b76300', '#c16c00', '#cc7601', '#d67f01', '#e18900', '#eb9300', 
                                             '#f59e00', '#ffa800'])
fig1.update_layout(legend_title_text='Dose Aplicada')
fig1.update_yaxes(showgrid=False),
fig1.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50), 
                   xaxis_tickangle=360,
                   xaxis_title='Município', yaxis_title="Doses Aplicadas",
                   plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                   title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                   font=dict(size=18, color='#dc770d'))
graf1 = fig1.to_html(full_html=False)


# Comparação entre municípios de doses distribuídas
fig2 = px.histogram(vacina, x='Doses Distribuídas', y='Município', orientation='h', template='xgridoff', 
                    color_discrete_sequence=['#f8ac5b', '#faad54', '#fbae4d', '#fdaf45', '#feb03d', '#ffb134', '#ffb329', '#ffb41a', 
                                             '#ffb600', '#ac5a00', '#b76300', '#c16c00', '#cc7601', '#d67f01', '#e18900', '#eb9300', 
                                             '#f59e00', '#ffa800'])
fig2.update_yaxes(showgrid=False),
fig2.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                   xaxis_tickangle=360,
                   xaxis_title='Doses Distribuídas', yaxis_title="Município",
                   plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                   title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                   font=dict(size=18, color='#dc770d'))
graf2 = fig2.to_html(full_html=False)


---------------------------------------------------------------------


# Gráficos referentes a /MUNICIPIOS/VACINA, function SEARCH

# Comparação entre municípios de aplicação das doses
fig1 = px.histogram(vacina, x='Município', y=['1ª Dose', '2ª Dose', '3ª Dose', 'Dose Única'], barmode='group', template='xgridoff', 
                    color_discrete_sequence=['#f8ac5b', '#faad54', '#fbae4d', '#fdaf45', '#feb03d', '#ffb134', '#ffb329', '#ffb41a', 
                                             '#ffb600', '#ac5a00', '#b76300', '#c16c00', '#cc7601', '#d67f01', '#e18900', '#eb9300', 
                                             '#f59e00', '#ffa800'])
fig1.update_layout(legend_title_text='Dose Aplicada')
fig1.update_yaxes(showgrid=False),
fig1.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                   xaxis_tickangle=360,
                   xaxis_title='Município', yaxis_title="Doses Aplicadas",
                   plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                   title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                   font=dict(size=18, color='#dc770d'))
graf1 = fig1.to_html(full_html=False)


# Comparação entre municípios de doses distribuídas
fig2 = px.histogram(vacina, x='Doses Distribuídas', y='Município', orientation='h', template='xgridoff', 
                    color_discrete_sequence=['#f8ac5b', '#faad54', '#fbae4d', '#fdaf45', '#feb03d', '#ffb134', '#ffb329', '#ffb41a', 
                                             '#ffb600', '#ac5a00', '#b76300', '#c16c00', '#cc7601', '#d67f01', '#e18900', '#eb9300', 
                                             '#f59e00', '#ffa800'])
fig2.update_yaxes(showgrid=False),
fig2.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                   xaxis_tickangle=360,
                   xaxis_title='Doses Distribuídas', yaxis_title="Município",
                   plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                   title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                   font=dict(size=18, color='#dc770d'))
graf2 = fig2.to_html(full_html=False)


-----------------------------------------------------------------------------------------------------


# Gráficos referentes a /ESTADO/VACINA, function MAIN e SEARCH


# Evolução 1ª dose
fig1 = px.bar(evoludose, x='Data', y='1ª Dose', template='xgridoff', 
              color_discrete_sequence=['#f8ac5b', '#faad54', '#fbae4d', '#fdaf45', '#feb03d', '#ffb134', '#ffb329', '#ffb41a', 
                                       '#ffb600', '#ac5a00', '#b76300', '#c16c00', '#cc7601', '#d67f01', '#e18900', '#eb9300', 
                                       '#f59e00', '#ffa800'])
fig1.update_yaxes(showgrid=False),
fig1.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50), 
                   xaxis_tickangle=360,
                   xaxis_title='', yaxis_title="Primeira Dose",
                   plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                   title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                   font=dict(size=18, color='#dc770d'))
graf1 = fig1.to_html(full_html=False)


# Evolução 2ª dose
fig2 = px.bar(evoludose, x='Data', y='2ª Dose', template='xgridoff', 
              color_discrete_sequence=['#f8ac5b', '#faad54', '#fbae4d', '#fdaf45', '#feb03d', '#ffb134', '#ffb329', '#ffb41a', 
                                       '#ffb600', '#ac5a00', '#b76300', '#c16c00', '#cc7601', '#d67f01', '#e18900', '#eb9300', 
                                       '#f59e00', '#ffa800'])
fig2.update_yaxes(showgrid=False),
fig2.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                   xaxis_tickangle=360,
                   xaxis_title='', yaxis_title="Segunda Dose",
                   plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                   title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                   font=dict(size=18, color='#dc770d'))
graf2 = fig2.to_html(full_html=False)


# Evolução 3ª dose
fig3 = px.bar(evoludose, x='Data', y='3ª Dose', template='xgridoff', 
              color_discrete_sequence=['#f8ac5b', '#faad54', '#fbae4d', '#fdaf45', '#feb03d', '#ffb134', '#ffb329', '#ffb41a', 
                                       '#ffb600', '#ac5a00', '#b76300', '#c16c00', '#cc7601', '#d67f01', '#e18900', '#eb9300', 
                                       '#f59e00', '#ffa800'])
fig3.update_yaxes(showgrid=False),
fig3.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50), 
                   xaxis_tickangle=360,
                   xaxis_title='', yaxis_title="Terceira Dose",
                   plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                   title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                   font=dict(size=18, color='#dc770d'))
graf3 = fig3.to_html(full_html=False)


# Evolução dose única
fig4 = px.bar(evoludose, x='Data', y='Dose Única', template='xgridoff', 
              color_discrete_sequence=['#f8ac5b', '#faad54', '#fbae4d', '#fdaf45', '#feb03d', '#ffb134', '#ffb329', '#ffb41a', 
                                       '#ffb600', '#ac5a00', '#b76300', '#c16c00', '#cc7601', '#d67f01', '#e18900', '#eb9300', 
                                       '#f59e00', '#ffa800'])
fig4.update_yaxes(showgrid=False),
fig4.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50), 
                   xaxis_tickangle=360,
                   xaxis_title='Data', yaxis_title="Dose Única",
                   plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                   title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                   font=dict(size=18, color='#dc770d'))
graf4 = fig4.to_html(full_html=False)


# Filtros apenas para dados totais
final = (evoludose['Data'].max() + dt.timedelta(days=1)).strftime('%Y-%m-%d')
inicial = (evoludose['Data'].max() - dt.timedelta(days=1)).strftime("%Y-%m-%d")
filterdate = (evoludose['Data'] > inicial) & (evoludose['Data'] < final)
evoludose = evoludose.loc[filterdate]

# Comparativo entre doses
fig5 = px.bar(evoludose, x='Data', y=['1ª Dose', '2ª Dose', '3ª Dose', 'Dose Única'], barmode='group', template='xgridoff', 
              color_discrete_sequence=['#f8ac5b', '#faad54', '#fbae4d', '#fdaf45', '#feb03d', '#ffb134', '#ffb329', '#ffb41a', 
                                       '#ffb600', '#ac5a00', '#b76300', '#c16c00', '#cc7601', '#d67f01', '#e18900', '#eb9300', 
                                       '#f59e00', '#ffa800'])
fig5.update_yaxes(showgrid=False),
fig5.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                   xaxis_tickangle=360,
                   xaxis_title='', yaxis_title="Doses Aplicadas",
                   plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                   title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                   font=dict(size=18, color='#dc770d'))
graf5 = fig5.to_html(full_html=False)


-----------------------------------------------------------------------------------------------------------

# Gráficos referentes a /ESTADO/LEITOS, function MAIN e SEARCH

# Filtro para só aparecer os dados referentes ao Estado de SP como um todo
leitos = leitos[leitos['Departamento Regional de Saúde'] == 'Estado de São Paulo']

# Ocupação dos leitos de UTI e enfermaria no Estado
fig1 = px.bar(leitos, x='Data', y='Ocupação dos leitos de UTI e Enfermaria (%)', template='xgridoff', 
              color_discrete_sequence=['#f8ac5b', '#faad54', '#fbae4d', '#fdaf45', '#feb03d', '#ffb134', '#ffb329', '#ffb41a', 
                                       '#ffb600', '#ac5a00', '#b76300', '#c16c00', '#cc7601', '#d67f01', '#e18900', '#eb9300', 
                                       '#f59e00', '#ffa800'])
fig1.update_yaxes(showgrid=False),
fig1.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50), 
                   xaxis_tickangle=360,
                   xaxis_title='', yaxis_title="Ocupação dos leitos",
                   plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                   title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                   font=dict(size=18, color='#dc770d'))
graf1 = fig1.to_html(full_html=False)


# Número de leitos de UTI e enfermaria no Estado
fig2 = px.bar(leitos, x='Data', y=['Total de leitos de UTI destinados à Covid', 'Total de leitos de Enfermaria destinados à Covid'], template='xgridoff', 
              color_discrete_sequence=['#f8ac5b', '#faad54', '#fbae4d', '#fdaf45', '#feb03d', '#ffb134', '#ffb329', '#ffb41a', 
                                       '#ffb600', '#ac5a00', '#b76300', '#c16c00', '#cc7601', '#d67f01', '#e18900', '#eb9300', 
                                       '#f59e00', '#ffa800'])
fig2.update_yaxes(showgrid=False),
fig2.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50), 
                   xaxis_tickangle=360,
                   xaxis_title='', yaxis_title="Leitos destinados à COVID-19",
                   plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                   title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                   font=dict(size=18, color='#dc770d'), barmode='group')
graf2 = fig2.to_html(full_html=False)


# Número de pacientes em tratamento na UTI e enfermaria no Estado
fig3 = px.bar(leitos, x='Data', y=['Pacientes em tratamento na UTI', 'Pacientes em tratamento na Enfermaria'], template='xgridoff', 
              color_discrete_sequence=['#f8ac5b', '#faad54', '#fbae4d', '#fdaf45', '#feb03d', '#ffb134', '#ffb329', '#ffb41a', 
                                       '#ffb600', '#ac5a00', '#b76300', '#c16c00', '#cc7601', '#d67f01', '#e18900', '#eb9300', 
                                       '#f59e00', '#ffa800'])
fig3.update_yaxes(showgrid=False),
fig3.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                   xaxis_tickangle=360,
                   xaxis_title='', yaxis_title="Pacientes em tratamento",
                   plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                   title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                   font=dict(size=18, color='#dc770d'), barmode='group')
graf3 = fig3.to_html(full_html=False)


# Novas internações por dia no Estado
fig4 = px.line(leitos.sort_values(by=['Data'], ascending=[True]), x='Data', y='Novos casos de internações (UTI e Enfermaria)', template='xgridoff', 
               color_discrete_sequence=['#f8ac5b', '#faad54', '#fbae4d', '#fdaf45', '#feb03d', '#ffb134', '#ffb329', '#ffb41a', 
                                        '#ffb600', '#ac5a00', '#b76300', '#c16c00', '#cc7601', '#d67f01', '#e18900', '#eb9300', 
                                        '#f59e00', '#ffa800'])
fig4.update_yaxes(showgrid=False),
fig4.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                   xaxis_tickangle=360,
                   xaxis_title='', yaxis_title="Internações (UTI e Enfermaria)",
                   plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                   title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                   font=dict(size=18, color='#dc770d'))
graf4 = fig4.to_html(full_html=False)


---------------------------------------------------------------------------------------------------


# Gráficos referentes a /ESTADO/ISOLA, function MAIN


# Filtragem padrão para o main:
isola = isola[isola['Município'] == 'Estado De São Paulo']
final = (isola['Data'].max() + dt.timedelta(days=1)).strftime('%Y-%m-%d')
inicial = (isola['Data'].max() - dt.timedelta(days=16)).strftime("%Y-%m-%d")
filterdate = (isola['Data'] > inicial) & (isola['Data'] < final)
isola = isola.loc[filterdate]


# Histórico do indice de isolamento no estado de SP
fig1 = px.bar(isola, orientation='v', y='Índice de Isolamento (%)', x='Data', color='Dia da Semana', template='xgridoff', 
              color_discrete_sequence=['#f8ac5b', '#faad54', '#fbae4d'])
fig1.update_yaxes(showgrid=False),
fig1.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                   xaxis_tickangle=360,
                   xaxis_title='', yaxis_title="Isolamento Social (%)",
                   plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                   title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                   font=dict(size=18, color='#dc770d'))
graf1 = fig1.to_html(full_html=False)


-----------------------------------------------------------------------------------------


# Gráficos referentes a /ESTADO/ISOLA, function SEARCH


# Filtragem padrão para o search:
isola = isola[isola['Município'] == 'Estado De São Paulo']


# Histórico do indice de isolamento no estado de SP
fig1 = px.bar(isola, orientation='v', y='Índice de Isolamento (%)', x='Data', color='Dia da Semana', template='xgridoff', 
              color_discrete_sequence=['#f8ac5b', '#faad54', '#fbae4d'])
fig1.update_yaxes(showgrid=False),
fig1.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50),
                   xaxis_tickangle=360,
                   xaxis_title='', yaxis_title="Isolamento Social (%)",
                   plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                   title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                   font=dict(size=18, color='#dc770d'))
graf1 = fig1.to_html(full_html=False)


-------------------------------------------------------------------------------------


# Gráficos referentes a /MUNICIPIOS/ISOLA, function MAIN


# Filtragem padrão para o main:
isola = isola.query("Município == 'São Paulo' | Município == 'São José Dos Campos' | Município == 'Caçapava' | Município == 'Jacareí' | Município == 'Campinas' | Município == 'São José Do Rio Preto' | Município == 'Ribeirão Preto' | Município == 'Sorocaba' | Município == 'São Bernardo Do Campo' | Município == 'Santo André'")
final = (isola['Data'].max() + dt.timedelta(days=1)).strftime('%Y-%m-%d')
inicial = (isola['Data'].max() - dt.timedelta(days=16)).strftime("%Y-%m-%d")
filterdate = (isola['Data'] > inicial) & (isola['Data'] < final)
isola = isola.loc[filterdate]


# Histórico do indice de isolamento nos municipios sp
fig1 = px.bar(isola, orientation='v', y='Índice de Isolamento (%)', x='Data', color='Município', 
              color_discrete_sequence=['#f8ac5b', '#faad54', '#fbae4d', '#fdaf45', '#feb03d', '#ffb134', '#ffb329', '#ffb41a', 
                                       '#ffb600', '#ac5a00', '#b76300', '#c16c00', '#cc7601', '#d67f01', '#e18900', '#eb9300', 
                                       '#f59e00', '#ffa800'])
fig1.update_yaxes(showgrid=False),
fig1.update_traces(hovertemplate=None,)
fig1.update_layout(autosize=True, margin=dict(t=70, b=0, l=70, r=40),
                   hovermode="x unified", 
                   xaxis_tickangle=360,
                   xaxis_title='Data', yaxis_title="Isolamento Social (%)",
                   plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                   title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                   font=dict(size=18, color='#dc770d'), barmode='stack')
graf1 = fig1.to_html(full_html=False)


-----------------------------------------------------------------------------------------

# Gráficos referentes a /MUNICIPIOS/ISOLA, function SEARCH


# Histórico do indice de isolamento nos municipios sp
fig1 = px.bar(isola, orientation='v', y='Índice de Isolamento (%)', x='Data', color='Município', template='xgridoff', 
              color_discrete_sequence=['#f8ac5b', '#faad54', '#fbae4d', '#fdaf45', '#feb03d', '#ffb134', '#ffb329', '#ffb41a', 
                                       '#ffb600', '#ac5a00', '#b76300', '#c16c00', '#cc7601', '#d67f01', '#e18900', '#eb9300', 
                                       '#f59e00', '#ffa800'])
fig1.update_yaxes(showgrid=False),
fig1.update_layout(autosize=True, margin=dict(t=80, b=40, l=85, r=50), 
                   xaxis_tickangle=360,
                   xaxis_title='', yaxis_title="Isolamento Social (%)",
                   plot_bgcolor='#ffffff', paper_bgcolor='#ffffff',
                   title_font=dict(size=32, color='#dc770d', family="Lato, sans-serif"),
                   font=dict(size=18, color='#dc770d'))
graf1 = fig1.to_html(full_html=False)






