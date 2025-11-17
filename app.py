from dash import Dash, dcc, html, Input, Output, ctx
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

# === Dados simulados ===
dados = pd.DataFrame({
    'Estação': ['Primavera', 'Verão', 'Outono', 'Inverno'],
    'Uso_Água_m³': [5200, 7500, 4500, 2500],
    'Umidade_Solo_%': [70, 78, 65, 60]
})

# === Cores e Emojis ===
cores_estacoes = {
    'Primavera': {'principal': '#F4A7B9', 'fundo': '#FDEDEF', 'emoji': '🌸', 'legenda': 'Alta umidade e clima agradável'},
    'Verão': {'principal': '#FFA726', 'fundo': '#FFF3E0', 'emoji': '☀️', 'legenda': 'Maior uso de água devido ao calor'},
    'Outono': {'principal': '#FFD54F', 'fundo': '#FFF8E1', 'emoji': '🍂', 'legenda': 'Transição com menor irrigação'},
    'Inverno': {'principal': '#64B5F6', 'fundo': '#E3F2FD', 'emoji': '❄️', 'legenda': 'Menor uso de água e umidade baixa'},
    'Padrão': {'principal': '#2196F3', 'fundo': '#E3F2FD', 'emoji': '💧', 'legenda': 'Uso geral da irrigação e umidade'}
}

# === Inicializa o app ===
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Dashboard Irrigação do Tomate 🍅"
server = app.server

# === Layout ===
app.layout = html.Div(id='pagina', style={
    'height': '100vh',
    'width': '100%',
    'display': 'flex',
    'flexDirection': 'column',
    'alignItems': 'center',
    'justifyContent': 'space-evenly',
    'backgroundColor': cores_estacoes['Padrão']['fundo'],
    'transition': 'background-color 0.8s ease'
}, children=[

    html.H1(id='titulo-principal',
            children="💧 Uso da Irrigação e Umidade do Solo no Plantio de Tomate",
            style={'textAlign': 'center', 'color': '#0D47A1', 'fontSize': '2.5rem'}),

    html.Div([
        *[
            html.Button(f"{cores_estacoes[estacao]['emoji']} {estacao}", id=f'btn-{estacao}', n_clicks=0,
                        style={
                            'backgroundColor': cores_estacoes[estacao]['principal'],
                            'color': 'white', 'border': 'none', 'padding': '10px 18px',
                            'margin': '0 5px', 'borderRadius': '8px', 'cursor': 'pointer',
                            'fontWeight': 'bold', 'boxShadow': '0 2px 4px rgba(0,0,0,0.2)',
                            'transition': 'all 0.3s ease',
                        })
            for estacao in ['Primavera', 'Verão', 'Outono', 'Inverno']
        ],
        html.Button("Limpar Filtros", id='btn-limpar', n_clicks=0,
                    style={
                        'backgroundColor': '#1565C0', 'color': 'white',
                        'border': 'none', 'padding': '10px 18px', 'margin': '0 5px',
                        'borderRadius': '8px', 'cursor': 'pointer', 'fontWeight': 'bold',
                        'boxShadow': '0 2px 4px rgba(0,0,0,0.2)', 'transition': 'all 0.3s ease',
                    })
    ], style={'textAlign': 'center'}),

    html.Div(id='painel-central', style={
        'width': '95%', 'maxWidth': '1200px',
        'flexGrow': 1, 'maxHeight': '80vh',
        'backgroundColor': cores_estacoes['Padrão']['fundo'],
        'borderRadius': '20px', 'boxShadow': '0px 8px 25px rgba(0,0,0,0.2)',
        'padding': '30px',
        'transition': 'background-color 0.8s ease, box-shadow 0.8s ease'
    }, children=[
        dbc.Row([
            dbc.Col([
                html.H5("📊 Média de Umidade do Solo", style={'color': '#1565C0', 'textAlign': 'center'}),
                html.H3(id='media-umidade', style={'textAlign': 'center', 'color': '#1565C0'})
            ], xs=12, md=6),
            dbc.Col([
                html.H5("🚜 Média de Uso de Água", style={'color': '#2E7D32', 'textAlign': 'center'}),
                html.H3(id='media-agua', style={'textAlign': 'center', 'color': '#2E7D32'})
            ], xs=12, md=6)
        ], className='mb-4'),

        dbc.Row([
            dbc.Col(dcc.Graph(id='grafico-barras', config={'displayModeBar': False}, style={'height': '100%'}), xs=12, lg=6),
            dbc.Col(dcc.Graph(id='grafico-pizza', config={'displayModeBar': False}, style={'height': '100%'}), xs=12, lg=6)
        ], className='h-75')
    ])
])

