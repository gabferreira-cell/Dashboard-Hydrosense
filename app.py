from dash import Dash, dcc, html, Input, Output, ctx
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

# === PREPARAÇÃO PARA DEPLOY: Define 'server' para Gunicorn/Plataformas de Hospedagem ===
# A variável 'server' é usada por servidores WSGI (como Gunicorn) em produção.
# 'app.server' é a instância Flask subjacente do Dash.

# === Dados (Simulação mais realista baseada em pesquisas agrícolas) ===
# Nota: Os dados foram ajustados para refletir a alta demanda de água no Verão
# e a sensibilidade do tomateiro, conforme o contexto científico.
dados = pd.DataFrame({
    'Estação': ['Primavera', 'Verão', 'Outono', 'Inverno'],
    'Uso_Água_m³': [5200, 7500, 4500, 2500], # Maior pico no Verão, menor no Inverno
    'Umidade_Solo_%': [70, 78, 65, 60]     # Umidade mais alta no Verão, refletindo maior irrigação
})

# === Cores e emojis ===
cores_estacoes = {
    'Primavera': {'principal': '#F4A7B9', 'fundo': '#FDEDEF', 'emoji': '🌸', 'legenda': 'Alta umidade e clima agradável'},
    'Verão': {'principal': '#FFA726', 'fundo': '#FFF3E0', 'emoji': '☀️', 'legenda': 'Maior uso de água devido ao calor'},
    'Outono': {'principal': '#FFD54F', 'fundo': '#FFF8E1', 'emoji': '🍂', 'legenda': 'Transição com menor irrigação'},
    'Inverno': {'principal': '#64B5F6', 'fundo': '#E3F2FD', 'emoji': '❄️', 'legenda': 'Menor uso de água e umidade baixa'},
    'Padrão': {'principal': '#2196F3', 'fundo': '#E3F2FD', 'emoji': '💧', 'legenda': 'Uso geral da irrigação e umidade'}
}

# === Inicializa o app ===
# Utiliza o tema BOOTSTRAP para um design moderno e responsivo
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Dashboard Irrigação do Tomate 🍅"

# VÍNCULO PARA O DEPLOY (usado pelo Gunicorn)
server = app.server

