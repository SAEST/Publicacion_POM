import pandas as pd
import re

# Columnas del archivo
CONTABILIZADA = 'CONTABILIZADA'
OBSERVACIONES = 'OBSERVACIONES'
LISTA_NOMINAL = 'LISTA_NOMINAL'
TOTAL_VOTOS_CALCULADO = 'TOTAL_VOTOS_CALCULADO'
TIPO_CASILLA = 'TIPO_CASILLA'
ACTAS_ESPERADAS = 'ACTAS_ESPERADAS'
ACTAS_REGISTRADAS = 'ACTAS_REGISTRADAS'
ACTAS_FUERA_CATALOGO = 'ACTAS_FUERA_CATALOGO'
ACTAS_CAPTURADAS = 'ACTAS_CAPTURADAS'
PORCENTAJE_ACTAS_CAPTURADAS = 'PORCENTAJE_ACTAS_CAPTURADAS'
ACTAS_CONTABILIZADAS = 'ACTAS_CONTABILIZADAS'
PORCENTAJE_ACTAS_CONTABILIZADAS = 'PORCENTAJE_ACTAS_CONTABILIZADAS'
PORCENTAJE_ACTAS_INCONSISTENCIAS = 'PORCENTAJE_ACTAS_INCONSISTENCIAS'
ACTAS_NO_CONTABILIZADAS = 'ACTAS_NO_CONTABILIZADAS'
LISTA_NOMINAL_ACTAS_CONTABILIZADAS = 'LISTA_NOMINAL_ACTAS_CONTABILIZADAS'
TOTAL_VOTOS_C_CS = 'TOTAL_VOTOS_C_CS'
TOTAL_VOTOS_S_CS = 'TOTAL_VOTOS_S_CS'
PORCENTAJE_PARTICIPACION_CIUDADANA = 'PORCENTAJE_PARTICIPACION_CIUDADANA'

def cargar_y_filtrar_datos():
    file_path = './data/bd/pres-csv/PRES_2024.csv' 
    df = pd.read_csv(file_path, skiprows=4, delimiter=',', low_memory=False)
    df1 = pd.read_csv(file_path, skiprows=3, nrows=1, header=None, 
                      names=["ACTAS_ESPERADAS","ACTAS_REGISTRADAS","ACTAS_FUERA_CATALOGO",
                             "ACTAS_CAPTURADAS","PORCENTAJE_ACTAS_CAPTURADAS","ACTAS_CONTABILIZADAS",
                             "PORCENTAJE_ACTAS_CONTABILIZADAS","PORCENTAJE_ACTAS_INCONSISTENCIAS",
                             "ACTAS_NO_CONTABILIZADAS","LISTA_NOMINAL_ACTAS_CONTABILIZADAS",
                             "TOTAL_VOTOS_C_CS","TOTAL_VOTOS_S_CS","PORCENTAJE_PARTICIPACION_CIUDADANA"])

    # Limpiar los valores de la columna OBSERVACIONES
    def limpiar_valor(valor):
        if isinstance(valor, str):
            return ', '.join(re.findall(r"'([^']*)'", valor))
        return valor
    df[OBSERVACIONES] = df[OBSERVACIONES].apply(limpiar_valor)

    # Filtros para realizar conteos y enviarlos como parametros
    valores_especificos = ['1']
    valores_especificos2 = ['2']
    valores_especificos3 = ['0']
    valores_especificos4 = ['0','1','2']
    valores_especificos5 = ['0','1']
    valores_especificos6 = [
        'Todos los campos ilegibles',
        'Sin dato',
        'Ilegible',
        'Todos los campos vacíos',
        'Ilegible, Sin dato',
        'Excede Lista Nominal',
        'Excede Lista Nominal, Sin dato',
        'Excede Lista Nominal, Ilegible',
        'Excede Lista Nominal, Ilegible, Sin dato'
    ]

    if CONTABILIZADA in df.columns:
        filtro = df['CONTABILIZADA'].isin(valores_especificos)
        df_filtrado = df[filtro]

    if CONTABILIZADA in df.columns:
        filtro2 = df['CONTABILIZADA'].isin(valores_especificos2)
        df_filtrado2 = df[filtro2]

    if CONTABILIZADA in df.columns:
        filtro3 = df['CONTABILIZADA'].isin(valores_especificos3)
        df_filtrado3 = df[filtro3]

    if CONTABILIZADA in df.columns:
        filtro4 = df['CONTABILIZADA'].isin(valores_especificos4)
        df_filtrado4 = df[filtro4]

    if CONTABILIZADA in df.columns:
        filtro5 = df['CONTABILIZADA'].isin(valores_especificos5)
        df_filtrado5 = df[filtro5]

    if OBSERVACIONES in df.columns:
        filtro6 = df['OBSERVACIONES'].isin(valores_especificos6)
        df_filtrado6 = df[filtro6]

    if CONTABILIZADA in df.columns and LISTA_NOMINAL in df.columns:
        df_filtrado7 = df[df['CONTABILIZADA'] == 1].copy()
        # Convertir los datos a numéricos si es necesario
        df_filtrado7['LISTA_NOMINAL'] = pd.to_numeric(df_filtrado['LISTA_NOMINAL'], errors='coerce')
        
    if CONTABILIZADA in df.columns and TOTAL_VOTOS_CALCULADO in df.columns:
        df_filtrado8 = df[df['CONTABILIZADA'] == 1].copy()
        # Convertir los datos a numéricos si es necesario
        df_filtrado8['TOTAL_VOTOS_CALCULADO'] = pd.to_numeric(df_filtrado['TOTAL_VOTOS_CALCULADO'], errors='coerce')

    if TOTAL_VOTOS_CALCULADO in df.columns and TIPO_CASILLA in df.columns:
        #df_filtrado9 = df[df[TIPO_CASILLA] != 'S'].copy()
        df_filtrado9 = df[(df['CONTABILIZADA'].isin(['1','2'])) & (df['TIPO_CASILLA'] != 'S')].copy()
        # Convertir los datos a numéricos si es necesario
        df_filtrado9['TOTAL_VOTOS_CALCULADO'] = pd.to_numeric(df_filtrado9['TOTAL_VOTOS_CALCULADO'], errors='coerce')

    # Retornar los DataFrames filtrados y df1 para otros datos
    return df, df1, df_filtrado, df_filtrado2, df_filtrado3, df_filtrado4, df_filtrado5, df_filtrado6, df_filtrado7, df_filtrado8, df_filtrado9

