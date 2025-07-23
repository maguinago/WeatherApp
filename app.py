import dash.exceptions
from dash import Dash, html, dash_table, dcc, Input, Output, State, callback
from dash.dash_table.Format import Format, Scheme, Symbol
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

# Load data
from dash.exceptions import PreventUpdate

month_list = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro",
              "outubro", "novembro", "dezembro"]

file = 'assets/Anexo_Arquivo_Dados_Projeto_Logica_e_programacao_de_computadores.csv'
df = pd.read_csv(file)
df['data'] = pd.to_datetime(df['data'], dayfirst=True, errors='coerce')
df['data_str'] = df['data'].dt.strftime('%d/%m/%Y')

df['ano'] = df['data'].dt.year
df['mes'] = df['data'].dt.month

# Group by year
year_series = df.groupby('ano').agg({
    'minima': 'mean',
    'temp_media': 'mean',
    'maxima': ['mean', 'max'],
    'precip': ['mean', 'sum']
}).reset_index()

# Group by month and year
month_series = df.groupby(['ano', 'mes']).agg({
    'precip': 'sum',
    'minima': 'mean',
    'maxima': 'mean',
    'temp_media': 'mean'
}).reset_index()

# Rename columns
year_series.columns = ['year', 'min_temp_avg', 'avg_temp_avg', 'max_temp_avg', 'max_temp_max', 'precipitation_avg',
                       'precipitation_sum']

# Create figure
fig = px.bar(
    year_series,
    x='year',
    labels=["Rarara", "rereer"],
    y=year_series.columns,
    barmode='group',
    title='Weather Summary by Year'
)

# Initialize app
app = Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.DARKLY,
                                                                              "https://cdn.jsdelivr.net/npm/bootstrap"
                                                                              "-icons@1.10.5/font/bootstrap-icons "
                                                                              ".css"])

# Layout


# Navbar
navbar = dbc.Navbar(
    dbc.Container([
        dbc.Row([
            dbc.Col(
                dbc.NavbarBrand([
                    html.Img(src="assets/img.png", className="bi bi-cloud-sun-fill me-2", height="30px"),
                    "Weather Dashboard"
                ], href="/home")),

        ], align="center", className="g-0"),

        dbc.Nav([
            dbc.NavItem(dbc.NavLink("Home", href="/home")),
            dbc.NavItem(dbc.NavLink("Questão A", href="/questao-a")),
            dbc.NavItem(dbc.NavLink("Questão B", href="/questao-b")),
            dbc.NavItem(dbc.NavLink("Questão C", href="/questao-c")),
            dbc.NavItem(dbc.NavLink("Questão D", href="/questao-d")),
        ], className="ms-auto", navbar=True),
    ]),
    color="primary",
    dark=True
)

# Footer
footer = dbc.Container(
    dbc.Row([
        html.P("2025 Weather Dashboard© - Criado por Guilherme Magnago",
               className="text-center py-3 text-light mb-0 mt-3")
    ],
        className='bg-secondary w-100',
        align='center'),
    fluid=True
)

app.layout = html.Div([
    dcc.Store(id='selected-month', storage_type='session', data=None),

    navbar,

    dcc.Location(id='url', refresh=True),  # Tracks URL
    dbc.Container(id='page-content', className='mt-5 mb-4 flex-grow-1'),  # Where the page content loads

    footer

],
    className="d-flex flex-column min-vh-100",
    style={'backgroundColor': '#ADB5BD'}
)

table_a = dbc.Container(
    dash_table.DataTable(
        id='data-table-a',
        data=df.to_dict('records'),
        columns=[
            {"name": "Data", "id": "data_str"},  # Str date column, used for visualization but not for sorting/filtering
            {"name": "Precipitação", "id": "precip", "hideable": True},
            {"name": "Temp. Mínima", "id": "minima", "hideable": True},
            {"name": "Temp. Média", "id": "temp_media", "hideable": True},
            {"name": "Temp. Máxima", "id": "maxima", "hideable": True},
            {"name": "H. de Insolação", "id": "horas_insol", "hideable": True},
            {"name": "Umidade Rel.", "id": "um_relativa", "hideable": True},
            {"name": "Vel. do Vento", "id": "vel_vento", "hideable": True},
            {"name": "Date Real", "id": "data"},  # Hidden, used for sorting/filtering
        ],
        page_size=15,
        sort_mode='single',

        page_current=0,
        page_action='native',
        style_header={
            'font-weight': 'bold',
            'border': '10px #F8F9FA',
            'padding': '20px 5px'
        },
        style_table={
            'overflowX': 'auto',
            'padding': '1em',
        },
        style_cell={
            'textAlign': 'center',
            'backgroundColor': '#161A1D',
            'border': 'light-grey',
            'padding': '0.5em',
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'even'},
                'backgroundColor': '#303030',
            }
        ],
        style_as_list_view=True,

        hidden_columns=['data'],  # Hidden real date column
    ),
    className='mt-3'
)

