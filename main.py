#pip install sqlalchemy psycopg2 pandas plotly streamlit
from datetime import date, timedelta
import streamlit as st
import pandas as pd
pd.options.plotting.backend = "plotly"
import plotly.graph_objects as go
from sqlalchemy import create_engine,URL,text
from py1 import *


def facts():
    candidate_name = records_ls('candidate_name','candidates')
    round_name = records_ls('round_name','rounds')
    return_obj = crud_facts(candidate_name, round_name, None, 'select')
    
    st.info(f'''no record exists for {candidate_name} {round_name}, you can insert here''' if return_obj is None
                else f'''record exists for {candidate_name} {round_name}, you can update or delete here''', icon='*️⃣') 

    with st.form(key='from1'):
        points_ls = [st.number_input(i, value=25, step=1, min_value=0, max_value=50) for i in parameters_ls]
        submit_button_insert_update = st.form_submit_button(label='insert' if return_obj is None else 'update')     
        if return_obj is not None:
            submit_button_delete = st.form_submit_button(label='delete') 

    if submit_button_insert_update:
        crud_facts(candidate_name, round_name, points_ls, 'insert' if return_obj is None else 'update')
        crud_facts(candidate_name, round_name, None, 'select') 

    if return_obj is not None:
        if submit_button_delete:
            crud_facts(candidate_name, round_name, None, 'delete')


def candidates():
    st.info(f'''you can insert new records here''', icon='*️⃣')

    with st.form(key='from1'):
        candidate_name = st.text_input('candidate_name', 'candidate1')
        city_name = st.text_input('city_name', 'city1')
        submit_button_insert = st.form_submit_button(label='insert')   

    if submit_button_insert:
        return_obj = crud_candidates(candidate_name, None, 'select')
        if city_name.isalnum() and candidate_name.isalnum() and return_obj is None: 
            crud_candidates(candidate_name, city_name, 'insert')
            crud_candidates(candidate_name, None, 'select')                  
        else:  
            st.warning(f'''record already exists for {candidate_name} or candidate_name / city_name is not alphanumeric''', icon='⚠️') 
   
    st.write("<hr>", unsafe_allow_html=True)

    candidate_name = records_ls('candidate_name','candidates')
    crud_candidates(candidate_name, None, 'select')

    st.info(f'''you can update or delete record for {candidate_name} here''', icon='*️⃣') 

    with st.form(key='from2'):
        city_name = st.text_input('city_name', 'city1')
        submit_button_update = st.form_submit_button(label='update')  
        submit_button_delete = st.form_submit_button(label='delete') 

    if submit_button_update:
        if city_name.isalnum(): 
            crud_candidates(candidate_name, city_name, 'update')
            crud_candidates(candidate_name, None, 'select')  
        else:  
            st.warning(f'''city_name should only be alphanumerics''', icon='⚠️')

    if submit_button_delete:
        crud_candidates(candidate_name, None, 'delete')
        st.session_state['candidate_name'] = candidate_name
        st.experimental_rerun()
        
    if 'candidate_name' in st.session_state:
        candidate_name = st.session_state['candidate_name']
        st.success(f'record deleted for {candidate_name}', icon='✅')
        del st.session_state['candidate_name']


def rounds():
    st.info(f'''you can insert new records here''', icon='*️⃣')

    with st.form(key='from1'):
        round_name = st.text_input('round_name', 'round1')
        start_date = st.date_input('start_date', date.today())
        end_date = st.date_input('end_date', date.today() + timedelta(days=7))
        submit_button_insert = st.form_submit_button(label='insert')   

    if submit_button_insert:
        return_obj = crud_rounds(round_name, start_date, end_date, 'select')
        if start_date < end_date and round_name.isalnum() and return_obj is None: 
            crud_rounds(round_name, start_date, end_date, 'insert')
            crud_rounds(round_name, None, None, 'select')                  
        else:  
            st.warning(f'''record already exists for {round_name} or round_name is not alphanumeric or start_date is greater than end_date''', icon='⚠️') 
   
    st.write("<hr>", unsafe_allow_html=True)

    round_name = records_ls('round_name','rounds')
    crud_rounds(round_name, None, None, 'select')

    st.info(f'''you can update or delete record for {round_name} here''', icon='*️⃣') 

    with st.form(key='from2'):
        start_date = st.date_input('start_date', date.today())
        end_date = st.date_input('end_date', date.today() + timedelta(days=7))
        submit_button_update = st.form_submit_button(label='update')  
        submit_button_delete = st.form_submit_button(label='delete') 

    if submit_button_update:
        if start_date < end_date:
            crud_rounds(round_name, start_date, end_date, 'update')
            crud_rounds(round_name, None, None, 'select') 
        else:
             st.warning(f'''start_date is greater than end_date''', icon='⚠️') 
       
    if submit_button_delete:
        crud_rounds(round_name, None, None, 'delete')
        st.session_state['round_name'] = round_name
        st.experimental_rerun()
        
    if 'round_name' in st.session_state:
        round_name = st.session_state['round_name']
        st.success(f'record deleted for {round_name}', icon='✅')
        del st.session_state['round_name']

#####
page = st.sidebar.radio('page',('data','insights'))


if page == 'data':

    radio_btn = st.sidebar.radio('table',('facts','candidates','rounds'))
    download_btn(radio_btn)

    if radio_btn == 'facts':
        facts()

    elif radio_btn == 'candidates':
        candidates()  

    elif radio_btn == 'rounds':
        rounds()  


elif page == 'insights':

    radio_btn = st.sidebar.radio('comparison',('peer','self'))

    candidate_name = records_ls('candidate_name','candidates')
    round_name = records_ls('round_name','rounds')
    return_obj = crud_facts(candidate_name, round_name, None, 'select')

    if return_obj is None:
        st.warning(f'''no record exists for {candidate_name} {round_name}''' , icon='⚠️') 

    else:
        sliced_df = sliced_df('round_name' if radio_btn == 'peer' else 'candidate_name',round_name if radio_btn == 'peer' else candidate_name,radio_btn)

        piechart(return_obj)

        st.title('peer comparison' if radio_btn == 'peer' else 'self comparison')
        st.table(sliced_df)
        
        overall_avg_piechart(sliced_df,round_name if radio_btn == 'peer' else candidate_name)
        stacked_barchart(sliced_df,round_name if radio_btn == 'peer' else candidate_name,'candidate_name' if radio_btn == 'peer' else 'round_name')
        individual_barcharts(sliced_df,candidate_name if radio_btn == 'peer' else round_name,'candidate_name' if radio_btn == 'peer' else 'round_name')
