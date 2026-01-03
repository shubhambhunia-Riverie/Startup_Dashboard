import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt   # For plot graph
st.set_page_config(layout='wide',page_title = 'Startup Analytics',page_icon='Wallpaper.png')  # For making the layout wider
df = pd.read_csv('startup_cleaned.csv')
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
