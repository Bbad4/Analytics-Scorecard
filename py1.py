from datetime import date, timedelta
import streamlit as st
import pandas as pd
pd.options.plotting.backend = "plotly"
import plotly.graph_objects as go
from sqlalchemy import create_engine,URL,text

parameters_ls = ['assignment', 'practical', 'interpersonal', 'extracurricular', 'attendance']

##for postgres
'''@st.cache_resource
def engine():
    engine = create_engine(URL.create('postgresql+psycopg2', username = 'postgres', password = 'root', database = 'postgres', host = '127.0.0.1', port = '5432'))  
    return engine
engine = engine()'''
##

##for sqlite
@st.cache_resource
def engine():
    engine = create_engine('sqlite:///analytics_scorecard.db')
    return engine
engine = engine()

with engine.connect() as conn:
    query = text(f'''PRAGMA foreign_keys = ON''')
    conn.execute(query)
##

def records_ls(col_name,tbl_name):
    with engine.connect() as conn:
        query = text(f'''SELECT {col_name} FROM {tbl_name}''')
        result = conn.execute(query)
    ls = [row[0] for row in result.fetchall()]
    return st.selectbox(col_name,(ls))


def crud_facts(candidate_name, round_name, points_ls, operation):

    with engine.begin() as conn:

        params = {'candidate_name': candidate_name, 'round_name': round_name} if points_ls is None else {'candidate_name': candidate_name, 'round_name': round_name, 
                'points_0': points_ls[0], 'points_1': points_ls[1], 'points_2': points_ls[2], 'points_3': points_ls[3], 'points_4': points_ls[4]}

        if operation == 'insert':
            query = text(f'''insert into facts (candidate_name ,round_name, assignment, practical, interpersonal, extracurricular, attendance) 
                        VALUES (:candidate_name, :round_name, :points_0, :points_1, :points_2, :points_3, :points_4)''')
            conn.execute(query, params)
            st.success(f'record inserted for {candidate_name} {round_name}', icon='✅')

        elif operation == 'update':
            query = text(f'''update facts 
                        set assignment = :points_0, practical = :points_1, interpersonal = :points_2, extracurricular = :points_3, attendance = :points_4
                        where round_name = :round_name and candidate_name = :candidate_name ''')
            conn.execute(query, params)
            st.success(f'record updated for {candidate_name} {round_name}', icon='✅')

        elif operation == 'delete':
            query = text(f'''delete from facts where candidate_name = :candidate_name and round_name = :round_name ''')
            conn.execute(query, params)
            st.success(f'record deleted for {candidate_name} {round_name}', icon='✅')            

        elif operation == 'select':
            query = text(f'''select * from facts where candidate_name = :candidate_name and round_name = :round_name ''')
            result = conn.execute(query, params)
            if result.fetchone() is None:
                return None
            else:
                record_df = pd.read_sql(query, params=params, con=conn)
                st.table(record_df)
                return record_df 
        

def crud_candidates(candidate_name, city_name, operation):

    with engine.begin() as conn:

        params = {'candidate_name': candidate_name} if city_name is None else {'candidate_name': candidate_name, 'city_name': city_name}

        if operation == 'insert':
            query = text(f'''insert into candidates (candidate_name , city_name) 
                        VALUES (:candidate_name, :city_name) ''')
            conn.execute(query, params)
            st.success(f'record inserted for {candidate_name}' , icon='✅') 

        elif operation == 'update':
            query = text(f'''update candidates 
                        set city_name = :city_name
                        where candidate_name = :candidate_name ''')
            conn.execute(query, params)
            st.success(f'record updated for {candidate_name}', icon='✅')

        elif operation == 'delete':
            query = text(f'''delete from candidates where candidate_name = :candidate_name ''')
            conn.execute(query, params)
            st.success(f'record deleted for {candidate_name}', icon='✅')            

        elif operation == 'select':
            query = text(f'''select * from candidates where candidate_name = :candidate_name ''')
            result = conn.execute(query, params)
            if result.fetchone() is None:
                return None
            else:
                record_df = pd.read_sql(query, params=params, con=conn)
                st.table(record_df)
                return record_df      