a_layout = dbc.Container([
    dbc.Row([
        dbc.Col([html.H2("Questão A:"),
                 html.P(["Gerar uma tabela com possibilidade de filtrar datas e escolher as colunas a serem mostradas.",
                         html.Br(),
                         "Função adicional: ordenamento dos dados."
                         ])
                 ])
    ]),

    dbc.Row([
        dbc.Col(
            dcc.DatePickerRange(
                id='date-range',
                min_date_allowed=df['data'].min().date(),
                max_date_allowed=df['data'].max().date(),
                start_date=df['data'].min().date(),
                end_date=df['data'].max().date(),
                display_format='DD/MM/YYYY',
                className="mb-2"
            ),
            width=9
        ),

        dbc.Col([
            html.Label("Ordenar por:"),
            dbc.Select(
                id='sort-by',
                options=[
                    {"label": "Data", "value": "data"},
                    {"label": "Precipitação", "value": "precip"},
                    {"label": "Temp. Mínima", "value": "minima"},
                    {"label": "Temp. Média", "value": "temp_media"},
                    {"label": "Temp. Máxima", "value": "maxima"},
                ],
                value="data",  # Default to date
                className="mb-2 me-1",
            )
        ], width=2),

        dbc.Col([
            html.Div([
                html.Label("⇵", className="w-50 mx-auto text-center"),
                dbc.Button("↑", id="order-button", color="primary", outline=True, n_clicks=0,
                           className="mb-2 me-1 w-50 d-flex justify-content-center")
            ], className="d-flex flex-column align-items-center"
            )], width=1),
    ],
        className="align-items-end g-0"
    ),

    dbc.Row([
        table_a
    ])
])


# Question A data printing callback
@app.callback(
    Output('data-table-a', 'data'),
    Output('order-button', 'children'),
    Input('date-range', 'start_date'),
    Input('date-range', 'end_date'),
    Input('sort-by', 'value'),
    Input('order-button', 'n_clicks')
)
def update_a_table(start_date, end_date, sort_by, n_clicks):
    dff = df.copy()

    # Filter by date
    if start_date and end_date:
        start = pd.to_datetime(start_date)
        end = pd.to_datetime(end_date)
        dff = dff[(dff['data'] >= start) & (dff['data'] <= end)]

    # Determine sort order from button clicks
    ascending = n_clicks % 2 == 0
    arrow = "↑" if ascending else "↓"

    # Apply sorting
    if sort_by == "data":
        dff = dff.sort_values(by="data", ascending=ascending)
    else:
        dff = dff.sort_values(by=sort_by, ascending=ascending)

    return dff.to_dict('records'), arrow


# Calculate rainiest_month for B answer
rainiest_month = month_series.loc[month_series['precip'].idxmax()]
month = month_list[int(rainiest_month['mes']) - 1]
year = int(rainiest_month['ano'])
precipitation = str(round(rainiest_month['precip'], 1)) + "mm"
rainiest_month = [f"O mês mais chuvoso da série histórica foi ", html.B(month), " de ",
                  html.B(year), " com precipitação total de ", html.B(precipitation), "."]

b_layout = dbc.Container([
    dbc.Row([
        dbc.Col([html.H2("Questão B:"),
                 html.P("Encontrar o mês mais chuvoso da série histórica.")
                 ])
    ],
    ),

    dbc.Row([
        dbc.Col([
            dbc.Button("Mostrar Resposta", n_clicks=0, id="show-answer", color="primary", className="mx-auto w-100"),
        ],
            className='mt-4 mx-auto d-flex', width={"size": 2}
        )
    ],
        justify="evenly",
    ),
    dbc.Row([
        dbc.Fade(
            dbc.Card(
                dbc.CardBody(
                    html.H2(rainiest_month, className="card-text text-center", style={'line-height': '2'}),

                )
            ),
            className="w-50 mx-auto",
            id="answer",
            is_in=False,
            appear=False,
        )
    ], className='mt-4 mx-auto')
])