# === Layout base ===
app.layout = html.Div(id='pagina', style={
    'height': '100vh', # ALTURA FIXA para remover a barra de rolagem
    'width': '100%',
    'display': 'flex',
    'flexDirection': 'column',
    'alignItems': 'center',
    'justifyContent': 'space-evenly', # Distribui o espaço entre os elementos
    'backgroundColor': cores_estacoes['Padrão']['fundo'],
    'transition': 'background-color 0.8s ease'
}, children=[

    html.H1(id='titulo-principal',
            children="💧 Uso da Irrigação e Umidade do Solo no Plantio de Tomate",
            style={'textAlign': 'center', 'color': '#0D47A1', 'fontSize': '2.5rem', 'marginTop': '10px'}), # Margem superior para respiro

    # Área dos Botões de Filtro
    html.Div([
        *[
            html.Button(f"{cores_estacoes[estacao]['emoji']} {estacao}", id=f'btn-{estacao}', n_clicks=0,
                        style={
                            'backgroundColor': cores_estacoes[estacao]['principal'], 'color': 'white',
                            'border': 'none', 'padding': '10px 18px', 'margin': '0 5px',
                            'borderRadius': '8px', 'cursor': 'pointer', 'fontWeight': 'bold',
                            'boxShadow': '0 2px 4px rgba(0,0,0,0.2)', 'transition': 'all 0.3s ease',
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
    ], style={'textAlign': 'center'}), # Margem inferior removida, dependendo de space-evenly

    # Painel Principal (KPIs e Gráficos)
    html.Div(id='painel-central', style={
        'width': '95%',
        'maxWidth': '1200px',
        'flexGrow': 1, # FAZ O PAINEL CRESCER e ocupar o espaço vertical restante
        'maxHeight': '80vh', # Garante que não ultrapasse muito a tela em monitores pequenos
        'backgroundColor': cores_estacoes['Padrão']['fundo'],
        'borderRadius': '20px',
        'boxShadow': '0px 8px 25px rgba(0,0,0,0.2)',
        'padding': '30px',
        'transition': 'background-color 0.8s ease, box-shadow 0.8s ease'
    }, children=[
        # Linha dos KPIs
        dbc.Row([
            dbc.Col([
                html.H5("📊 Média de Umidade do Solo", style={'color': '#1565C0', 'textAlign': 'center', 'fontWeight': '600'}),
                html.H3(id='media-umidade', style={'textAlign': 'center', 'color': '#1565C0', 'marginBottom': '20px', 'fontSize': '2rem'})
            ], xs=12, md=6), # Responsividade: 12 colunas em mobile, 6 em desktop

            dbc.Col([
                html.H5("🚜 Média de Uso de Água", style={'color': '#2E7D32', 'textAlign': 'center', 'fontWeight': '600'}),
                html.H3(id='media-agua', style={'textAlign': 'center', 'color': '#2E7D32', 'marginBottom': '20px', 'fontSize': '2rem'})
            ], xs=12, md=6)
        ], className='mb-4'),

        # Linha dos Gráficos - Adicionado h-100 para garantir que os gráficos usem o espaço
        dbc.Row([
            dbc.Col(dcc.Graph(id='grafico-barras', config={'displayModeBar': False}, style={'height': '100%'}), xs=12, lg=6),
            dbc.Col(dcc.Graph(id='grafico-pizza', config={'displayModeBar': False}, style={'height': '100%'}), xs=12, lg=6)
        ], className='h-75') # Usando classes Bootstrap para ajudar na altura
    ]) # Fim do Painel Central
])

# === Callback para atualizar o Dashboard ===
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
    """
    Função que atualiza os gráficos e KPIs com base no botão de estação clicado.
    Também muda a cor de fundo e do painel para refletir a estação selecionada.
    """
    botao_id = ctx.triggered_id if ctx.triggered_id else 'btn-limpar'

    if botao_id != 'btn-limpar':
        estacao = botao_id.replace('btn-', '')
        df = dados[dados['Estação'] == estacao]
        cor_fundo = cores_estacoes[estacao]['fundo']
        cor_principal = cores_estacoes[estacao]['principal'] # Cor da estação
        cor_painel = cores_estacoes[estacao]['principal'] + '20' # Cor principal com 20% de opacidade para o painel
        emoji = cores_estacoes[estacao]['emoji']
        legenda = cores_estacoes[estacao]['legenda']
        titulo = f"{emoji} {estacao} — {legenda}"
    else:
        # Estado Padrão (Limpar Filtros)
        df = dados
        estacao = 'Padrão'
        cor_fundo = cores_estacoes[estacao]['fundo']
        cor_principal = cores_estacoes[estacao]['principal'] # Cor Padrão (azul)
        cor_painel = cores_estacoes[estacao]['fundo']
        emoji = '💧'
        legenda = 'Uso geral da irrigação e umidade'
        titulo = "💧 Uso da Irrigação e Umidade do Solo no Plantio de Tomate"

    # === Gráfico de Barras (Umidade do Solo) ===
    fig_bar = px.bar(df, x='Estação', y='Umidade_Solo_%', color='Estação',
                     color_discrete_map={
                         'Primavera': '#F4A7B9', 'Verão': '#FFA726',
                         'Outono': '#FFD54F', 'Inverno': '#64B5F6'
                     },
                     text='Umidade_Solo_%', # Adiciona o valor no topo da barra
                     labels={'Umidade_Solo_%': 'Umidade do Solo (%)', 'Estação': 'Estação'})
    
    fig_bar.update_traces(texttemplate='%{text}%', textposition='outside', marker_line_width=1.5, marker_line_color='white')
    fig_bar.update_layout(title='Umidade do Solo (%) Média', title_x=0.5,
                          plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                          showlegend=False,
                          yaxis_range=[0, 100], # Fixa o eixo Y para Umidade
                          transition={'duration': 800, 'easing': 'cubic-in-out'},
                          margin={'l': 20, 'r': 20, 't': 40, 'b': 20})

    # === Gráfico de Pizza (Uso de Água) ===
    fig_pizza = px.pie(df, values='Uso_Água_m³', names='Estação', hole=0.65,
                       color='Estação', color_discrete_map={
                           'Primavera': '#F4A7B9', 'Verão': '#FFA726',
                           'Outono': '#FFD54F', 'Inverno': '#64B5F6'
                       },
                       labels={'Uso_Água_m³': 'Volume de Água', 'Estação': 'Estação'})

    total_agua = df['Uso_Água_m³'].sum()
    
    # Texto central: Apenas valor, com cor dinâmica.
    text_color = cor_principal if botao_id != 'btn-limpar' else '#0D47A1'
    central_texto = f"<span style='font-size:30px; font-weight:bold; color:{text_color};'>{total_agua:,.0f} m³</span>"


    fig_pizza.update_traces(textinfo='percent+label', showlegend=False, hoverinfo='label+value+percent')
    fig_pizza.update_layout(
        title='Distribuição do Uso de Água (m³)',
        title_x=0.5,
        annotations=[dict(text=central_texto, x=0.5, y=0.5,
                          font=dict(color='#000000'), showarrow=False,
                          align='center', xanchor='center', yanchor='middle')],
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        transition={'duration': 800, 'easing': 'cubic-in-out'},
        margin={'l': 20, 'r': 20, 't': 40, 'b': 20}
    )

    # === Médias para os KPIs ===
    media_umidade = f"{df['Umidade_Solo_%'].mean():.1f}%"
    media_agua = f"{df['Uso_Água_m³'].mean():,.0f} m³"

    # Estilos dinâmicos
    estilo_pagina = {
        'height': '100vh',
        'width': '100%',
        'display': 'flex',
        'flexDirection': 'column',
        'alignItems': 'center',
        'justifyContent': 'space-evenly', # Manteve a distribuição de espaço
        'backgroundColor': cor_fundo,
        'transition': 'background-color 0.8s ease'
    }

    estilo_painel = {
        'width': '95%',
        'maxWidth': '1200px',
        'flexGrow': 1, # APLICADO AQUI para o painel central crescer
        'maxHeight': '80vh', # Limite de altura
        'backgroundColor': cor_painel,
        'borderRadius': '20px',
        'boxShadow': '0px 8px 25px rgba(0,0,0,0.2)',
        'padding': '30px',
        'transition': 'background-color 0.8s ease, box-shadow 0.8s ease'
    }

    return fig_bar, fig_pizza, media_umidade, media_agua, estilo_pagina, estilo_painel, titulo

# === Execução local (mantenha para testes no VS Code) ===
if __name__ == '__main__':
    # CORREÇÃO APLICADA AQUI: app.run_server() -> app.run()
    app.run(debug=True, port=8050)












