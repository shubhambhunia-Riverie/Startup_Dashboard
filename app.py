import coerce
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt   # For plot graph

from Streamlit_doc import date

st.set_page_config(layout='wide',page_title = 'Startup Analytics',page_icon='Wallpaper.png')  # For making the layout wider
df = pd.read_csv('startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'],format='mixed',errors = 'coerce')
# st.dataframe(df)
df['investors'] = df['investors'].fillna('Undisclosed')
# Load the selected invester name function
def load_investors_details(investor):
    st.title(investor)
    #Load the recent 5 investment of the investor function
    last5_df = df[df['investors'].str.contains(investor)].head()[['date','startup','vertical','SubVertical','city','round','amount']]
    st.subheader('Most Recent Investment')
    st.dataframe(last5_df)

    col1, col2 = st.columns(2)
    with col1:
        # Biggest Investment
        biggest_inv = df[df['investors'].str.contains(investor)].groupby('startup')['amount'].sum().sort_values(
            ascending=False).head(5)
        st.subheader('Most biggest Investment')
        fig, ax = plt.subplots()
        ax.bar(biggest_inv.index, biggest_inv.values)
        st.pyplot(fig)
    with col2:
        #Biggest investment sectorwise
        biggest_sec = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum().sort_values(
            ascending=False).head(5)
        st.subheader('Biggest Investment sectorwise')
        fig1 , ax1 = plt.subplots()
        ax1.bar(biggest_sec.index, biggest_sec.values)
        st.pyplot(fig1)
    col1,col2 = st.columns(2)
    with col1:
        fig, ax = plt.subplots()
        # Pie plot for Sectorwise investment
        vertical_series = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum().sort_values(ascending = False).head()
        st.subheader('Sector wise Investment')
        fig2,ax2 = plt.subplots()
        ax2.pie(vertical_series,labels=vertical_series.index,autopct='%1.1f%%')
        st.pyplot(fig2)
    with col2:
        # Pie plot for roundwise investment
        round_series = df[df['investors'].str.contains(investor)].groupby('round')['amount'].sum().sort_values(ascending = False).head()
        st.subheader('Round wise Investment')
        fig3,ax3 = plt.subplots()
        ax3.pie(round_series,labels=round_series.index,autopct='%1.1f%%')
        st.pyplot(fig3)

    col1,col2 = st.columns(2)
    with col1:
        # Pie plot for city investment
        city_series = df[df['investors'].str.contains(investor)].groupby('city')['amount'].sum().sort_values(
            ascending=False).head()
        st.subheader('City wise Investment')
        fig4, ax4 = plt.subplots()
        ax4.pie(city_series, labels=city_series.index, autopct='%1.1f%%')
        st.pyplot(fig4)
    with col2:
        #year on year investment growth
        df['year'] = df['date'].dt.year
        year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
        st.subheader('Year wise Investment')
        fig5, ax5 = plt.subplots()
        ax5.plot(year_series.index,year_series.values)
        st.pyplot(fig5)




st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Invester'])

if option == 'Overall Analysis':
    st.title('Overall Analysis')
elif option == 'Startup':
    st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup details')
    st.title('Startup Funding Analysis')
else:
    selected_investors = st.sidebar.selectbox('Select Investors',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor details')

    if btn2:
        load_investors_details(selected_investors)
    #st.title('Investor Analysis')
