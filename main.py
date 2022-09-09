import psycopg2
import streamlit as st

connection = psycopg2.connect(database="postgres", user="postgres", password="root", host="127.0.0.1", port="5432")
cursor = connection.cursor()

week_ls = ('week1','week2','week3','week4','week5','week6','week7','week8')
week = st.sidebar.selectbox('select week',(week_ls))

with st.form(key='from1'):
  st.subheader(week)

  n = st.text_input('name', value='')

  par_ls = ('test','assignment','behaviour','communication','participation')
  score_ls = []
  for i in par_ls:
    o = st.number_input(i, value=25, step=1)
    score_ls.append(o)
  
  st.metric(label='total', value=sum(score_ls))

  submit_button = st.form_submit_button(label='submit')

def f1(tb_name):  
  cursor.execute("select * from {} where name = %s" .format(tb_name), (n,))  
  row=cursor.fetchone()
  
  if(row==None):
    cursor.execute("insert into {} (name, test, assignment, behaviour, communication, participation) values (%s,%s,%s,%s,%s,%s)" .format(tb_name), ([n]+score_ls))
    connection.commit()
    st.success(f'added record for {n}!' , icon="✅")
  else:
    cursor.execute("update {} set (test, assignment, behaviour, communication, participation) = (%s,%s,%s,%s,%s) where name = %s" .format(tb_name), (score_ls+[n])) 
    connection.commit()
    st.success(f'name {n} already existed, so we updated the records!', icon="✅")

if submit_button == True:
  if len(n) == 0:
    st.warning('please enter a name', icon='⚠️')
  else:  
    f1(week)