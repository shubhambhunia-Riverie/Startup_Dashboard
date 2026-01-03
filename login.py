import streamlit as st
email = st.text_input('Enter Email')
password = st.text_input('Enter Password')

gender = st.selectbox('Select gender',['Male','Female','Other'])
age = st.number_input('Enter Age')
btn = st.button('Submit')

if btn:
    if email == 'Shubhambhunia04@gmail.com' and password == '740717':
        st.success('Email Submitted')
        st.balloons()
        st.write(gender)
    else:
        st.error('Login Failed')





