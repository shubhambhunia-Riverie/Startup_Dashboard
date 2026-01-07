
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt   # For plot graph



st.set_page_config(layout='wide',page_title = 'Startup Analytics',page_icon='Content/Wallpaper.png')  # For making the layout wider
df = pd.read_csv('Content/startup_cleaned.csv')
df['date'] = pd.to_datetime(df['date'],format='mixed',errors = 'coerce')
df.set_index('Sr No',inplace = True)
# st.dataframe(df)
df['investors'] = df['investors'].fillna('Undisclosed')
st.title('Warning--Now on Development Phase')

def load_startup_analysis(startup):
    #st.title(startup)
    st.markdown(
        f"<h1 style='text-align: center; margin-bottom: 0;'>{startup}</h1>",
        unsafe_allow_html=True
    )
    st.divider()
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        # Which city based startup
        city = df[df['startup'] == startup]['city'].values[0]
        st.markdown("### Founded In")
        st.write(city)
    with col2:
        # Sector of the startup
        sector = df[df['startup'] == startup]['vertical'].values[0]
        st.markdown("### Sector")
        st.write(sector)

    with col3:
        # Subsector of the startup
        subsector = df[df['startup'] == startup]['SubVertical'].values[0]
        st.markdown("### Sub Sector")
        st.write(subsector if pd.notna(subsector) else "Not available")
    with col4:
        # Total funding got
        funding = df.groupby('startup')['amount'].sum().sort_values(ascending = False)[startup]
        st.markdown("### Funding Raised")
        st.markdown(f"#### {funding} Cr")
    st.divider()
    st.markdown(
        f"<h1 style='text-align: center; margin-bottom: 0;'>{'Funding Partners'}</h1>",
        unsafe_allow_html=True
    )
    st.dataframe(df[df['startup'] == startup][['investors','amount','round','year']])






def load_overall_analysis():

    #st.title('Overall Analysis')
    st.markdown(
        f"<h1 style='text-align: center; margin-bottom: 0;'>{'Overall Analysis'}</h1>",
        unsafe_allow_html=True
    )
    st.divider()
    col1,col2,col3,col4 = st.columns(4)
    with col1:
        # Total investment amount
        total_inv = df['amount'].sum()
        st.metric('Total Investment', str(int(total_inv)) + ' Cr')
    with col2:
        # MAx amount infused in a startup
        max_inv = df.groupby('startup')['amount'].max().sort_values(ascending=False).head(1).values[0]
        st.metric('Maximum Investment in a single startup', str(int(max_inv)) + ' Cr')
    with col3:
        # Average investment
        avg_inv = df.groupby('startup')['amount'].sum().mean()
        st.metric('Average Investment', str(round(avg_inv)) + ' Cr')
    with col4:
        # Total funded Startup
        total_startup = df['startup'].nunique()
        st.metric('Total funded Startups', str(total_startup))

    st.header('Monthly Investment graph')


    selected_option = st.selectbox('Select Type',['Total','Count'])
    df['month'] = df['date'].dt.month
    df['year'] = df['date'].dt.year
    if selected_option == 'Total':
        temp_df = df.groupby(['year', 'month'])['amount'].sum().reset_index()
    else:
        temp_df = df.groupby(['year', 'month'])['amount'].count().reset_index()

    temp_df['x_axis'] = temp_df['month'].astype('str') + '-' + temp_df['year'].astype('str')
    fig6, ax6 = plt.subplots()
    ax6.plot(temp_df['x_axis'], temp_df['amount'])
    st.pyplot(fig6)





# Load the selected investor name function
def load_investors_details(investor):
    #st.title(investor)
    st.markdown(
        f"<h1 style='text-align: center; margin-bottom: 0;'>{investor}</h1>",
        unsafe_allow_html=True
    )
    st.divider()
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
        #Biggest investment sector wise
        biggest_sec = df[df['investors'].str.contains(investor)].groupby('vertical')['amount'].sum().sort_values(
            ascending=False).head(5)
        st.subheader('Biggest Investment sector wise')
        fig1 , ax1 = plt.subplots()
        ax1.bar(biggest_sec.index, biggest_sec.values)
        st.pyplot(fig1)
    col1,col2 = st.columns(2)
    with col1:
        # Pie plot for Sector wise investment
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
        #year-on-year investment growth
        df['year'] = df['date'].dt.year
        year_series = df[df['investors'].str.contains(investor)].groupby('year')['amount'].sum()
        st.subheader('Year wise Investment')
        fig5, ax5 = plt.subplots()
        ax5.plot(year_series.index,year_series.values)
        st.pyplot(fig5)




st.sidebar.title('Startup Funding Analysis')
option = st.sidebar.selectbox('Select One',['Overall Analysis','Startup','Investor'])

if option == 'Overall Analysis':
    load_overall_analysis()

elif option == 'Startup':
    selected_startup = st.sidebar.selectbox('Select Startup',sorted(df['startup'].unique().tolist()))
    btn1 = st.sidebar.button('Find Startup details')

    if btn1:
        load_startup_analysis(selected_startup)
else:
    selected_investors = st.sidebar.selectbox('Select Investors',sorted(set(df['investors'].str.split(',').sum())))
    btn2 = st.sidebar.button('Find Investor details')

    if btn2:
        load_investors_details(selected_investors)
    #st.title('Investor Analysis')
