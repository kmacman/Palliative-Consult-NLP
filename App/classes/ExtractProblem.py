from medspacy.io import DocConsumer
from App.data_processing.processing import nlp
import pandas as pd
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the DocConsumer
doc_consumer = DocConsumer(nlp, dtypes=("ents", "doc"), 
                            dtype_attrs={
                                "ents": [
                                    "text",
                                    "label_",
                                    "problem_type",
                                    "treatment_type",
                                    "is_negated",
                                    "is_uncertain",
                                    "is_historical",
                                    "is_hypothetical",
                                    "is_family",
                                    
                                ],
                                "doc":
                                ["text", 
                                 #"report_title"
                                 ]
                                
                            }
)

#Establish problem heirarchy

class ProbExtraction:
    def __init__(self, text):
        try:
            self.doc = nlp(text)
            self.extracted_categories = self._extract_categories()
        except Exception as e:
            logger.error(f"An error occurred during NLP processing: {e}")
            self.doc = nlp('')
            self.extracted_categories = self._extract_categories()

    def _consume_document(self):
        """Converts NLP doc to a DataFrame using DocConsumer."""
        dc = doc_consumer(self.doc)
        return dc._.to_dataframe()

    def _extract_categories(self):
        """Extracts categories from the NLP processed document."""
        dcdf = self._consume_document()
        return dcdf['problem_type']
    
    def _determine_primary_diagnosis(self):
        diagnosis_heirarchy = ['cancer_heme', 'cancer_solid', 'cardiovascular','renal','infectious','pulmonary','trauma','gastrointestinal','hepatology','dementia','neurology','vascular','met_end','genetic','hematology','premature','fetal','unknown']
        for diagnosis in diagnosis_heirarchy:
            if diagnosis in self.extracted_categories.values:
                return diagnosis
        return 'unknown'
    
    def get_problem_code(self):
        """Determines problem codes based on the extracted categories."""
        primary_diagnosis = self._determine_primary_diagnosis()
        codes = {'cancer_solid': 1, 'cancer_heme': 2, 'infectious': 10, 'cardiovascular': 3, 'renal': 7,  'pulmonary': 4, 'trauma': 11, 'gastrointestinal': 5, 'hepatology': 6, 'dementia': 8, 'neurology': 9, 'vascular': 12, 'met_end': 13, 'genetic': 14, 'hematology': 15, 'premature': 16, 'fetal': 17, 'unknown': 99}
        # Map categories to codes
        return codes[primary_diagnosis]

        # Testing methods
    def show_doc(self):
        """Prints the text of the NLP processed document."""
        try:
            print(self.doc.text)
        except AttributeError:
            logger.error("NLP document is not initialized properly.")

    def show_dcdf(self):
        """Displays the DataFrame created by DocConsumer."""
        return self._consume_document().head(10)

    def show_categories(self):
        """Displays the extracted categories."""
        return self.extracted_categories

    def show_primary(self):
        """Displays the extracted categories."""
        return self._determine_primary_diagnosis()