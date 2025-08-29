import streamlit as st
import requests
import json
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Course Recommendation System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .result-box {
        background-color: #e8f5e8;
        padding: 1.5rem;
        border-radius: 0.5rem;
        border: 2px solid #28a745;
        margin: 1rem 0;
        text-align: center;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 2px solid #dc3545;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Main title
st.markdown('<h1 class="main-header">🎓 Course Recommendation System</h1>', unsafe_allow_html=True)

# API endpoint configuration
API_URL = "https://course-recommender-backend-yrfa.onrender.com"

# Create two columns for layout
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<h2 class="sub-header">📝Enter Your Profile Information</h2>', unsafe_allow_html=True)
    
    # Create tabs for better organization
    tab1, tab2, tab3 = st.tabs(["Personal Info", "Academic Background", "Professional Experience"])
    
    with tab1:
        st.subheader("Personal Information")
        age = st.slider("Age", min_value=18, max_value=70, value=25, 
                       help="Student's age in years")
        
        gender = st.selectbox("Gender", 
                             options=["Male", "Female"],
                             help="Student's gender")
        
        field_of_study = st.selectbox("Field of Study", 
                                    options=["Computer Science", "Business/Finance", "Medical/Bio", 
                                            "Engineering", "Arts", "Education", "Law", "Marketing"],
                                    help="Academic domain or area of study")
    
    with tab2:
        st.subheader("Academic Performance")
        high_school_gpa = st.slider("High School GPA", min_value=0.0, max_value=10.0, 
                                   value=7.5, step=0.1,
                                   help="High school GPA rescaled to 0-10")
        
        university_gpa = st.slider("University GPA", min_value=0.0, max_value=10.0, 
                                  value=7.5, step=0.1,
                                  help="University GPA rescaled to 0-10")
        
        col_a, col_b = st.columns(2)
        with col_a:
            internships = st.selectbox("Have you Completed any Internships", 
                                     options=[0, 1], 
                                     format_func=lambda x: "Yes" if x == 1 else "No",
                                     help="Whether student has completed internships")
        
        with col_b:
            certifications = st.selectbox("Do you have any Previous Certifications", 
                                        options=[0, 1], 
                                        format_func=lambda x: "Yes" if x == 1 else "No",
                                        help="Whether student has earned certifications")
    
    with tab3:
        st.subheader("Skills & Professional Experience")
        soft_skills_score = st.slider("Rate your soft skills out of 10", min_value=5.0, max_value=10.0, 
                                     value=7.5, step=0.1,
                                     help="Score for communication, teamwork, leadership, etc.")
        
        networking_score = st.slider("How comfortable are you with networking", min_value=4.0, max_value=9.0, 
                                    value=6.5, step=0.1,
                                    help="Score for networking ability")
        
        col_c, col_d = st.columns(2)
        with col_c:
            job_offers = st.selectbox("Have any previous full-time working experience?", 
                                    options=[0, 1], 
                                    format_func=lambda x: "Yes" if x == 1 else "No",
                                    help="Whether student has received job offers")
        
        with col_d:
            current_job_level = st.selectbox("Current Job Level (select NA if not experienced)", 
                                           options=["NA", "Entry", "Mid", "Senior"],
                                           help="Current job seniority level")
            
        
        starting_salary = st.number_input("Previous/Current Salary (Enter 0 for fresher)", min_value=0, max_value=69860, 
                                        value=35000, step=1000,
                                        help="Previous/Current salary (annual)")
        
        

with col2:
    st.markdown('<h2 class="sub-header"> Profile Summary</h2>', unsafe_allow_html=True)
    
    # Create a visual summary
    summary_data = {
        'Category': ['Academic Performance', 'Professional Skills', 'Experience Level'],
        'Score': [
            (high_school_gpa + university_gpa) / 2,
            (soft_skills_score + networking_score) / 2,
            (internships + certifications + job_offers) * 3.33
        ]
    }
    
    # Display key metrics
    st.metric("Academic Average", f"{(high_school_gpa + university_gpa) / 2:.1f}/10")
    st.metric("Skills Average", f"{(soft_skills_score + networking_score) / 2:.1f}/10")
    st.metric("Experience Points", f"{internships + certifications + job_offers}/3")
    st.markdown('</div>', unsafe_allow_html=True)

# Prediction section
st.markdown('<h2 class="sub-header"> Get Course Recommendation</h2>', unsafe_allow_html=True)

if st.button(" Get Recommendation", type="primary", use_container_width=True):
    # Prepare the data for API call
    student_data = {
        "Age": age,
        "High_School_GPA": high_school_gpa,
        "University_GPA": university_gpa,
        "Soft_Skills_Score": soft_skills_score,
        "Networking_Score": networking_score,
        "Starting_Salary": starting_salary,
        "Gender": gender,
        "Field_of_Study": field_of_study,
        "Internships_Completed": internships,
        "Certifications": certifications,
        "Job_Offers": job_offers,
        "Current_Job_Level": current_job_level
    }
    
    try:
        with st.spinner("Analyzing your profile..."):
            # Make API call
            response = requests.post(API_URL+'/predict', json=student_data, timeout=10)
            
            if response.status_code == 200:
                result = response.json()
                
                # Display result in a beautiful box
                st.markdown(f"""
                ### Recommended Course
                # {result['recommended_course']}
                
                **Prediction Label:** {result['prediction_label']}
                """)
                st.markdown('</div>', unsafe_allow_html=True)
                
                # Show additional insights
                st.markdown("### Recommendation Insights")
                
                col_insight1, col_insight2 = st.columns(2)
                
                with col_insight1:
                    st.info(f"""
                    **Why this recommendation?**
                    
                    Based on your profile:
                    - Field of Study: {field_of_study}
                    - Academic Performance: {(high_school_gpa + university_gpa) / 2:.1f}/10
                    - Professional Readiness: {(soft_skills_score + networking_score) / 2:.1f}/10
                    """)
                
                with col_insight2:
                    # Create a radar chart for profile visualization
                    categories = ['Academic\nPerformance', 'Soft Skills', 'Networking', 
                                'Experience', 'Career\nReadiness']
                    values = [
                        (high_school_gpa + university_gpa) / 2,
                        soft_skills_score,
                        networking_score,
                        (internships + certifications) * 5,
                        (job_offers * 5 + starting_salary / 10000)
                    ]
                    
                    fig_radar = go.Figure()
                    fig_radar.add_trace(go.Scatterpolar(
                        r=values,
                        theta=categories,
                        fill='toself',
                        name='Your Profile'
                    ))
                    fig_radar.update_layout(
                        polar=dict(
                            radialaxis=dict(
                                visible=True,
                                range=[0, 10]
                            )),
                        showlegend=False,
                        title="Profile Analysis",
                        height=300
                    )
                    st.plotly_chart(fig_radar, use_container_width=True)
                
            else:
                st.markdown('<div class="error-box">', unsafe_allow_html=True)
                st.error(f" API Error: {response.status_code}")
                st.write("Response:", response.text)
                st.markdown('</div>', unsafe_allow_html=True)
                
    except requests.exceptions.RequestException as e:
        st.markdown('<div class="error-box">', unsafe_allow_html=True)
        st.error(f" Connection Error: {str(e)}")
        st.write("Please make sure your FastAPI server is running and the URL is correct.")
        st.markdown('</div>', unsafe_allow_html=True)

# Footer with instructions
st.markdown("---")
st.markdown("###  Instructions")
st.markdown("""
**Course Options:**
- Business Analytics (part-time)
- Data Science and AI (full-time)  
- Data Analytics + Machine Learning (part-time)
- Data Science (part-time)
""")

# Sidebar with additional information
with st.sidebar:
    st.markdown("## About This System")
    st.markdown("""
    This course recommendation system uses machine learning to suggest the most suitable course based on:
    
    - **Academic Background**
    - **Professional Skills** 
    - **Career Goals**
    - **Personal Profile**
    
    The system considers various factors including GPA, field of study, internship experience, and career aspirations to provide personalized recommendations.
    """)
    
    st.markdown("## Technical Details")
    st.markdown("""
    - **Backend:** FastAPI with scikit-learn pipeline
    - **Frontend:** Streamlit with interactive visualizations
    - **ML Model:** Clustering-based recommendation system
    - **Features:** 12 input variables for comprehensive profiling
    """)
    
    if st.button("🔄 Reset Form"):
        st.rerun()



