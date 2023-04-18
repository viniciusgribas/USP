import pandas as pd
import numpy as np
# import missingno as msno
import requests
from pathlib import Path
from datetime import datetime
import os


class get_data:
    
    def __init__(self, patch):
        self.patch = patch
    
    def line(self, x):
        print(x*50)

    def get_csv_data_from_aneel(self):
        


        # Assign path with the energy agency address for API access

        PATCH = self.patch

        # Applying a server request
        self.line('*')
        print("[1 - REQUESTING DATA FROM THE AGENCY]")
        self.line('*')

        response_API = requests.get(PATCH)

        # Check the file availability, if the value is 200 it was succeeded.


        print("Status Code")
        self.line('.')
        print(response_API.status_code)
        if response_API.status_code == 200:
            print("SUCCESS")
        else: 
            print("FAILED")

        # Vizualize the requested address information by the html page headers

        self.line('*')
        print('HEADERS')
        self.line('.')
        print(response_API.headers)
        DataBase_LastModified = response_API.headers['Last-Modified'] # The last data update is important information, a variable is assigned to it.

        # The encoding information can be obtained via the .encoding command
        self.line('*')
        print('ENCODING')
        self.line('.')
        print(response_API.encoding)
        self.line('*')

        # The ISO-8859-1 Encoding is the same as UTF-16 
        # We have to remember this information for the pd.read_csv function.
        # Creating a dataframe
        try:

            df_0 = pd.read_csv(PATCH, sep= ";", header=0, decimal= ',',encoding='ISO-8859-1')
            data_geracao = df_0.DatGeracaoConjuntoDados[0]
            self.line("_")
            print("DATA SUCCESSFULLY EXTRACTED")
            print(data_geracao)
            self.line("_")
        except:
            self.line("_")
            print("DATA EXTRACTION FAILED")
            self.line("_")


        self.line('*')
        print("[2 - DATA MANIPULATIONS]")
        self.line('*')
        df = df_0.copy()
        
        # print(df.columns)
        # df.info()
        # self.line("=")

        # print("""
        # #   VARIABLE CLASSIFICATION

        # ##  ##   Column                          Dtype             Variable Type          Decision
        # ## ---  ------                          -----              ----------         │ --------
        # ##  0   DatGeracaoConjuntoDados      │  object   │  CATEGORICAL-DATETIME      │  DROP
        # ##  1   NomEmpreendimento            │  object   │  CATEGORICAL-NOMINAL       │
        # ##  2   IdeNucleoCEG                 │  int64    │  CATEGORICAL-ORDINAL       │  DROP
        # ##  3   CodCEG                       │  object   │  CATEGORICAL-ORDINAL       │  DROP
        # ##  4   SigUFPrincipal               │  object   │  CATEGORICAL-NOMINAL       │
        # ##  5   SigTipoGeracao               │  object   │  CATEGORICAL-NOMINAL       │
        # ##  6   DscFaseUsina                 │  object   │  CATEGORICAL-ORDINAL       │
        # ##  7   DscOrigemCombustivel         │  object   │  CATEGORICAL-NOMINAL       │
        # ##  8   DscFonteCombustivel          │  object   │  CATEGORICAL-NOMINAL       │
        # ##  9   DscTipoOutorga               │  object   │  CATEGORICAL-ORDINAL       │
        # ##  10  NomFonteCombustivel          │  object   │  CATEGORICAL-ORDINAL       │
        # ##  11  DatEntradaOperacao           │  object   │  CATEGORICAL-DATETIME      │
        # ##  12  MdaPotenciaOutorgadaKw       │  float64  │  NUMERICAL-CONTINOUS-RATIO │
        # ##  13  MdaPotenciaFiscalizadaKw     │  int64    │  NUMERICAL-DISCRETE        │
        # ##  14  MdaGarantiaFisicaKw          │  float64  │  NUMERICAL-CONTINOUS-RATIO │
        # ##  15  IdcGeracaoQualificada        │  object   │  CATEGORICAL-BINARY        │
        # ##  16  NumCoordNEmpreendimento      │  float64  │  NUMERICAL-CONTINOUS-INTERVAL*│ 
        # ##  17  NumCoordEEmpreendimento      │  float64  │  NUMERICAL-CONTINOUS-INTERVAL*│
        # ##  18  DatInicioVigencia            │  object   │  CATEGORICAL-DATETIME      │
        # ##  19  DatFimVigencia               │  object   │  CATEGORICAL-DATETIME      │
        # ##  20  DscPropriRegimePariticipacao │  object   │  CATEGORICAL-NOMINAL       │  DROP
        # ##  21  DscSubBacia                  │  object   │  CATEGORICAL-NOMINAL       │  DROP
        # ##  22  DscMuninicpios               │  object   │  CATEGORICAL-NOMINAL       │  DROP

        # ### *Geographical Variables

        # # Using the .drop() function to delete unwanted columns
        # """)

        df = df.drop(columns=['DatGeracaoConjuntoDados','IdeNucleoCEG','CodCEG','DscPropriRegimePariticipacao','DscSubBacia'] )
      
        df.IdcGeracaoQualificada.fillna('Não',inplace=True)
     

        # For the 'DatInicioVigencia' column the 'nan' values was replaced by '1900-01-01'
        # Given that is a Date-Time Type Variable

        df.DatInicioVigencia.fillna('1900-01-01',inplace=True)
        df.DatInicioVigencia = pd.to_datetime(df.DatInicioVigencia)


        # For the 'DatEntradaOperacao' column the 'nan' values was replaced by '1900-01-01'
        # Given that is a Date-Time Type Variable

        df.DatEntradaOperacao.fillna('1900-01-01',inplace=True)
        df.DatEntradaOperacao = pd.to_datetime(df.DatEntradaOperacao)

        # Missing Values Analysis - After Transformations  

        # The .rename() function was used to rename and make it easier to interpret the variables

        df = df.rename( columns={
        "NomEmpreendimento":"Empreendimento",
        "SigUFPrincipal":"UF",
        "SigTipoGeracao":"TipoGeracao",
        "DscFaseUsina":"Fase",
        "DscOrigemCombustivel":"OrigemCombustivel",
        "DscFonteCombustivel":"FonteCombustivel",
        "NomFonteCombustivel":"NomeCombustivel",
        "DscTipoOutorga":"Outorga",
        "MdaGarantiaFisicaKw":"MdaGarantiaFisicaKW",
        "MdaPotenciaFiscalizadaKw":"MdaPotenciaFiscalizadaKW",
        "MdaPotenciaOutorgadaKw":"MdaPotenciaOutorgadaKW",
        "IdcGeracaoQualificada":"GeracaoQualificada",
        "NumCoordEEmpreendimento": "X",
        "NumCoordNEmpreendimento": "Y",	
        "DscMuninicpios":"Municipio"}
        )

        df

        # Create a new column with the datetime.now() function
        # enabling this ETL to store the output time.

        df['ETL_CreatedDataLoad_At'] = datetime.now().strftime("%Y.%m.%d - %H:%M:%S")
        df.ETL_CreatedDataLoad_At = pd.to_datetime(df.ETL_CreatedDataLoad_At)

        # Create a new column with the previously created variable 'DataBase_LastModified'
        # enabling this ETL to store the last update performed by the host.

        df['ETL_DataBase_LastModified'] = DataBase_LastModified
        df.ETL_DataBase_LastModified = pd.to_datetime(df.ETL_DataBase_LastModified).dt.tz_localize(None)

        # Determines the new directory path and the name of the file to be generated
        self.line('*')
        print("[3 - DATA DESCRIPTION AND FINAL OUTPUT]")
        self.line('*')

        df.DatEntradaOperacao = pd.to_datetime(df.DatEntradaOperacao)
        df.DatInicioVigencia  = pd.to_datetime(df.DatInicioVigencia)
        df.DatFimVigencia = pd.to_datetime(df.DatFimVigencia)
        df.ETL_CreatedDataLoad_At = pd.to_datetime(df.ETL_CreatedDataLoad_At)
        df.ETL_DataBase_LastModified = pd.to_datetime(df.ETL_DataBase_LastModified)

        self.line('_')
        print("3.1 - Analysing the number of unique values in each column")
        print('*'*50)
        # Unique Values Analyses.
        print(df.select_dtypes(['object']).nunique().sort_values())
        for col in df.select_dtypes(include=['object']):
            print('-'*50)
            print(col, '- Unique')
            print(df[col].unique())
        self.line('_')


        print('CREATION DATE [',df.ETL_CreatedDataLoad_At[1], ']') # Time this file was generated by the ETL
        print('LAST SERVER UPDATE ON DATA [',df.ETL_DataBase_LastModified[1],']') # Time the host last updated the file
        self.line("*")
        print(" [ SUCESS ] ")


        
        # VARIABLE METADATA

        # | Variable                 | Type        | Meaning                      |
        # |--------------------------|-------------|------------------------------|
        # | MdaGarantiaFisicaKW      | Numerical   | Physical Guarantee of Energy |
        # | MdaPotenciaFiscalizadaKW | Numerical   | Supervised Electric Power    |
        # | MdaPotenciaOutorgadaKW   | Numerical   | Granted Electric Power       |
        # | Empreendimento           | Categorical | Business Name                |
        # | UF                       | Categorical | Brasil States                |
        # | TipoGeracao              | Categorical | Generation Type              |
        # | Fase                     | Categorical | Operational Phase            |
        # | OrigemCombustivel        | Categorical | Fuel Origin                  |
        # | FonteCombustivel         | Categorical | Fuel Source                  |
        # | NomeCombustivel          | Categorical | Fuel Name                    |
        # | Outorga                  | Categorical | Grant                        |
        # | GeracaoQualificada       | C    ategorical | Qualified Generation Mode    |
        # | DatEntradaOperacao       | Date-Time   | Operation Start Date         |
        # | DatInicioVigencia        | Date-Time   | Start Date of Contract       |
        # | DatFimVigencia           | Date-Time   | End Date of Contract         |
        # | X                        | Geographic  | Longitude Values             |
        # | Y                        | Geographic  | Latitude Values              |
        # │ ETL_CreatedDataLoad_At   │ Date-Time   | DataFrame creation date      |
        # │ ETL_DataBase_LastModified│ Date-Time   | DataFrame Last Updated       |

        return(df)


