import sys
sys.path.append('C:/Users/wadka/Documents/scorecard')
sys.path.append('C:/Users/wadka/Documents/scorecard/pages')
import weekly
import main
import plotly.express as px
import streamlit as st
import pandas as pd
pd.options.plotting.backend = "plotly"

dfoverall = pd.read_sql("select * from parameters",main.connection)

n1 = st.sidebar.selectbox('select name',(dfoverall['name']))
st.subheader(n1)

total_ls = ('test_total','assignment_total','behaviour_total','communication_total','participation_total','parameters_total')

(col1,col2,col3,col4,col5,col6) = st.columns(6)

weekly.f0(6,total_ls,dfoverall,n1) 

hd_ls = ('test total - peer comparison','assignment total - peer comparison','behaviour total - peer comparison','communication total - peer comparison'
        ,'participation total - peer comparison','parameters total - peer comparison')

weekly.f1(total_ls,dfoverall,n1,total_ls)     

st.download_button(label='download data', data=dfoverall.to_csv(), file_name='overall.csv', mime='text/csv')   