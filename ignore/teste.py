import pandas as pd
from pybaf import pybaf

key = '55TGKKBnP79cJxveQeOm~MIrRMhh_wJEiCCmMumvvJA~AtsupJEjwEsphI6j3AFjFZ9oTID2xMW53eQx1XBwaRIQv808EVYmeyx-GaZ-l1LE'

pybaf = pybaf(key=key)

print(pybaf)
cidades = pd.read_csv('cidades.csv', encoding='iso 8859-1', delimiter=';')
cidades['latitude'] = cidades['latitude'].str.replace(',','.')
cidades['longitude'] = cidades['longitude'].str.replace(',','.')

sc_cidades = cidades.loc[cidades['Estado']==('SC')]
rs_cidades = cidades.loc[cidades['Estado'] == ('RS')]
pr_cidades =  cidades.loc[cidades['Estado'] == ('PR')]

df_origin = pr_cidades[:55]
df_destination = df_origin

df_matrix_pr = pybaf.distance_matrix(df_destination=df_origin, df_origin=df_destination, destination_id='codigo_ibge',
                                     origin_id='codigo_ibge')

df_matrix_pr.to_csv('resultado.csv')

df_matrix = pd.read_csv('resultado.csv')

print(df_matrix['codigo_ibge'].nunique())
