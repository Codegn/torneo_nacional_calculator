#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import matplotlib


# In[2]:


df = pd.read_csv('probs.csv', sep = ';', encoding = 'latin-1')


# In[3]:


df.tail(3)


# In[4]:


df_equipos = pd.read_csv('tabla_equipos_actual.csv', sep = ';', encoding = 'latin-1')
equipos = list(df_equipos['EQUIPO'])
equipos


# In[5]:


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


# In[6]:


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


# In[7]:


puntajes_guardados_df = pd.DataFrame(puntajes_guardados, columns = equipos)


# In[8]:


puntajes_guardados_df.tail(3)


# In[18]:


boxplot = puntajes_guardados_df.boxplot(rot=90)


# In[10]:


posiciones_guardadas_df = pd.DataFrame(posiciones_guardadas, columns = equipos)


# In[11]:


posiciones_guardadas_df.tail(3)


# In[12]:


boxplot2 = posiciones_guardadas_df.boxplot(rot=90)


# In[13]:


df2 = pd.DataFrame(np.zeros((len(equipos), len(equipos))),columns=equipos)
df2.index = range(1,1+len(equipos))


# In[14]:


df2.head()


# In[15]:


for index, row in posiciones_guardadas_df.iterrows():
    for equipo in list(df2.columns):
        print(equipo)
        df2.at[int(row[equipo]), equipo] += 1


# In[16]:


df2


# In[17]:


df2.to_csv('matriz_resultados.csv', sep = ';', encoding = 'latin-1')


# In[ ]:





# In[ ]:




