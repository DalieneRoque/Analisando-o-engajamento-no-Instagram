#!/usr/bin/env python
# coding: utf-8

#                                        Analisando o engajamento no Instagram
# 
#     O que queremos responder?
# 
#         Qual tipo de conteúdo mais engaja no Instagram da minha empresa?
# 
#         Temos a base de dados do Instagram desde que o usuário começou a postar na marca até o dia 27/março
# 
#         Ele também dá alguns direcionamentos: 
#             Podem ignorar a coluna visualizações, queremos entender apenas curtidas, comentários e interações. 
#             Tags vazias é que realmente não possuem tag (favor tratar como vazio).

#     Vamos importar e visualizar a nossa base

# In[ ]:


# importando o pandas

import pandas as pd


# In[93]:


# importar a base em excel
# Base: 001. Analisando o engajamento no Instagram.xlsx

base = pd.read_excel('001.Analisando o engajamento no Instagram.xlsx')


# In[94]:


# Visualizar as 5 primeiras linhas

base.head()


#     Como ele pediu para não considerar a coluna visualizações, vamos retirar essa coluna da base
#     O .drop() permite apagar uma coluna ou linha da base: base.drop(nome_coluna,axis=1)
# 
#     O axis = 1 se refere a coluna, enquanto axis = 0 se refere a linha
# 
#     Devemos passar o nome da coluna que queremos apagar da base
# 
#     Em caso de mais de 1 coluna, passamos a lista entre colchetes

# In[95]:


# Apagando a coluna "Visualizações"

base = base.drop('Visualizações',axis=1)


# In[96]:


# Visualizando novamente as 5 primeiras linhas

base.head()


# In[97]:


# Visualizando as 5 últimas linhas

base.tail()


# In[98]:


#Tamanho da base

base.shape


# In[99]:


# Verificando as informações

base.info()


#     Carrossel possui apenas 8 valores não nulos
#     Vamos entender os valores de carrossel
# 
# 

# In[100]:


# Contando os valores que aparecem na coluna Carrossel

base.Carrossel.value_counts()


#     Na verdade, os valores nulos são de postagens que não são carrossel. Sendo assim o nulo deveria ser “N”

#     Tratando os valores nulos

# In[101]:


# Filtrando os valores em que carrossel é nulo

base.loc[base.Carrossel.isnull()].head()


# In[102]:


# Buscando valores que NÃO são nulos

base.loc[base.Carrossel.notnull()].head()


# In[103]:


# Selecionando apenas a coluna Carrossel

base.loc[base.Carrossel.isnull(),'Carrossel'].head()


# In[104]:


# Agora vamos atribuir o valor N para essa coluna

base.loc[base.Carrossel.isnull(),'Carrossel'] = 'N'


# In[105]:


base.head()


# In[106]:


# Filtrando os valores em que carrossel é nulo

base.loc[base.Carrossel.isnull()].head()


# In[107]:


base.info()


# In[108]:


# Verificando novamente os valores dessa coluna

base.Carrossel.value_counts()


#     Mostrando as informações estatísticas

# In[109]:


# Descrição estatística da base

base.describe()


#     Visualizando essas informações de maneira gráfica

# In[110]:


# Um gráfico de dispersão ajudaria a entender melhor curtidas e comentários

base.plot(kind='scatter', x='Data', y='Curtidas', figsize=(14,8));


# In[111]:


# Podemos colocar curtidas e comentários no mesmo gráfico

ax = base.plot(kind='scatter', x='Data', y='Curtidas', color='blue', label='Curtidas', figsize=(14,8));
base.plot(kind='scatter', x='Data', y='Comentários', label='Comentários',figsize=(14,8),ax=ax);


# In[112]:


# A escala de curtidas pode  estar atrapalhando a visualização, por isso vamos deixar comentários em gráfico separado

base.plot(kind='scatter', x='Data', y='Comentários', color='red',label='Comentários',figsize=(14,8));


#     O gráfico e as informações estatísticas não estão dizendo muita coisa pois existe uma grande dispersão entre curtidas e comentários
# 
#     Precisamos verificar se existe um padrão usando as outras colunas de informações
# 
#     A primeira coisa que podemos fazer é pegar os 5 primeiros registros com mais e menos curtidas.

# In[113]:


# Ordenando os valores

base.sort_values(by='Curtidas', ascending=False).head()


# In[114]:


# Selecionando os 5 últimos valores

base.sort_values(by='Curtidas', ascending=False).tail()


#     Podemos observar que no top 5 todas as postagens tinham pessoas e eram fotos de campanha
# 
#     Nas 5 piores postagens, não haviam pessoas e nem eram postagens de campanhas
# 
#     Isso pode ser um indicador que pessoas e campanhas tem relação com as curtidas

# In[115]:


#Para melhorar a visualização, vamos criar um padrão no formato dos valores

pd.options.display.float_format = '{:,.2f}'.format


# In[116]:


#Agrupando as informações por tipo

base.groupby('Tipo')['Curtidas'].mean()


# In[117]:


# Agrupando por Tipo e Pessoas

base.groupby(['Tipo', 'Pessoas'])[['Curtidas']].mean()


# In[118]:


base.groupby(['Tipo', 'Pessoas'])[['Curtidas', 'Comentários']].mean()


# In[119]:


# Incluindo a coluna de campanhas

base.groupby(['Tipo', 'Pessoas', 'Campanhas'])[['Curtidas', 'Comentários']].mean()


#     O groupby já permite ver que publicações de campanha tem um grande engajamento e com foto de pessoas também
# 
#     Podemos então fazer os agrupamentos que acharmos melhor para entender os nossos dados

# In[120]:


# Somente para pessoas

base.groupby('Pessoas')[['Curtidas', 'Comentários']].mean()


# In[121]:


# Somente para campanhas

base.groupby('Campanhas')[['Curtidas', 'Comentários']].mean()


# In[122]:


# Carrossel sem filtrar a base = Esta errado essa comparação

base.groupby('Carrossel')[['Curtidas', 'Comentários']].mean()


# In[123]:


# Podemos também filtrar a base

base[base.Tipo == 'Foto'].groupby('Carrossel')[['Curtidas', 'Comentários']].mean()


#     A média sem usar carrossel é melhor do que quando usamos, então não é algo que possa impactar tanto no resultado das mídias dessa empresa olhando inicialmente
# 
#     Nesse caso devemos filtrar apenas as fotos pois só temos carrossel em fotos. Sem esse filtro estaríamos comparando coisas erradas
# 
#     Colocando pessoas e campanhas junto podemos ver como se dá essa diferença

# In[124]:


# Agregando por pessoas e campanhas

base.groupby(['Pessoas','Campanhas'])[['Curtidas', 'Comentários']].mean()


#     A média quando tem pessoas e publicação de campanhas é de cerca de 19,4 mil curtidas, já quando é apenas pessoas (sem campanha passa para quase 10mil e se não tiver pessoas chega no máximo a 5,9 mil mesmo em campanhas
# 
#     Nesse caso a gente já consegue mostrar para a empresa a importância de incluir pessoas usando os seus produtos, o que gera um aumento considerável no engajamento

# In[125]:


# Agregando por pessoas, campanhas e tipo

base.groupby(['Pessoas', 'Campanhas','Tipo'])[['Curtidas', 'Comentários']].mean()


#     Analisando novamente a questão do vídeo, ele não parece mais tão ruim assim. Quando feito em campanha e usando pessoas ele teve um resultado bom, inclusive próximo a foto
# 
#     O que poderia ter levado a média baixa é que só temos vídeos ou COM pessoa e COM campanha ou sem nenhum dos dois. Não temos nenhum vídeo com apenas um dos dois (pessoas ou campanha)
# 
#     Já IGTV, mesmo tendo pessoa, não teve um resultado tão bom
# 
#     Inclusive podemos entender o que havia gerado a média baixo no vídeo

# In[126]:


# Vamos filtrar a base apenas onde o tipo é video

base[base.Tipo == 'Vídeo']


#                                                  Conclusões
#                     
#     Em uma análise inicial, postagens incluindo pessoas engajam muito mais que aquelas que aquelas que não possui ninguém
# 
#     Postagens em épocas de campanha também possuem um melhor engajamento
# 
#     Nessa base, o carrossel não foi um diferencial para melhorar o engajamento da marca

#                                O que queremos responder?
#  
#     Qual a tag mais engaja nessas publicações? Agora queremos olhar apenas tags
# 
#     Ele também dá alguns direcionamentos: 
# 
#     Podem ignorar a coluna visualizações, queremos entender apenas curtidas, comentários e interações Tags vazias é que realmente não possuem tag (favor tratar como vazio)

# In[128]:


# Importando o pandas

import pandas as pd
import numpy as np

# Usando o mesmo formato dos valores
pd.options.display.float_format = '{:,.2f}'.format


# In[129]:


# Importar a base em excel
base = pd.read_excel('001.Analisando o engajamento no Instagram.xlsx')


# In[130]:


# Apagando a coluna 'Visualizações'

base = base.drop('Visualizações', axis=1)


# In[131]:


# Visualizando novamente as 5 primeiras linhas
base.head()


# In[132]:


# Agrupamento por tags
base.groupby('Tags')['Curtidas'].mean()


