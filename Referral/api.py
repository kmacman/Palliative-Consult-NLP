import sys
sys.path.append('\classes')  
sys.path.append('\data_processing')  

from fastapi import FastAPI
from pydantic import BaseModel
from classes.ExtractProblem import ProbExtraction
from classes.ExtractReason import EntExtraction 


app = FastAPI()
class TextData(BaseModel):
    text: str

@app.post("/analyze")
def analyze_text(data: TextData):
    reasons = EntExtraction(data.text).get_reason_codes()
    reason1 = reasons[0]
    reason2 = reasons[1]
    reason3 = reasons[2]
    problem = ProbExtraction(data.text).get_problem_code()
    problem_text = ProbExtraction(data.text)._determine_primary_diagnosis()
    return {"reason_code_1": reason1,
            "reason_code_2": reason2,
            "reason_code_3": reason3,
            "reason_codes_key": "1: symptom, 2: goals, 3: support",
            "primary_diagnosis_code": problem,
            "primary_diagnosis_text": problem_text}

