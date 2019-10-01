#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

df = pd.read_csv('probs.csv', sep = ';', encoding = 'latin-1')

df_equipos = pd.read_csv('tabla_equipos_actual.csv', sep = ';', encoding = 'latin-1')
equipos = list(df_equipos['EQUIPO'])

def suma_puntos(row):
    indice_local = equipos.index(row['LOCAL'])
    indice_visita = equipos.index(row['VISITA'])
    if row['r_uniform'] <= row['GL']:
        puntajes[indice_local] += 3
    elif row['r_uniform'] >= 1 - row['GV']:
        puntajes[indice_visita] += 3
    else:
        puntajes[indice_local] += 1
        puntajes[indice_visita] += 1

n_iter = 10000
puntajes_guardados = []
posiciones_guardadas = []
for i in range(n_iter):
    puntajes = [0] * len(equipos)
    df['r_uniform'] = np.random.uniform(low=0.0, high=1.0, size=240)
    df.apply(suma_puntos, axis=1)
    puntajes_guardados.append(puntajes)
    
    s = pd.Series(puntajes)
    posiciones = list(s.rank(method='first', ascending = False))
    posiciones_guardadas.append(posiciones)

puntajes_guardados_df = pd.DataFrame(puntajes_guardados, columns = equipos)

ax1 = puntajes_guardados_df[puntajes_guardados_df.columns[::-1]].boxplot(vert=False)
ax1.xaxis.set_major_locator(ticker.MultipleLocator(2))
plt.xticks(rotation=90)
ax1.get_figure().savefig('boxplot_puntajes.png', bbox_inches = "tight")
plt.clf()

posiciones_guardadas_df = pd.DataFrame(posiciones_guardadas, columns = equipos)

ax2 = posiciones_guardadas_df[posiciones_guardadas_df.columns[::-1]].boxplot(vert=False)
ax2.xaxis.set_major_locator(ticker.MultipleLocator(1))
plt.xticks(rotation=90)
ax2.get_figure().savefig('boxplot_posiciones.png', bbox_inches = "tight")
plt.clf()

df2 = pd.DataFrame(np.zeros((len(equipos), len(equipos))),columns=equipos)
df2.index = range(1,1+len(equipos))

for index, row in posiciones_guardadas_df.iterrows():
    for equipo in list(df2.columns):
        df2.at[int(row[equipo]), equipo] += 1

df2.to_csv('matriz_resultados.csv', sep = ';', encoding = 'latin-1')



