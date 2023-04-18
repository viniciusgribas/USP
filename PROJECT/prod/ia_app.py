import streamlit as st
import pandas as pd
import plotly.express as px
from textblob import TextBlob
import base64
import io
import sys
import plotly.io as pio

pio.templates.default = "plotly"
sys.path.insert(0, '../utils')

import plotly.express as px
from get_data import get_data




# Leitura dos dados
@st.cache_data()
def load_data():
    data = get_data("https://dadosabertos.aneel.gov.br/dataset/6d90b77c-c5f5-4d81-bdec-7bc619494bb9/resource/11ec447d-698d-4ab8-977f-b424d5deee6a/download/siga-empreendimentos-geracao.csv")
    df = data.get_csv_data_from_aneel()

    numeric_df = df[['MdaPotenciaFiscalizadaKW','MdaGarantiaFisicaKW','MdaPotenciaOutorgadaKW']]
    numeric_cols = numeric_df.columns

    text_df = df[[   'UF',
                     'TipoGeracao',
                     'Fase',
                     'OrigemCombustivel',
                     'FonteCombustivel',
                     'Outorga',
                     'NomeCombustivel',
                     'GeracaoQualificada',] ]
    
    text_cols = text_df.columns

    return (numeric_cols, text_cols, df)

def convert_df(df):
   return df.to_csv(index=False, sep= ";", header=True, decimal= ',',encoding='ISO-8859-1')

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Configurações da página
st.set_page_config(page_title="SmartDash", page_icon="🚀")
# Add author information in the sidebar
st.sidebar.title("Author Information")
st.sidebar.image("https://media.licdn.com/dms/image/C4D03AQHcL597WbnKUw/profile-displayphoto-shrink_800_800/0/1656103164309?e=1687392000&v=beta&t=Xhrpz7x4yyZ8AJcFcUvgLgXgU34KmWxHOamwKAwMns0", width=200)  # Replace with your image URL
st.sidebar.markdown("""
Vinicius Guerra e Ribas

[![Email](https://img.icons8.com/color/20/000000/filled-message.png)](mailto:viniciusgribas@gmail.com)
[![LinkedIn](https://img.icons8.com/color/20/000000/linkedin.png)](https://www.linkedin.com/in/vinicius-guerra-e-ribas/)
[![GitHub](https://img.icons8.com/material-outlined/20/000000/github.png)](https://github.com/viniciusgribas)

---
👋 Greetings! As an accomplished data engineer and proficient 🐍 Python developer, I've dedicated my career to mastering the art of data collection, cleaning, and analysis. My expertise enables me to provide clients across the energy sector and various other industries with valuable and actionable insights.

🎓 I proudly hold an MBA postgraduate degree in Data Science and Analytics from the University of São Paulo. My education has provided me with a solid foundation in statistical analysis, machine learning, and data visualization. In addition to my academic achievements, I am highly skilled in Python, SQL, R, EXCEL, and data manipulation tools such as Pandas and Spark.

🌟 As a dedicated professional, I have built a diverse portfolio showcasing my expertise in various data-driven projects, including this Streamlit app. My work consistently demonstrates the ability to develop innovative solutions and derive actionable insights from complex data sets.

🔗 Let's connect and explore how we can collaborate to create data-driven solutions that deliver impactful results!
""")


# Título
st.title("Data Insights Hub")

# Carregamento dos dados
numeric_cols, text_cols, df = load_data()


tab1, tab2 = st.tabs(["Dataframe", "About"])

with tab1:
    st.write("""
        🔍 By clicking on the title of each column, you can sort the data to identify trends and patterns, such as the highest or lowest values, changes over time, or even correlations between different variables.""") 
    st.write("""💡 Try it out and discover valuable insights about your data!""")
    st.dataframe(df)
    csv = convert_df(df)

    st.download_button(
        "Download CSV",
        csv.encode('ISO-8859-1'),
        "file.csv",
        "text/csv",
        key='download-csv',
        )