# === Callback ===
@app.callback(
    [Output('grafico-barras', 'figure'),
     Output('grafico-pizza', 'figure'),
     Output('media-umidade', 'children'),
     Output('media-agua', 'children'),
     Output('pagina', 'style'),
     Output('painel-central', 'style'),
     Output('titulo-principal', 'children')],
    [Input('btn-Primavera', 'n_clicks'),
     Input('btn-Verão', 'n_clicks'),
     Input('btn-Outono', 'n_clicks'),
     Input('btn-Inverno', 'n_clicks'),
     Input('btn-limpar', 'n_clicks')]
)
def atualizar_dashboard(*botoes):
    botao_id = ctx.triggered_id if ctx.triggered_id else 'btn-limpar'

    if botao_id != 'btn-limpar':
        estacao = botao_id.replace('btn-', '')
        df = dados[dados['Estação'] == estacao]
        cor_fundo = cores_estacoes[estacao]['fundo']
        cor_principal = cores_estacoes[estacao]['principal']
        cor_painel = cores_estacoes[estacao]['principal'] + '20'
        emoji = cores_estacoes[estacao]['emoji']
        legenda = cores_estacoes[estacao]['legenda']
        titulo = f"{emoji} {estacao} — {legenda}"
    else:
        df = dados
        estacao = 'Padrão'
        cor_fundo = cores_estacoes[estacao]['fundo']
        cor_principal = cores_estacoes[estacao]['principal']
        cor_painel = cores_estacoes[estacao]['fundo']
        titulo = "💧 Uso da Irrigação e Umidade do Solo no Plantio de Tomate"

    fig_bar = px.bar(df, x='Estação', y='Umidade_Solo_%', color='Estação',
                     color_discrete_map={
                         'Primavera': '#F4A7B9', 'Verão': '#FFA726',
                         'Outono': '#FFD54F', 'Inverno': '#64B5F6'
                     },
                     text='Umidade_Solo_%', labels={'Umidade_Solo_%': 'Umidade do Solo (%)'})
    fig_bar.update_traces(texttemplate='%{text}%', textposition='outside', marker_line_width=1.5,
                          marker_line_color='white')
    fig_bar.update_layout(title='Umidade do Solo (%) Média', title_x=0.5,
                          plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                          showlegend=False, yaxis_range=[0, 100],
                          transition={'duration': 1000, 'easing': 'cubic-in-out'},
                          margin={'l': 20, 'r': 20, 't': 40, 'b': 20})

    fig_pizza = px.pie(df, values='Uso_Água_m³', names='Estação', hole=0.65,
                       color='Estação', color_discrete_map={
                           'Primavera': '#F4A7B9', 'Verão': '#FFA726',
                           'Outono': '#FFD54F', 'Inverno': '#64B5F6'
                       })
    total_agua = df['Uso_Água_m³'].sum()
    text_color = cor_principal if botao_id != 'btn-limpar' else '#0D47A1'
    central_texto = f"<span style='font-size:30px; font-weight:bold; color:{text_color};'>{total_agua:,.0f} m³</span>"
    fig_pizza.update_traces(textinfo='percent+label', showlegend=False)
    fig_pizza.update_layout(title='Distribuição do Uso de Água (m³)', title_x=0.5,
                            annotations=[dict(text=central_texto, x=0.5, y=0.5, showarrow=False)],
                            plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                            transition={'duration': 1000, 'easing': 'cubic-in-out'},
                            margin={'l': 20, 'r': 20, 't': 40, 'b': 20})

    media_umidade = f"{df['Umidade_Solo_%'].mean():.1f}%"
    media_agua = f"{df['Uso_Água_m³'].mean():,.0f} m³"

    estilo_pagina = {'height': '100vh', 'width': '100%', 'display': 'flex',
                     'flexDirection': 'column', 'alignItems': 'center', 'justifyContent': 'space-evenly',
                     'backgroundColor': cor_fundo, 'transition': 'background-color 0.8s ease'}

    estilo_painel = {'width': '95%', 'maxWidth': '1200px', 'flexGrow': 1,
                     'maxHeight': '80vh', 'backgroundColor': cor_painel, 'borderRadius': '20px',
                     'boxShadow': '0px 8px 25px rgba(0,0,0,0.2)', 'padding': '30px',
                     'transition': 'background-color 0.8s ease, box-shadow 0.8s ease'}

    return fig_bar, fig_pizza, media_umidade, media_agua, estilo_pagina, estilo_painel, titulo


import os

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8050))
    app.run(host='0.0.0.0', port=port, debug=False)




























