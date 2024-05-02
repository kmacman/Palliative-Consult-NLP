import spacy
import medspacy
from App.data_processing.preprocessor import preprocess_rules, Preprocessor
from App.data_processing.context_rules import ConText, context_rules
from medspacy.section_detection import Sectionizer
from App.data_processing.postprocessing import postprocess_rules, Postprocessor
from medspacy.visualization import visualize_ent, visualize_dep
import re
import pandas as pd


from .target_rules import target_rules # Import the target rules from the target_rules.py file


nlp = medspacy.load() # Load the medspacy model

#Add preprocessor to pipeline
preprocessor = Preprocessor(nlp.tokenizer)
preprocessor.add(preprocess_rules)
nlp.tokenizer = preprocessor

#Add target matcher rules
target_matcher = nlp.get_pipe("medspacy_target_matcher") # Add the target matcher to the pipeline
target_matcher.add(target_rules) # Add the target rules to the target matcher

#Add Context Rules
context = nlp.get_pipe("medspacy_context") # Add the context to the pipeline
context.add(context_rules)

#Add section detection? Holding off for now, not needed for current project


#Add Postprocessing Rules
#postprocessor = nlp.add_pipe("medspacy_postprocessor", config={"debug": False})
#postprocessor.add(postprocess_rules)

#Defining the data loading function
def load_xls(file_path, consult_column="consult_question"):
    """
    Load an excel file into a pandas dataframe
    """
    df = pd.read_excel(file_path)
    dfcq = df[consult_column]
    return df, dfcq