# Displaying question B answer callback
@app.callback(
    Output("answer", "is_in"),
    Output("show-answer", "children"),
    [Input("show-answer", "n_clicks")],
    [State("answer", "is_in")],
)
def display_b_answer(n, is_in):
    if n % 2 == 0:
        # Button has never been clicked
        return False, "Mostrar Resposta"
    return not is_in, "Esconder Resposta"


# BACKUP
c_layout = dbc.Container([
    dbc.Row([
        dbc.Col([html.H2("Questão C:"),
                 html.Br(),
                 html.H5("Retornar dados de 2006-2016 de temperatura mínima, média e máxima com base no input do "
                         "usuário.")
                 ],
                className='mt-4',
                width={"size": "auto", "order": 1, "offset": 1},
                ),

    ], className="mb-5"
    ),

    # List group
    dbc.Row([
        dbc.Col(
            [
                dbc.RadioItems(
                    id="radios-c",
                    className="btn-group d-flex",
                    inputClassName="btn-check",
                    labelClassName="btn btn-outline-primary",
                    labelCheckedClassName="active",
                    options=[
                        {"label": month.title(), "value": idx + 1} for idx, month in enumerate(month_list)
                    ],
                    value=None,
                ),

            ],
            className="radio-group",
            width="auto",
        ),
    ],
        className="justify-content-center"
    ),
    dbc.Row([
        dbc.Col(
            html.Div("", id="c-output"),
            className="mx-auto",
            width=6
        )
    ],
        className="mt-5 mb-5 justify-content-center"
    )
])


# Generating table from C callback
@app.callback(
    Output("c-output", "children"),
    # Output("selected-month", "data"),
    Input("radios-c", "value")
)
def display_c_table(value=None):
    dff = month_series.copy()
    if value is None:
        raise dash.exceptions.PreventUpdate

    filtered = dff.query('2006 <= ano <= 2016 and mes == @value')

    table = dash_table.DataTable(
        data=filtered.to_dict('records'),
        page_size=12,
        columns=[
            dict(id='ano', name='Ano', type='numeric'),
            dict(id='minima', name='Temp. Mínima', type='numeric', hideable=True,
                 format=Format(precision=3).symbol(Symbol.yes).symbol_suffix('ºC')),
            dict(id='temp_media', name='Temp. Média', type='numeric', hideable=True,
                 format=Format(precision=3).symbol(Symbol.yes).symbol_suffix('ºC')),
            dict(id='maxima', name='Temp. Máxima', type='numeric', hideable=True,
                 format=Format(precision=3).symbol(Symbol.yes).symbol_suffix('ºC')),
        ],
        page_action='native',
        style_header={
            'font-weight': 'bold',
            'border': '10px #F8F9FA',
            'padding': '20px 5px'
        },
        style_table={
            'overflowX': 'auto',
            'backgroundColor': '#F8F9FA',
        },
        style_cell={
            'textAlign': 'center',
            'backgroundColor': '#161A1D',
            'border': 'light-grey'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'even'},
                'backgroundColor': '#303030',
            }
        ],
        style_as_list_view=True,
    )

    return table


d_layout = dbc.Container([
    dbc.Row([
        dbc.Col([html.H2("Questão D:"),
                 html.Br(),
                 html.H5("Retornar gráfico com dados de 2006-2016 de temperatura mínima, média e máxima com base no "
                         "input do usuário.")
                 ],
                className='mt-4',
                width={"size": "auto", "order": 1, "offset": 1},
                ),

    ], className="mb-5"
    ),
    dbc.Row([
        dbc.Col(
            [
                dbc.RadioItems(
                    id="radios-d",
                    className="btn-group d-flex",
                    inputClassName="btn-check",
                    labelClassName="btn btn-outline-primary",
                    labelCheckedClassName="active",
                    options=[
                        {"label": month.title(), "value": idx + 1} for idx, month in enumerate(month_list)
                    ],
                    value=None,
                ),
            ],
            className="radio-group",
            width="auto",
        ),
    ],
        className="justify-content-center"
    ),
    dbc.Row([
        dbc.Col([

            dcc.Slider(id='d-slider', min=50, max=100, value=75, disabled=True,
                       marks={x: str(x) for x in [50, 75, 100]})

        ], className="mx-auto mt-5 justify-content-center", width=6)
    ], align="center", className="g-0"),
    dbc.Row([
        dbc.Col([

            html.Div(

                id="d-output",
                className='mx-auto',
                style={"textAlign": "center",
                       "width": "100%",
                       "margin": "auto",
                       "minHeight": "500px",

                       },

            )
        ], className="justify-content-center mx-auto mt-5")
    ], align="center", className="justify-content-center mx-auto"),

], fluid=True
)


