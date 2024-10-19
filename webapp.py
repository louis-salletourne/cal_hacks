import streamlit as st
import PyPDF2
import json
import os
from pdf.export_missing_fields import export_missing_fields
import tempfile
from email_read import read_email

# JSON file path
json_file_path = "user_profile.json"

# Initialize or load the JSON file
def load_json():
    if not os.path.exists(json_file_path):
        return {}
    with open(json_file_path, 'r') as f:
        return json.load(f)

# Save the updated JSON data
def save_json(data):
    with open(json_file_path, 'w') as f:
        json.dump(data, f, indent=4)

# Dummy function to simulate extraction of information from PDF


# Main Streamlit app
def main():
    output = read_email()
    st.title("PDF Info Extractor")
    st.write("Upload a PDF file and I'll extract information, then fill in the missing details.")
    print(output)
    attachments = output['Attachments']
    if not attachments:
        st.write("No attachments found.")
        return
    path = attachments[0]
    st.write("Saved attachment:", path)

    # Load current user profile
    user_profile = load_json()

    # Display current user profile
    if user_profile:
        st.subheader("Current User Profile")
        st.json(user_profile)
    else:
        st.write("No user profile found.")
    extracted_info = export_missing_fields(path)
    st.write(extracted_info)

    # Display extracted information and find missing information
    st.subheader("Extracted Information")
    missing_info = {}
    user_inputs = {}

    for key, value in extracted_info.items():
        if key not in user_profile or user_profile[key] is None:
            if value is None:
                # Create text input for missing information
                user_inputs[key] = st.text_input(f"Please provide your {key.replace('_', ' ').capitalize()}:")
            else:
                st.write(f"{key.replace('_', ' ').capitalize()}: {value}")
        else:
            st.write(f"{key.replace('_', ' ').capitalize()}: {user_profile[key]}")

    # Submit button to update missing information
    if st.button("Submit"):
        for key, user_input in user_inputs.items():
            if user_input:
                user_profile[key] = user_input
        save_json(user_profile)

        st.success("User profile updated successfully!")
        st.json(user_profile)
    

# Run the app
if __name__ == "__main__":
    main()
