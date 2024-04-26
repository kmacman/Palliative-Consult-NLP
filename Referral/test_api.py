from api import app
from fastapi.testclient import TestClient
import pandas as pd
from referral.ExtractReason import EntExtraction
from referral.ExtractProblem import ProbExtraction


client = TestClient(app)

def test_analyze_text():
    response = client.post("/analyze", json={"text": "25 y/o male hx of heart failure, dyspnea, GOC. Needs support."})
    assert response.status_code == 200
    assert response.json() == {"reason_code_1": 1,
            "reason_code_2": 2,
            "reason_code_3": 3,
            "primary_diagnosis_code": 3,
            "primary_diagnosis_text": "cardiovascular"}

def test_reason_extract():
    text = "25 y/o male hx of heart failure, dyspnea, GOC. Needs support."
    rsn = EntExtraction(text)
    assert rsn.get_reason_codes() == [1, 2, 3]

def test_reason_extract_none():
    text = ""
    rsn = EntExtraction(text)
    assert rsn.get_reason_codes() == [4, pd.NA, pd.NA]

def test_problem_extract():
    text = "25 y/o male hx of heart failure, dyspnea, GOC. Needs support."
    prob = ProbExtraction(text)
    assert prob.get_problem_code() == 3