def calcular_data_values(df, df1, df_filtrado, df_filtrado2, df_filtrado3, df_filtrado4, df_filtrado5, df_filtrado6, df_filtrado7, df_filtrado8, df_filtrado9):   
    value_counts = df_filtrado['CONTABILIZADA'].astype(int).value_counts().sum()
    value_counts1 = df_filtrado2['CONTABILIZADA'].astype(int).value_counts().sum()
    value_counts2 = df_filtrado3['CONTABILIZADA'].astype(int).value_counts().sum()
    value_counts3 = df_filtrado4['CONTABILIZADA'].astype(int).value_counts().sum() 
    value_counts4 = df_filtrado5['CONTABILIZADA'].astype(int).value_counts().sum() 
    value_counts5 = (df_filtrado5['CONTABILIZADA'].astype(int).value_counts().sum() * 100) / df1['ACTAS_ESPERADAS'].astype(int).values 
    value_counts5 = pd.Series(value_counts5)
    value_counts5 = value_counts5.apply(lambda x: int(x * 10000) / 10000)
    value_counts5 = value_counts5.iloc[0]
    value_counts6 = (df_filtrado['CONTABILIZADA'].value_counts() * 100) / df1['ACTAS_ESPERADAS'].astype(int).values 
    value_counts6 = pd.Series(value_counts6)
    value_counts6 = value_counts6.apply(lambda x: int(x * 10000) / 10000)
    value_counts6 = value_counts6.iloc[0]
    value_counts7 = (df_filtrado6['OBSERVACIONES'].value_counts().sum() * 100) / df1['ACTAS_ESPERADAS'].astype(int).values 
    value_counts7 = pd.Series(value_counts7)
    value_counts7 = value_counts7.apply(lambda x: int(x * 10000) / 10000)
    value_counts7 = value_counts7.iloc[0]
    value_counts8 = df_filtrado7['LISTA_NOMINAL'].sum()
    value_counts9 = (df_filtrado8['TOTAL_VOTOS_CALCULADO'].sum() * 100) / value_counts8
    value_counts9 = pd.Series(value_counts9)
    value_counts9 = value_counts9.apply(lambda x: int(x * 10000) / 10000)
    value_counts9 = value_counts9.iloc[0]
    value_counts10 = df_filtrado8['TOTAL_VOTOS_CALCULADO'].sum()
    value_counts11 = df_filtrado9['TOTAL_VOTOS_CALCULADO'].sum()
    actas_regis = int(df1['ACTAS_REGISTRADAS'].values[0])
    actas_fuera = int(df1['ACTAS_FUERA_CATALOGO'].values[0])
    actas_cap = int(df1['ACTAS_CAPTURADAS'].values[0])
    actas_cap_por = float(df1['PORCENTAJE_ACTAS_CAPTURADAS'].values[0])
    actas_con = int(df1['ACTAS_CONTABILIZADAS'].values[0])
    actas_con_por = float(df1['PORCENTAJE_ACTAS_CONTABILIZADAS'].values[0])
    actas_incon_por = float(df1['PORCENTAJE_ACTAS_INCONSISTENCIAS'].values[0])
    actas_nocon = int(df1['ACTAS_NO_CONTABILIZADAS'].values[0])
    lnactascon = int(df1['LISTA_NOMINAL_ACTAS_CONTABILIZADAS'].values[0])
    totalvotosc = int(df1['TOTAL_VOTOS_C_CS'].values[0])
    totalvotoss = int(df1['TOTAL_VOTOS_S_CS'].values[0])
    participacionciu = float(df1['PORCENTAJE_PARTICIPACION_CIUDADANA'].values[0])

    return {
            "value_counts": value_counts,
            "value_counts1": value_counts1,
            "value_counts2": value_counts2,
            "value_counts3": value_counts3,
            "value_counts4": value_counts4,
            "value_counts5": value_counts5,
            "value_counts6": value_counts6,
            "value_counts7": value_counts7,
            "value_counts8": value_counts8,
            "value_counts9": value_counts9,
            "value_counts10": value_counts10,
            "value_counts11": value_counts11,
            "actas_regis": actas_regis,
            "actas_fuera": actas_fuera,
            "actas_cap": actas_cap,
            "actas_cap_por": actas_cap_por,
            "actas_con": actas_con,
            "actas_con_por": actas_con_por,
            "actas_incon_por": actas_incon_por,
            "actas_nocon": actas_nocon,
            "lnactascon": lnactascon,
            "totalvotosc": totalvotosc,
            "totalvotoss": totalvotoss,
            "participacionciu": participacionciu
    }