# Question D plotting graph for month
@app.callback(
    Output("d-output", "children"),
    Output("d-slider", "disabled"),
    Input("radios-d", "value"),
    Input("d-slider", "value"),
)
def generate_d_chart(month, size=75):
    if month is None:
        raise dash.exceptions.PreventUpdate
    else:
        # Generate data (like for exercise C)
        dff = month_series.copy()

        filtered = dff.query('2006 <= ano <= 2016 and mes == @month')
        long_form = px.data.medals_long()
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=filtered['ano'],
            y=filtered['maxima'],
            name='Máxima',
            marker_color='red',
            opacity=0.4,
            hovertemplate='X: %{x}<br>Y: %{y:.1f}ºC<extra></extra>'
        ))

        fig.add_trace(go.Bar(
            x=filtered['ano'],
            y=filtered['temp_media'],
            name='Média',
            marker_color='yellow',
            opacity=0.6,
            hovertemplate='X: %{x}<br>Y: %{y:.1f}ºC<extra></extra>'
        ))

        fig.add_trace(go.Bar(
            x=filtered['ano'],
            y=filtered['minima'],
            name='Mínima',
            marker_color='lightskyblue',
            opacity=0.8,
            hovertemplate='X: %{x}<br>Y: %{y:.1f}ºC<extra></extra>'
        ))
        fig.update_layout(
            title=dict(
                text=f"Temperaturas em {month_list[month - 1]}, entre {filtered['ano'].min()} - {filtered['ano'].max()}",
                x=0.5,
                xanchor="center",
                font=dict(size=28, weight=750)
            ),
            barmode='overlay',
            xaxis_title='Ano',
            yaxis_title='Temperatura (ºC)',
            xaxis=dict(dtick=1),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0.1)',
            margin_t=150
        )

        return dcc.Graph(figure=fig, config={"responsive": True},
                         style={
                             "display": "inline-block",
                             "width": f"{size}%",
                         }
                         ), False


home_layout = dbc.Container([
    dbc.Row([
        html.H1("Início")
    ]),
    dbc.Row([
        html.H3([
            html.Br(),
            html.B("\n\nBem-vind@ ao analisador de Dados do Clima de Porto Alegre.\n"),
        ]
        ),
    ], className="mb-5"),
    dbc.Row([
        html.H4([

            "Este dashboard foi criado como uma evolução do projeto final da cadeira de ",
            html.B("Lógica de Programação "),
            "da Graduação em ",
            html.B("Análise e Desenvolvimento de Sistemas"),
            " da PUCRS Online.",
            html.Br(),
            html.Br(),
            "O projeto consistiu em processar dados do clima de Porto Alegre entre 1961 e 2016 e responder questões "
            "específicas com base em inputs do usuário no prompt de comando.",
            html.Br(),
            html.Br(),
            "Como forma de continuar explorando módulos de Python, desta vez focando em usar dataframes e na criação de "
            "interfaces de usuário, usei Pandas e Dash para dar forma ao Dashboard. Para criar uma interface de "
            "elaborada de forma simplificada, utilizei o dash-bootstrap-components, que organiza os componentes em "
            "grids. "
        ], style={'line-height': "1.5em"})
    ]),
], className='align-middle', style={"max-width": "70%"}
)


# Page navigation callback
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'),
              )
def display_page(pathname):
    if pathname == '/questao-a':
        return a_layout
    if pathname == '/questao-b':
        return b_layout
    if pathname == '/questao-c':
        return c_layout
    if pathname == '/questao-d':
        return d_layout
    else:
        return home_layout


if __name__ == '__main__':
    app.run(debug=True)