#     Para conseguir analisar separadamente as tags, podemos dividir linhas com 2 tags em 2 linhas
#     Para isso primeiro vamos usar o split para separar em uma lista com as tags
# 
#     Depois vamos usar o explode para transformar as listas com 2 tags em 2 linhas diferentes
# 
#     O split separa um texto em uma lista baseado em algum separador

# In[133]:


# Vamos usar isso para a nossa coluna 'Tags'
# Trasnformando a coluna Tags em uma linha de tags
base.Tags = base.Tags.str.split('/')
base.head()


#         O explode vai separar uma coluna de um DataFrame em 1 linha para cada elemento da lista
# 
#     ·         Tudo que estiver em lista será separado em 1 linha por elemento da lista
# 
#     ·         Se não tiver na lista, o elemento será mantido
# 
#     ·         Listas vazias vão ter o valor de NaN
# 
#  
# 
#     ·         Para as outras colunas, elas irão repetir os seus valores
# 
#     ·         Inclusive o índice também irá repetir

# In[134]:


# Separando a coluna Tag em 1 linha para cada elemento da linha
base = base.explode('Tags')
base.head()


#     Fazendo a mesma análise da média por tag
# 
#     Aviso importante: muito cuidado pois as outras colunas serão duplicadas, então não podemos fazer o mesmo cálculo da média que estávamos fazendo

# In[135]:


# Analisando a média de Tag
base.groupby('Tags')['Curtidas'].mean()


# In[136]:


# Ordenando por curtidas
base.groupby('Tags')[['Curtidas', 'Comentários']].mean().sort_values('Curtidas',ascending=False)


#        Postagens de promoções são as que mais engajam
# 
#     ·     Além de promoções, datas comemorativas e trends também possuem um bom engajamento

# In[137]:


# Filtrando valores sem tag
base[base.Tags.isnull()]


# In[138]:


base.loc[base.Tags.isnull(),'Tags']


#     Da mesma forma que fizemos para Carrossel, poderíamos ter feito para as tags escrevendo “Sem tag” e nesse caso iria aparecer no groupby.

# In[139]:


# Atribuindo o texto sem tag para as colunas onde a tag é NaN
base.loc[base.Tags.isnull(),'Tags'] = 'Sem tag'


# In[140]:


# Mostrando novamente a tabela de curtidas por tag
base.groupby('Tags')[['Curtidas', 'Comentários']].mean().sort_values('Curtidas',ascending=False)


# In[141]:


# Podemos voltar como NaN caso a gente queira somente ignorar esses valores conforme orientado
import numpy as np
base.loc[base.Tags == 'Sem tag', "Tags"] = np.nan


# In[142]:


# E voltamos com as colunas com valores nulos
base[base.Tags.isnull()]


# In[143]:


# E essas linhas novamente param de ser considerados na agregação
base.groupby('Tags')[['Curtidas', 'Comentários']].mean().sort_values('Curtidas',ascending=False)


#     Agora analisando as tags com pessoas e campanhas

# In[144]:


# Fazendo para Pessoas e Tag
base.groupby(['Pessoas', 'Tags'])[['Curtidas', 'Comentários']].mean()


# In[145]:


# Também podemos ordenar por curtidas
base.groupby(['Pessoas', 'Tags'])[['Curtidas', 'Comentários']].mean().sort_values('Curtidas',ascending=False)


# In[146]:


# Fazendo para Campanhas e Tag
base.groupby(['Campanhas', 'Tags'])[['Curtidas', 'Comentários']].mean().sort_values('Curtidas',ascending=False)


# ## Conclusões
# 
# ### Ter o rosto de outras pessoas é fundamental para um bom engajamento na publicação em todas as tags, quando havia o rosto, o resultado foi muito melhor
# 
# Criar campanhas ajuda muito na divulgação da marca
# 
# Promoções tiveram um desempenho absurdamente maior que qualquer outra tag porém é uma tag que pode ter custo para a loja, o que deve ser analisado
# 
# Usar conteúdo que estão em trend também ajudam na divulgação da marca, mesmo a trend sendo de outros nichos
# 
# A melhor maneira de mostrar produtos é através de outras pessoas utilizando-os, e se possível em campanhas de datas especiais.
# 
# Para novos produtos a inclusão de pessoas é mais crítica ainda, sendo quase o dobro quando há  um rosto junto ao produto.
# 
# Não podemos afirmar que Tag Loja é ruim até testarmos essa tag incluindo pessoas ou em uma campanha. Vale o teste para verificar.
# 
# Continuaremos a monitorar as postagens para encontrar novos padrões dado que ainda temos poucas informações da base.
