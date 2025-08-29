from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd

# Load pipeline + output mapping
pipeline = joblib.load("course_recommender.pkl")

output_map = {
    0: "Business Analytics (part-time)",
    1: "Data Science and AI (full-time)",
    2: "Data Analytics + Machine Learning (part-time)",
    4: "Data Science (part-time)"   # new label
}

# Define request schema
class StudentProfile(BaseModel):
    Age: int
    High_School_GPA: float
    University_GPA: float
    Soft_Skills_Score: float
    Networking_Score: float
    Starting_Salary: float
    Gender: str
    Field_of_Study: str
    Internships_Completed: int
    Certifications: int
    Job_Offers: int
    Current_Job_Level: str

# Initialize FastAPI app
app = FastAPI(title="Course Recommendation API")

@app.post("/predict")
def predict_course(student: StudentProfile):
    # Convert input to DataFrame
    student_df = pd.DataFrame([student.dict()])

    # Predict cluster
    pred_label = pipeline.predict(student_df)[0]

    # Apply special rule
    if student.Field_of_Study == "Computer Science" and pred_label == 0:
        pred_label = 4

    # Map to recommendation
    recommendation = output_map[pred_label]

    return {
        "prediction_label": int(pred_label),
        "recommended_course": recommendation
    }