with tab2:
    st.write("""The SIGA database is a public dataset provided by ANEEL, the Brazilian Electricity Regulatory Agency. It contains information about power generation enterprises in Brazil, including their locations, installed capacities, and other relevant data.
    [LINK🔗](https://dadosabertos.aneel.gov.br/dataset/siga-sistema-de-informacoes-de-geracao-da-aneel)""")
    st.image("https://dadosabertos.aneel.gov.br/uploads/group/2022-08-23-193719.950953MARCAS-ANEEL-022.png")

    st.subheader("Data Dictionary")
    st.write( """

        | Variable                 | Type        | Meaning                      |
        |--------------------------|-------------|------------------------------|
        | MdaGarantiaFisicaKW      | Numerical   | Physical Guarantee of Energy |
        | MdaPotenciaFiscalizadaKW | Numerical   | Supervised Electric Power    |
        | MdaPotenciaOutorgadaKW   | Numerical   | Granted Electric Power       |
        | Empreendimento           | Categorical | Business Name                |
        | UF                       | Categorical | Brasil States                |
        | TipoGeracao              | Categorical | Generation Type              |
        | Fase                     | Categorical | Operational Phase            |
        | OrigemCombustivel        | Categorical | Fuel Origin                  |
        | FonteCombustivel         | Categorical | Fuel Source                  |
        | NomeCombustivel          | Categorical | Fuel Name                    |
        | Outorga                  | Categorical | Grant                        |
        | GeracaoQualificada       | Categorical | Qualified Generation Mode    |
        | DatEntradaOperacao       | Date-Time   | Operation Start Date         |
        | DatInicioVigencia        | Date-Time   | Contract Start Date       |
        | DatFimVigencia           | Date-Time   | Contract End Date         |
        | X                        | Geographic  | Longitude Values             |
        | Y                        | Geographic  | Latitude Values              |
        |  ETL_CreatedDataLoad_At    |  Date-Time   | DataFrame creation date      |
        |  ETL_DataBase_LastModified |  Date-Time   | DataFrame Last Updated       |

        """)


# st.write("Teste")
tab3, tab4, tab5, tab6, tab7 = st.tabs(["Analysis 1", "Analysis 2", "Analysis 3", "Analysis 4", "Analysis 5"])
fases = df.Fase.unique() 
with tab3:
    st.write("""
        #  Try Analyses 🧪
        
        > 💡 interact with the graph by clicking on the desired section.

        > 📍 Remember to put on full screen for better viewing.
        
        """)
        
    st.write("""
        Bar Chart with one numeric variable and two categorical.  
        > 💡 Interact with the map by hovering the mouse over or try selecting an area.
    
    """)
    # Titulo
    st.subheader("Bar Chart Settings")

    x = st.selectbox("horizontal axis (category)", options=text_cols)
    y = st.selectbox("vertical axis (value)", options=numeric_cols)
    color_value = st.selectbox("color (category)", options=text_cols)
    phase = st.selectbox("phase (filter)", options=fases)
    title_BarChart = "Bar Chart with Numeric and Categorical Variables" 
    # adiciona um slider na barra lateral para ajustar a largura da figura
    width = 800

    # adiciona um slider na barra lateral para ajustar a altura da figura
    height = 800

    # atualiza a figura com as dimensões selecionadas
    
    
    fig_BarChart = px.bar(df[df.Fase == phase],  # Dataframe
    title=title_BarChart,                # Titulo
    x=x,                               # Variável Qualitativa Nominal
    y=y,                      # Variável Qualitativa Nominal
    #z= "MdaPotenciaOutorgadaKW" ,           # Variável Quantitativa Contínua
    color=color_value,               # Tipo de diagrama adicional para o eixo X
    )
    buffer = io.StringIO()
    fig_BarChart.write_html(buffer, include_plotlyjs='cdn')
    html_bytes = buffer.getvalue().encode()
    fig_BarChart.update_layout(width=width, height=height)

    st.download_button(
        label='Download HTML',
        data=html_bytes,
        file_name='stuff.html',
        mime='text/html'
    )
    st.plotly_chart(fig_BarChart)




with tab4:
    st.write("""
    #  Try Analyses 🧪
    
    > 💡 interact with the graph by clicking on the desired section.

    > 📍 Remember to put on full screen for better viewing.
    
    """)

    st.write("""
        Density and Bar Diagrams with categorical variables.    
        > 💡 Interact with the map by hovering the mouse over or try selecting an area.
    
    """)
    # Titulo
    st.subheader("Density Heatmap Settings")

    x = st.selectbox("x axis", options=text_cols)
    y = st.selectbox("y axis", options=text_cols)
    z = st.selectbox("z axis", options=numeric_cols)
    phase_density = st.selectbox("phase(filter)", options=fases)

    title_Densidade = "Density and Bar Diagrams with categorical variables"

    fig_dens = px.density_heatmap(df[df.Fase == phase_density],  
    title=title_Densidade,              
    x=x,                              
    y=y,                      
    z= z,           
    marginal_x="histogram",               
    marginal_y="histogram",              
    text_auto=True,                      
    width= 1500,
    height= 800,
    )

    buffer = io.StringIO()
    fig_dens.write_html(buffer, include_plotlyjs='cdn')
    html_bytes = buffer.getvalue().encode()

    st.download_button(
        label='Download HTML',
        data=html_bytes,
        file_name='stuff.html',
        mime='text/html'
    )
    st.plotly_chart(fig_dens)

    

