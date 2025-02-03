import streamlit as st
import os
import random
import string
import json

# Set the title of the app
st.title("📁 File Sharing Application")

# Ensure the uploads directory exists
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Load the file code mapping from a JSON file
mapping_file = "file_code_mapping.json"
if os.path.exists(mapping_file):
    with open(mapping_file, "r") as f:
        file_code_mapping = json.load(f)
else:
    file_code_mapping = {}

# Function to generate a unique 4-digit code
def generate_code():
    return ''.join(random.choices(string.digits, k=4))

# Create two columns for upload and download sections
col1, col2 = st.columns(2)

# File upload section
with col1:
    st.header("Upload File")
    uploaded_file = st.file_uploader("Choose a file to upload")
    
    if uploaded_file is not None:
        # Save the uploaded file to the local directory
        file_path = os.path.join("uploads", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Generate a unique 4-digit code
        code = generate_code()
        while code in file_code_mapping:
            code = generate_code()
        
        # Store the mapping between the code and the file name
        file_code_mapping[code] = uploaded_file.name
        
        # Save the updated mapping to the JSON file
        with open(mapping_file, "w") as f:
            json.dump(file_code_mapping, f)
        
        st.success(f"File uploaded successfully! Your code is: {code}")

# File download section
with col2:
    st.header("Download File")
    code_input = st.text_input("Enter the 4-digit code")
    
    if st.button("Download"):
        if code_input in file_code_mapping:
            file_name = file_code_mapping[code_input]
            file_path = os.path.join("uploads", file_name)
            
            with open(file_path, "rb") as f:
                st.download_button(label="Download File", data=f, file_name=file_name)
        else:
            st.error("Invalid code. Please try again.")