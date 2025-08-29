# Course Recommendation System
An intelligent course recommendation system that uses machine learning to suggest the most suitable courses based on student profiles. The system combines a FastAPI backend with a beautiful Streamlit frontend to provide personalized course recommendations.

## Features
Intelligent Recommendations: ML-powered course suggestions based on comprehensive student profiles
Interactive Frontend: User-friendly Streamlit interface with real-time visualizations
RESTful API: FastAPI backend for scalable and efficient predictions
Visual Analytics: Profile analysis with charts and metrics
Comprehensive Profiling: 12 different factors including academics, skills, and experience

## Available Courses
- Business Analytics (part-time)
- Data Science and AI (full-time)
- Data Analytics + Machine Learning (part-time)
- Data Science (part-time)

## Student Profile Features
Feature	Type	Range/Categories
Age	Numerical	18 – 70 years
High School GPA	Numerical	0 – 10 (rescaled)
University GPA	Numerical	0 – 10 (rescaled)
Internships Completed	Binary	0 = No, 1 = Yes
Certifications	Binary	0 = No, 1 = Yes
Soft Skills Score	Numerical	5 – 10
Networking Score	Numerical	4 – 9
Job Offers	Binary	0 = No, 1 = Yes
Starting Salary	Numerical	0 – 69,860
Field of Study	Categorical	Computer Science, Business/Finance, Medical/Bio, Engineering, Arts, Education, Law, Marketing
Current Job Level	Categorical	NA, Entry, Mid, Senior
Gender	Categorical	Male, Female

## Quick Start
Prerequisites
Python 3.8 or higher
pip package manager
Installation
Clone the repository
bash
git clone <your-repo-url>
cd course-recommendation-system
Install dependencies
bash
pip install -r requirements.txt
Prepare your model
Ensure you have course_recommender.pkl in the project root directory
This should be your trained scikit-learn pipeline
Running the Application
Option 1: Run Both Services Locally
Start the FastAPI backend
bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
In a new terminal, start the Streamlit frontend
bash
streamlit run streamlit_app.py
Access the application
API Documentation: http://localhost:8000/docs
Streamlit Interface: http://localhost:8501
Option 2: Run API Only
bash
uvicorn main:app --reload
Then test the API using curl or any API client:

bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "Age": 25,
       "High_School_GPA": 8.5,
       "University_GPA": 7.8,
       "Soft_Skills_Score": 8.2,
       "Networking_Score": 7.0,
       "Starting_Salary": 45000,
       "Gender": "Male",
       "Field_of_Study": "Computer Science",
       "Internships_Completed": 1,
       "Certifications": 1,
       "Job_Offers": 1,
       "Current_Job_Level": "Entry"
     }'
     
## Project Structure
course-recommendation-system/
├── main.py                 # FastAPI backend application
├── front.py        # Streamlit frontend application
├── course_recommender.pkl  # Trained ML model (you need to provide this)
├── requirements.txt        # Python dependencies
├── render.yaml            # Render.com deployment configuration
├── README.md              # Project documentation


## API Endpoints
POST /predict
Predicts the most suitable course for a student based on their profile.

Request Body:

json
{
  "Age": 25,
  "High_School_GPA": 8.5,
  "University_GPA": 7.8,
  "Soft_Skills_Score": 8.2,
  "Networking_Score": 7.0,
  "Starting_Salary": 45000,
  "Gender": "Male",
  "Field_of_Study": "Computer Science",
  "Internships_Completed": 1,
  "Certifications": 1,
  "Job_Offers": 1,
  "Current_Job_Level": "Entry"
}
Response:

json
{
  "prediction_label": 4,
  "recommended_course": "Data Science (part-time)"
}

## Frontend Features
The Streamlit frontend provides:

Interactive Form: Easy-to-use input fields with validation
Visual Analytics:
Profile strength overview bar chart
Comprehensive radar chart analysis
Key metrics display
Real-time Feedback: Immediate visual updates as you input data
Responsive Design: Works on desktop and mobile devices
Error Handling: Clear error messages and connection status

### Deployment
Deploy to Render.com
Fork/Clone this repository
Connect your GitHub repository to Render
Create a new Web Service
Use the provided render.yaml configuration
Make sure to upload your course_recommender.pkl file
Deploy to Other Platforms

Built with ❤️ using FastAPI and Streamlit

