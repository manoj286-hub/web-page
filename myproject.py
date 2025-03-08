import streamlit as st;
import time;

st.markdown("# My Application")
st.markdown("## Created by Manoj")
st.markdown("### This is a general application app")

Name = st.text_input("Enter your name: ")
st.write(f"Your name is {Name} as per you entered")

Age = st.slider("Select your age", min_value=1, max_value=150)
st.write(f"Your age is {Age}")

Email_Id=st.text_input("Enter your E_mail-Id :")
st.write(f"Your E_mail-Id : ,{Email_Id}")

Gender = st.radio("Select your gender:", ["Male", "Female", "Other"])
st.write(f"You selected **{Gender}**")

Qualification = st.radio("Select your qualification:", ["Below SSLC", "SSLC", "PUC", "Degree", "PG Degree"])
st.write(f"You selected **{Qualification}**")

Family=st.radio("Select your close family member:",["Manoj","Girija","Deepa","Sudeep","Baby","Narayana","Somayya"])
st.write(f"You selected person is **{Family}**")
Relation=st.text_input("Enter your relation with them")
st.write(f"Your relation with them is **{Relation}")

Id = st.radio("Select your Id proof:", ["Aadhar_card", "Pan_card", "Voter_Id", "Passport", "Driving_licence"])

if Id == "Aadhar_card":
    num = st.text_input("Enter your Aadhar number: ")
    st.write(f"Aadhar card number: {num}")
    num_file=st.file_uploader("Uploade Aadhar file",type=["txt","csv","png","jpg","pdg"])
    st.write("You successfully uploaded")
elif Id == "Pan_card":
    num = st.text_input("Enter your Pan number: ")
    st.write(f"Pan card number: {num}")
    pan_file=st.file_uploader("Uploade Pan card file",type=["txt","csv","png","jpg","pdg"])
    st.write("You successfully uploaded")
elif Id == "Voter_Id":
    num = st.text_input("Enter your Voter Id number: ")
    st.write(f"Voter id number: {num}")
    vote_file=st.file_uploader("Uploade Voter Id file",type=["txt","csv","png","jpg","pdg"])
    st.write("You successfully uploaded")
elif Id == "Passport":
    num = st.text_input("Enter your Passport number: ")
    st.write(f"Passport number: {num}")
    pass_file=st.file_uploader("Uploade Passport file",type=["txt","csv","png","jpg","pdg"])
    st.write("You successfully uploaded")
else:
    num = st.text_input("Enter your Driving licence number: ")
    st.write(f"Driving licence number: {num}")
    dri_file=st.file_uploader("Uploade Driving licence file",type=["txt","csv","png","jpg","pdg"])
    st.write("You successfully uploaded")

st.markdown("##Your details given below :")
st.write(f"Your name :,{Name} ")
st.write(f"Your age :,{Age} ")
st.write(f"Your E_mail-Id :,{Email_Id} ")
st.write(f"Your gender :,{Gender} ")
st.write(f"Your qualification :,{Qualification} ")
st.write(f"Your given Id details :,{Id} ")
st.write(f"Your number :,{num} ")



check = st.checkbox("I agree to the terms and conditions")
if check:
    st.write("You have agreed to the terms and conditions.")
else:
    st.write("You must agree to the terms and conditions to submit the form.")

Button = st.button("Submit")
if Button and check:
    st.title("Processing")
    with st.spinner("Data is Fetching..."):
        time.sleep(5)
    st.success("Task completed")
    st.write("## You successfully filled the application.")
    st.markdown("# Thank you!")
    st.write("**************************************************************************************************************************")
else:
    if Button and not check:
        st.warning("You must agree to the terms and conditions before submitting.")
 


        
         









