import sys
sys.path.append('C:/Users/wadka/Documents/scorecard')
import main
import plotly.express as px
import streamlit as st
import pandas as pd
pd.options.plotting.backend = "plotly"

week_ls = ('week1','week2','week3','week4','week5','week6','week7','week8')
week = st.sidebar.selectbox('select week',(week_ls))

dfweek = pd.read_sql("select * from {}".format(week),main.connection)

n = st.sidebar.selectbox('select name',(dfweek['name']))

del_btn = st.sidebar.button('delete record')   
if del_btn == True:
  main.cursor.execute("delete from {} where name = %s".format(week),(n,))
  main.connection.commit()
  st.success(f'deleted record for {n}', icon="✅")

st.subheader(n)

(col1,col2,col3,col4,col5) = st.columns(5)

def f0(a0,b0,c0,d0):
  score_ls = []  
  for i,j in zip(st.columns(a0),b0):
    with i:
      o = c0.set_index('name').loc[d0,j]
      score_ls.append(o)
      st.metric(label=j, value=o)

  vs1 = px.pie(values= score_ls[:5], names= b0[:5])
  st.plotly_chart(vs1)      
  
f0(5,main.par_ls,dfweek,n) 

hd_ls = ('test - peer comparison','assignment - peer comparison','behaviour - peer comparison','communication - peer comparison'
        ,'participation - peer comparison')  

def f1(a1,b1,c1,d1):
  for i,j in zip(d1,a1):
    st.subheader(i)
    color_discrete_map = { z:{ c1 : '#EF553B'}.get(z, '#636EFA') for z in b1.name}
    vs2 = b1.plot(x ='name', y=j , kind = 'bar', color='name', color_discrete_map = color_discrete_map)
    vs2 = vs2.update_layout(yaxis=dict(showgrid=False), xaxis={'categoryorder':'total descending'},showlegend=False)
    st.plotly_chart(vs2)

  st.subheader('tabular format - peer comparison')
  with st.expander('expand'):
    st.dataframe(data=b1, height=1200)

f1(main.par_ls,dfweek,n,hd_ls)  

st.download_button(label='download data', data=dfweek.to_csv(), file_name='weekly.csv', mime='text/csv')      