def crud_rounds(round_name, start_date, end_date, operation):

    with engine.begin() as conn:

        params = {'round_name': round_name} if start_date and end_date is None else {'round_name': round_name, 'start_date': start_date, 'end_date': end_date}

        if operation == 'insert':
            query = text(f'''insert into rounds (round_name , start_date, end_date) 
                        VALUES (:round_name, :start_date, :end_date) ''')
            conn.execute(query, params)
            st.success(f'record inserted for {round_name}' , icon='✅') 

        elif operation == 'update':
            query = text(f'''update rounds 
                        set start_date = :start_date, end_date = :end_date
                        where round_name = :round_name ''')
            conn.execute(query, params)
            st.success(f'record updated for {round_name}', icon='✅')

        elif operation == 'delete':
            query = text(f'''delete from rounds where round_name = :round_name ''')
            conn.execute(query, params)
            st.success(f'record deleted for {round_name}', icon='✅')            

        elif operation == 'select':
            query = text(f'''select * from rounds where round_name = :round_name ''')
            result = conn.execute(query, params)
            if result.fetchone() is None:
                return None
            else:
                record_df = pd.read_sql(query, params=params, con=conn)
                st.table(record_df)
                return record_df 


def sliced_df(col_name,col_val,radio_btn):
    with engine.begin() as conn:
        params = {'col_val': col_val}
        query = text(f'''select * from facts where {col_name} = :col_val ''')
        sliced_df = pd.read_sql(query, params=params, con=conn)
    sliced_df_csv = sliced_df.to_csv(index=False)
    name = f'{radio_btn}_comparison_{col_val}'
    st.sidebar.download_button(f':arrow_double_down: {name}', data=sliced_df_csv, file_name=f'{name}.csv')
    return sliced_df  


def piechart(return_obj):
    values_ls = return_obj.loc[:,parameters_ls].values.tolist()
    data = go.Pie(labels = parameters_ls, values = sum(values_ls, []))
    fig = go.Figure(data=data)
    st.plotly_chart(fig)   


def overall_avg_piechart(sliced_df,col_val):
    values_ls = sliced_df.loc[:,parameters_ls].mean().values.tolist()
    data = go.Pie(labels = parameters_ls, values = values_ls)
    fig = go.Figure(data=data)
    st.subheader(f'{col_val} overall distribution')
    st.plotly_chart(fig)  


def stacked_barchart(sliced_df,col_val,col_name):    
    x_ls = sliced_df.loc[:,[col_name]].values.tolist()  
    y_ls = sliced_df.loc[:,parameters_ls].values.tolist()
    y_ls = list(zip(*y_ls))
    data = [go.Bar(name = i, x = sum(x_ls, []), y = j) for i,j in zip(parameters_ls,y_ls)]
    fig = go.Figure(data=data)
    fig.update_layout(barmode='stack')
    st.subheader(f'{col_val} total')
    st.plotly_chart(fig)


def individual_barcharts(sliced_df,col_val,col_name):
    for i in parameters_ls:
        x_ls = sliced_df.loc[:,[col_name]].values.tolist() 
        y_ls = sliced_df.loc[:,[i]].values.tolist()
        colors = ['#0068c9' if value == col_val else '#83c9ff' for value in sum(x_ls, [])]
        data = [go.Bar(x = sum(x_ls, []), y = sum(y_ls, []), marker=dict(color=colors))]
        fig = go.Figure(data=data)
        st.subheader(i)
        st.plotly_chart(fig)


def download_btn(tbl_name):
    with engine.begin() as conn:
        query = text(f'''select * from {tbl_name}''')
        table_df = pd.read_sql(query, con=conn)
    table_df_csv = table_df.to_csv(index=False)
    name = f'{tbl_name}_table'
    st.sidebar.download_button(f':arrow_double_down: {name}', data=table_df_csv, file_name=f'{name}.csv')
    

