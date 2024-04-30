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

class EntExtraction:
    def __init__(self, text):
        try:
            self.doc = nlp(text)
        except Exception as e:
            logger.error(f"An error occurred during NLP processing: {e}")
            self.doc = nlp('')

    def _consume_document(self):
        """Converts NLP doc to a DataFrame using DocConsumer."""
        dc = doc_consumer(self.doc)
        return dc._.to_dataframe()

    def _extract_categories(self):
        """Extracts categories from the NLP processed document."""
        dcdf = self._consume_document()
        return dcdf['treatment_type']

    def get_reason_codes(self):
        """Determines reason codes based on the extracted categories."""
        categories = self._extract_categories()
        codes = []
        # Map categories to codes
        if 'symptom' in categories.values:
            codes.append(1)  
        if 'goals' in categories.values:
            codes.append(2)
        if 'support' in categories.values:
            codes.append(3)
        # Fill remaining slots with NaN or default values
        while len(codes) < 3:
            codes.append(pd.NA)  # or some default value
        #if codes contains nothing but nan, then set the first value to 4
        if all([pd.isnull(code) for code in codes]):
            codes[0] = 4
        return codes[:3]  # Ensure only three codes are returned

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
        return self._extract_categories()