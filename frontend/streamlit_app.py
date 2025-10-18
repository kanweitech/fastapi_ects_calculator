import streamlit as st
import requests
import os

st.set_page_config(page_title="ECTS Calculator", layout="centered")


BACKEND_URL = os.environ.get("BACKEND_URL", "https://fastapi-ects-calculator.onrender.com/")
CALCULATE_ENDPOINT = BACKEND_URL.rstrip("/") + "/calculate"

st.title("ECTS Calculator")
with st.form("ects_form"):
    st.write("Enter your program details")
    masters_program_academic_year = st.number_input("ECTS per Academic Year", min_value=1.0)
    number_of_years_of_bachelor_study = st.number_input("Years of Bachelor Study", min_value=1.0)
    total_number_of_units = st.number_input("Total Number of Units", min_value=1.0)
    name_of_course = st.text_input("Course Name")
    accumulated_units = st.number_input("Accumulated Units", min_value=0.0)
    submitted = st.form_submit_button("Calculate ECTS")
    if submitted:
    payload = {
            "masters_program_academic_year": masters_program_academic_year,
            "number_of_years_of_bachelor_study": number_of_years_of_bachelor_study,
            "total_number_of_units": total_number_of_units,
            "name_of_course_you_want_to_calculate": name_of_course,
            "Accumulated_units": accumulated_units
    }
    try:
        with st.spinner("Calculating..."):
            r = requests.post(CALCULATE_ENDPOINT, json=payload, timeout=10)
        if r.status_code == 200:
            data = r.json()
            st.success(f"{name_of_course} — {data['ECTS']} ECTS (conversion factor: {data['conversion_factor']})")
            st.write("**Request sent:**")
            st.json(payload)
            st.write("**Response:**")
            st.json(data)

        else:
            # show server error details if available
            try:
                detail = r.json().get('detail')
            except Exception:
                detail = r.text
            st.error(f"Server returned {r.status_code}: {detail}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error contacting backend: {e}")

