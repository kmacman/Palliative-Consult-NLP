from medspacy.preprocess import PreprocessingRule, Preprocessor



preprocess_rules = [
    PreprocessingRule(
        r"\d{2}/\d{2}/\d{2} \d{1,2}:\d{2}:\d{2} (EST|EDT)",
        repl="",
        desc="Remove date and time from consult questions"
    ),
    
    PreprocessingRule(
        r"\[\*\*[\d]{4}\*\*\]",
        repl="2010",
        desc="Replace MIMIC year brackets with a generic year."
    ),

    PreprocessingRule(
        "Consult-Follow-Up Until Problem Resolved,",
        repl="",
        desc="Remove 'Consult-Follow-Up Until Problem Resolved,' from docs"
    ),

    PreprocessingRule(
        "Single Consultation-No Follow-Up,",
        repl="",
        desc="Remove 'Single Consultation-No Follow-Up,' from docs"
    ),

    PreprocessingRule(
        "Consultation,",
        repl="",
        desc="Remove 'Consultation,' from docs"
    ),

        PreprocessingRule(
        "Reason:",
        repl="",
        desc="Remove 'Reason:' from docs"
    ),
    
    PreprocessingRule(
        "dx'd", 
        repl="Diagnosed", 
        desc="Replace abbreviation"
    ),

    PreprocessingRule(
        "can't", 
        repl="cannot", 
        desc="Replace contraction"
    ),

    PreprocessingRule(
        "cant", 
        repl="cannot", 
        desc="Replace contraction"
    ),
    
    PreprocessingRule(
        "tx'd", 
        repl="Treated", 
        desc="Replace abbreviation"
    ),
    
        PreprocessingRule(
        "\[\*\*[^\]]+\]", 
        desc="Remove all other bracketed placeholder text from MIMIC"
    )
]