with tab5:
    st.write("""
        🌞 The Sunburst Chart provides an interactive visualization of the granted power by phase, type of generation, and states in Brazil. 
        By hovering over different segments, you can see the values of the granted power and the corresponding labels. 
        You can also zoom in and out of different levels of the hierarchy, and click on the center to reset the view.
        """)
    st.write("""🔎 Take a closer look at the chart and discover hidden insights that may surprise you!""")


    fig_SunBurstChart = px.sunburst(df, 
        path=[px.Constant('BRASIL'),
            "OrigemCombustivel",
            # "NomeCombustivel",
            "Fase",
            "UF",
            
            "TipoGeracao",
            ],
        values='MdaPotenciaOutorgadaKW',
        title= 'Granted Power by Phase, Type of Generation and States in Brazil',
        width=750,
        height=750,
        maxdepth = -1,
        color_discrete_sequence=px.colors.qualitative.Vivid
    )

    fig_SunBurstChart.update_traces(root_color="lightgrey")
    fig_SunBurstChart.update_layout(margin = dict(t=50, l=50, r=50, b=50))

    st.plotly_chart(fig_SunBurstChart)

    st.write("""
        This analysis employs a sunburst chart to display the authorized power capacity categorized by phase, type of generation, 
        and Brazilian states. This chart offers a comprehensive view of power generation distribution across various phases, types, and states in one place. 
    """)

    st.write("""
    💡 This can help you identify patterns, trends, and potential areas for improvement in the power generation sector in Brazil. 🔍📈
    """)

    

    buffer = io.StringIO()
    fig_SunBurstChart.write_html(buffer, include_plotlyjs='cdn')
    html_bytes = buffer.getvalue().encode()

    st.download_button(
        label='Download HTML',
        data=html_bytes,
        file_name='stuff.html',
        mime='text/html'
    )

with tab6:
    st.write("""
        📊 The Strip Chart is an interactive chart that shows the distribution of a variable across different categories.
        In this case, it shows the distribution of granted power by state, generation type, and phase in Brazil.
        You can hover over each strip to see the corresponding label and value.
        You can also click on the legend to highlight or exclude certain categories, or zoom in and out using the buttons on the top right corner.
        """)
    st.write("""👁️ Keep an eye out for unusual trends or unexpected gaps in the data, as they could indicate underlying factors that warrant further investigation.""")

    fig_Strip = px.strip(df,  
    x="MdaPotenciaOutorgadaKW",  
    y="UF",                      
    orientation="h",            
    hover_name="Empreendimento", 
    title = 'Strip Chart - Power Granted by States, Generation Type, Phase and Business',
    color="TipoGeracao",      
    animation_frame='Fase',
    width=750,
    height=750,
    color_discrete_sequence=px.colors.qualitative.Vivid

    )
    st.plotly_chart(fig_Strip)

    buffer = io.StringIO()
    fig_Strip.write_html(buffer, include_plotlyjs='cdn')
    html_bytes = buffer.getvalue().encode()

    st.download_button(
        label='Download HTML',
        data=html_bytes,
        file_name='stuff.html',
        mime='text/html'
    )

with tab7:
    st.write("""
        🗺️ The Points Map is an interactive map that shows the location and details of power generation projects across Brazil. 
            You can zoom in and out using the buttons on the top right corner, and hover over each point to see the corresponding label and value.
            You can also click on the legend to highlight or exclude certain categories.
            """)
    st.write("""
        🧭 Explore the interactive map and analyze the location, size, and type of power generation projects in Brazil. 
        Look for patterns and trends that can inform strategic planning and investment decisions.
        Identify clusters of projects and assess the impact of regulatory policies on the distribution of power generation.""")


    df_map = df.get(df['X']!=0.0)
    fig_pointsMap = px.scatter_mapbox(df_map,                                         
        lat="Y",                                              
        lon="X",                                              
        color="TipoGeracao",                       
        size="MdaPotenciaOutorgadaKW",                        
        color_continuous_scale=px.colors.sequential.matter,   
        hover_name = "Empreendimento",                
        hover_data = ["MdaPotenciaOutorgadaKW"],
        title= 'Iterative Cartesian Coordinate Map',              
        size_max=80,                                          
        zoom=3,                      
        width=750,
        height=750,                         
        mapbox_style='open-street-map',                      
        animation_frame='Fase'                        
        )
    st.plotly_chart(fig_pointsMap)

    buffer = io.StringIO()
    fig_pointsMap.write_html(buffer, include_plotlyjs='cdn')
    html_bytes = buffer.getvalue().encode()

    st.download_button(
        label='Download HTML',
        data=html_bytes,
        file_name='stuff.html',
        mime='text/html'
    )


