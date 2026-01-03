import streamlit as st
import pandas as pd
df = pd.read_csv('startup_cleaned.csv')
# st.dataframe(df)
df['investors'] = df['investors'].fillna('Undisclosed')
st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Invester'])

if option == 'Overall Analysis':
    st.title('Overall Analysis')
elif option == 'Startup':
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup details')
    st.title('Startup Funding Analysis')
else:
    st.sidebar.selectbox('Select Investors',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor details')
    st.title('Investor Analysis')
