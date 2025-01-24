import streamlit as st
import google.generativeai as genai
import os
import PyPDF2 as pdf
from dotenv import load_dotenv
import json

# Load environment variables for secure key management
load_dotenv()

# Configure Google Generative AI with an API key from the environment
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to query Gemini Pro for resume evaluation
def analyze_resume_with_gemini(input_data):
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(input_data)
        return response.text
    except Exception as e:
        return f"Error in processing the request: {str(e)}"

# Function to extract text from uploaded PDF resumes
def extract_text_from_pdf(file):
    try:
        reader = pdf.PdfReader(file)
        return ''.join(page.extract_text() for page in reader.pages if page)
    except Exception as e:
        return f"Failed to extract text: {str(e)}"

# Prompt template for evaluating resumes
prompt_template = """
Act as an advanced ATS (Application Tracking System) expert with a deep understanding of software engineering, data science, and analytics. 
Your job is to evaluate resumes against job descriptions, assign a skill match percentage, identify gaps, and suggest actionable improvements. 
Provide the response in this format: {{"Skill Match":"%","Gaps":[],"Summary":""}}.

Resume Content: {resume_text}
Job Description: {job_description}
"""

# Streamlit UI for the app
st.title("Next-Gen AI Resume Evaluator")
st.text("Supercharge your resume with AI-driven insights!")

# User inputs: job description and resume file
job_description = st.text_area("Enter the Job Description")
uploaded_resume = st.file_uploader("Upload Your Resume (PDF only)", type="pdf", help="Upload your resume as a PDF")

# Button to initiate processing
if st.button("Analyze Resume"):
    if uploaded_resume and job_description:
        resume_text = extract_text_from_pdf(uploaded_resume)
        if not resume_text.startswith("Failed to extract"):
            # Prepare and send the prompt
            formatted_prompt = prompt_template.format(resume_text=resume_text, job_description=job_description)
            analysis_result = analyze_resume_with_gemini(formatted_prompt)
            st.subheader("Evaluation Results")
            st.text(analysis_result)
        else:
            st.error(resume_text)
    else:
        st.warning("Please upload a resume and provide a job description.")
