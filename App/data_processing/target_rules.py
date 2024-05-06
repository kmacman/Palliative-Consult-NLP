from medspacy.ner import TargetRule
from spacy.tokens import Span

#TODO: change treatment_type to reason_type?
Span.set_extension("problem_type", default="")
Span.set_extension("treatment_type", default="")

def disambiguate_stage_4(matcher, doc, i, matches):
    match_id, start, end = matches[i] #sets span variables based on the matched entity

    ent = doc[start:end] #Defines ent based on the start + end of the matched entity within the target doc
    surrounding_tokens = doc[start-1:end+4] #defines surrounding tokens

    #looks for specific words in the surrounding tokens to help disambiguate the matched entity
    if any(tok.lower_ in ["cancer","malignant"] for tok in surrounding_tokens):
        ent._.set("problem_type", "cancer_solid")
    elif any(tok.lower_ in ["sacral","wound", "decubitus","decub","ulcer"] for tok in surrounding_tokens):
        ent._.set("problem_type", "met_end")
    elif any(tok.lower_ in ["sarcoid","sarcoidosis","copd","gold"] for tok in surrounding_tokens):
        ent._.set("problem_type", "pulmonary")
    elif any(tok.lower_ in ["ckd"] for tok in surrounding_tokens):
        ent._.set("problem_type", "renal")

    #If none of the above are matched, leaves problem type as unknown
    else:
        ent._.set("problem_type", "unknown")

#TODO: add write in for FTT, weight loss, poor PO intake, etc.? Or make them all met/end?
#TODO: Dysphagia - neurology? Or like above?
#TODO: Add "trump" definitions for serious diagnoses that are likley to be the primary diagnosis?


#reason code rules
symptom_rules = [
    TargetRule("Symptom", "REASON", 
              pattern=[
                  {"LOWER": {"IN": ["symptom","wob","intractible","intractable","mucositis","symptoms","symptomatic","anxiety","anxious","n/v","agitated","existential","depression","pain","nausea","vomiting","sob","dyspnea","pruritus","pruritis","itch","encephalopathy","obstruction","hemorrhage","diarrhea","constipation","hemoptysis","agitation"]}},
              ],
              attributes={"treatment_type": "symptom"}),

    TargetRule("Opioid", "REASON", 
              pattern=[
                    {"LOWER": "n"},
                    {"IS_PUNCT": True, "OP": "?"},  # Optional punctuation
                    {"LOWER": "v"}
                ],
              attributes={"treatment_type": "symptom"}),

    TargetRule("opioids", "REASON", 
              pattern=[
                  {"LOWER": {"IN": ["opioid","opioids","pca","morphine","dilaudid","hydromorphone","fentanyl","oxycodone","oxycontin"]}},
              ],
              attributes={"treatment_type": "symptom"}),
]

goal_rules = [
    TargetRule("Goals of care", "REASON", 
              pattern=[
                  {"LOWER": "goals"},
                  {"LOWER": "of"},
                  {"LOWER": "care"}
              ],
              attributes={"treatment_type": "goals"}),

    TargetRule("withdraw care", "REASON", 
              pattern=[
                  {"LOWER": "withdraw"},
                  {"LOWER": "care"}
              ],
              attributes={"treatment_type": "goals"}),

    TargetRule("family meeting", "REASON", 
              pattern=[
                  {"LOWER": "family"},
                  {"LOWER": "meeting"},
              ],
              attributes={"treatment_type": "goals"}),

    TargetRule("Goals", "REASON", 
              pattern=[
                  {"LOWER": {"IN": ["goc","goals","conversation",'goal',"cmo","hospice","discussion","discussions","decisions","decision","decide","discuss","mdm"]}},
              ],
              attributes={"treatment_type": "goals"}),

    TargetRule("Goals", "REASON", 
              pattern=[
                  {"LOWER": {"IN": ["proxy","hcp","capacity","surrogate","guardian","hcps"]}},
              ],
              attributes={"treatment_type": "goals"}),

    TargetRule("dnr/dni", "REASON", 
              pattern=[
                  {"LOWER": {"IN": ["dnr","dni","molst","cpr","intubation"]}},
              ],
              attributes={"treatment_type": "goals"}),

    TargetRule("not a candidate", "REASON", 
              pattern=[
                  {"LOWER": {"IN": ["not"]}},
                  {"LOWER": {"IN": ["a"]}},
                  {"LOWER": {"IN": ["candidate"]}},
              ],
              attributes={"treatment_type": "goals"}),

    TargetRule("treatment options", "REASON", 
              pattern=[
                  {"LOWER": {"IN": ["treatment"]}},
                  {"LOWER": {"IN": ["options"]}},
              ],
              attributes={"treatment_type": "goals"}),

    TargetRule("code status", "REASON", 
              pattern=[
                  {"LOWER": "code"},
                  {"LOWER": "status"}
              ],
              attributes={"treatment_type": "goals"}),

    TargetRule("care planning", "REASON", 
              pattern=[
                  {"LOWER": "care"},
                  {"LOWER": "planning"}
              ],
              attributes={"treatment_type": "goals"}),

    TargetRule("comfort care", "REASON", 
              pattern=[
                  {"LOWER": "comfort"},
                  {"LOWER": "care"}
              ],
              attributes={"treatment_type": "goals"}),

    TargetRule("full code", "REASON", 
              pattern=[
                  {"LOWER": "full"},
                  {"LOWER": "code"}
              ],
              attributes={"treatment_type": "goals"}),

    TargetRule("decision making", "REASON", 
              pattern=[
                  {"LOWER": "decision"},
                  {"LOWER": "making"}
              ],
              attributes={"treatment_type": "goals"}),

    TargetRule("comfort measures", "REASON", 
              pattern=[
                  {"LOWER": "comfort"},
                  {"LOWER": "measures"}
              ],
              attributes={"treatment_type": "goals"}),

# Specific Treatment Decisions
    TargetRule("trach_peg", "REASON", 
              pattern=[
                  {"LOWER": {"IN": ["peg","trach","tracheostomy"]}},
              ],
              attributes={"treatment_type": "goals"}),

    TargetRule("extubate", "REASON", 
              pattern=[
                  {"LOWER": {"IN": ["extubate"]}},
              ],
              attributes={"treatment_type": "goals"}),

    TargetRule("feeding tube", "REASON", 
              pattern=[
                  {"LOWER": {"IN": ["feeding","ng","og","g"]}},
                  {"LOWER": {"IN": ["tube"]}},
              ],
              attributes={"treatment_type": "goals"}),

    TargetRule("feeding tube", "REASON", 
              pattern=[
                  {"LOWER": {"IN": ["tube"]}},
                  {"LOWER": {"IN": ["feed","feeds","feeding","fed"]}},
              ],
              attributes={"treatment_type": "goals"}),

    TargetRule("transfusion", "REASON", 
              pattern=[
                  {"LOWER": {"IN": ["transfuse","transfusion","transfused"]}},
              ],
              attributes={"treatment_type": "goals"}),

]

support_rules = [
    TargetRule("caregiver fatigue", "REASON", 
              pattern=[
                  {"LOWER": {"IN": ["caregiver"]}},
                  {"LOWER": {"IN": ["fatigue","burnout"]}},
              ],
              attributes={"treatment_type": "support"}),

    TargetRule("social situation", "REASON", 
              pattern=[
                  {"LOWER": {"IN": ["social","family","home"]}},
                  {"LOWER": {"IN": ["situation","environment"]}},
              ],
              attributes={"treatment_type": "support"}),

    TargetRule("emotional support", "REASON", 
              pattern=[
                  {"LOWER": {"IN": ["emotional"]}},
                  {"LOWER": {"IN": ["support"]}},
              ],
              attributes={"treatment_type": "support"}),

    TargetRule("family support", "REASON",
                pattern=[
                    {"LOWER": {"IN": ["family","patient"]}},
                    {"LOWER": {"IN": ["support"]}},
                ],
                attributes={"treatment_type": "support"}),

    TargetRule("mixed opinions", "REASON",
                pattern=[
                    {"LOWER": {"IN": ["mixed"]}},
                    {"LOWER": {"IN": ["opinions"]}},
                ],
                attributes={"treatment_type": "support"}),

    TargetRule("support", "REASON",
                pattern=[
                    {"LOWER": {"IN": ["support","supporting","supported"]}},
                ],
                attributes={"treatment_type": "support"}),

    TargetRule("adjustment", "REASON",
                pattern=[
                    {"LOWER": {"IN": ["adjustment","adjusting"]}},
                ],
                attributes={"treatment_type": "support"}),

    TargetRule("refuse", "REASON",
                pattern=[
                    {"LOWER": {"IN": ["refuse","refusing","refused"]}},
                ],
                attributes={"treatment_type": "support"}),

#FIXME: remove unsure?? It might moreso reflect goals than support...
    TargetRule("conflicting", "REASON",
                pattern=[
                    {"LOWER": {"IN": ["conflicting","conflict","conflicted","disagreement","disagreements","disagree","unsure","discrepancy"]}},
                ],
                attributes={"treatment_type": "support"}),

    TargetRule("young", "REASON",
                pattern=[
                    {"LOWER": {"IN": ["young"]}},
                ],
                attributes={"treatment_type": "support"}),

    TargetRule("frustrated", "REASON",
                pattern=[
                    {"LOWER": {"IN": ["frustrated","frustration"]}},
                ],
                attributes={"treatment_type": "support"}),

    TargetRule("scared", "REASON",
                pattern=[
                    {"LOWER": {"IN": ["scared","afraid"]}},
                ],
                attributes={"treatment_type": "support"}),

    TargetRule("burden", "REASON",
                pattern=[
                    {"LOWER": {"IN": ["burden"]}},
                ],
                attributes={"treatment_type": "support"}),

    TargetRule("struggle", "REASON",
                pattern=[
                    {"LOWER": {"IN": ["struggle","struggling"]}},
                ],
                attributes={"treatment_type": "support"}),

    TargetRule("difficult", "REASON",
                pattern=[
                    {"LOWER": {"IN": ["difficulty","difficult"]}},
                ],
                attributes={"treatment_type": "support"}),

    TargetRule("understand", "REASON",
                pattern=[
                    {"LOWER": {"IN": ["understand","understanding","insight"]}},
                ],
                attributes={"treatment_type": "support"}),
                
    TargetRule("overwhelmed", "REASON",
                pattern=[
                    {"LOWER": {"IN": ["overwhelmed","overwhelming"]}},
                ],
                attributes={"treatment_type": "support"}),
]

#diagnosis rules

cancer_solid_rules = [
    TargetRule("Cancer", "PROBLEM", 
              pattern=[
                    {"LOWER": {"IN": ["stage"]},
                        "IS_PUNCT": False},
                    {"IS_PUNCT": True, "OP": "?"},
                    {"LOWER": {"IN": ["i","ii","iii","iiia","iiib","1","2","3","3a","3b","one","two","three"]},
                        "IS_PUNCT": False},
              ],
              attributes={"problem_type": "cancer_solid"}),

    TargetRule("Cancer", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["path", "cholangiocarcinoma", "pathology", "squamous","cancer","adenocarcinoma", "nodule","lesion","nodules","rcc","brca", "glioblastoma","metastases","cancers", "carcinoma", "malignancy", "neoplasm", "tumor","metastasis","mets","metastatic","uroepitheliacarcinoma","malignant","mass","gbm","hcc","adenocarcinoma","scc","sclc","nsclc","carcinomatosis","onc","oncology","sarcoma","melanoma","mesothelioma","glioma","astrocytoma","oligodendroglioma","ependymoma"]}},
              ],
              attributes={"problem_type": "cancer_solid"}),

    TargetRule("Cancer", "PROBLEM", 
              pattern = 
                        [{"TEXT": {"REGEX": r"\bca\b"}}]
                        ,
              attributes={"problem_type": "cancer_solid"}),

    TargetRule("Cancer Directed Therapy", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["biopsy","rad","xrt","radiation"]}},
              ],
              attributes={"problem_type": "cancer_solid"}),

    TargetRule("Spread", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["leptomeningeal","carcinomatosis"]}},
              ],
              attributes={"problem_type": "cancer_solid"}),

    TargetRule("blank ca", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["endometrial","lung"]}},
                  {"LOWER": {"IN": ["ca"]}}
              ],
              attributes={"problem_type": "cancer_solid"}),       
            

]

cancer_heme_rules = [
    TargetRule("Cancer", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["cll","lymphoma","leukemia","myeloma"]}},
              ],
              attributes={"problem_type": "cancer_heme"}),

    TargetRule("Cancer", "PROBLEM", 
              pattern=[
                    {"LOWER": {"IN": ["bone"]}, "OP": "?"},
                    {"LOWER": {"IN": ["marrow"]}},
                    {"LOWER": {"IN": ["biopsy","bx"]}},
              ],
              attributes={"problem_type": "cancer_heme"}),
]

cardiovascular_rules = [
    TargetRule("PE", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["pe"]}},
              ],
              attributes={"problem_type": "cardiovascular"}),

    TargetRule("pulmonary embolism", "PROBLEM",
                pattern=[
                    {"LOWER": {"IN": ["pulmonary"]}},
                    {"LOWER": {"IN": ["embolism"]}}
                ],
                attributes={"problem_type": "cardiovascular"}),

    TargetRule("pci", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["pci","angioplasty"]}},
              ],
              attributes={"problem_type": "cardiovascular"}),


    TargetRule("pacermaker", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["pacemaker","pacer","icd","defibrillator"]}},
              ],
              attributes={"problem_type": "cardiovascular"}),

    TargetRule("tavr", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["tavr"]}},
              ],
              attributes={"problem_type": "cardiovascular"}),

    TargetRule("cardiorenal", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["cardiorenal"]}},
              ],
              attributes={"problem_type": "cardiovascular"}),

    TargetRule("cabg", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["cabg"]}},
              ],
              attributes={"problem_type": "cardiovascular"}),

    TargetRule("iabp", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["iabp","impella"]}},
              ],
              attributes={"problem_type": "cardiovascular"}),

    TargetRule("balloon pump", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["balloon"]}},
                  {"LOWER": {"IN": ["pump"]}},
              ],
              attributes={"problem_type": "cardiovascular"}),

    TargetRule("ECMO", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["ecmo"]}},
              ],
              attributes={"problem_type": "cardiovascular"}),

    TargetRule("valve issues", "problem", 
              pattern=[
                  {"LOWER": {"IN" : ["mitral","aortic","tricuspid","pulmonic"]}},
                  {"LOWER": {"IN" : ["stenosis","regurgitation","insufficiency","prolapse","disease","regurge","valve"]}},
              ],
              attributes={"problem_type": "cardiovascular"}),

    TargetRule("NYHA", "problem", 
              pattern=[
                  {"LOWER": {"IN" : ["nyha"]}},
                  {"LOWER": {"IN" : ["class"]}, "OP": "?"},
                  {"LOWER": {"IN" : ["1","2","3","4","one","two","three","four","i","ii","iii","iv"]}},
              ],
              attributes={"problem_type": "cardiovascular"}),

    TargetRule("cardio shock", "problem", 
              pattern=[
                  {"LOWER": {"IN" : ["cardiogenic","cardiac"]}},
                  {"LOWER": "shock"}
              ],
              attributes={"problem_type": "cardiovascular"}),

    TargetRule("fluid overload", "problem", 
              pattern=[
                  {"LOWER": "fluid"},
                  {"LOWER": {"IN" : ["overload","overloaded"]}}                  
              ],
              attributes={"problem_type": "cardiovascular"}),

    TargetRule("Heart Failure", "problem", 
              pattern=[
                  {"LOWER": {"IN" : ["heart","lv","rv"]}},
                  {"LOWER": "failure"}
              ],
              attributes={"problem_type": "cardiovascular"}),

    TargetRule("heart_failure", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["hf","chf","cardiomyopathy","ef","hfpef","hfref","diuretic","diuresis","diurese","cad"]}},
              ],
              attributes={"problem_type": "cardiovascular"}),

    TargetRule("atrial fibrillation", "problem", 
              pattern=[
                  {"LOWER": {"IN": ["atrial"]}},
                  {"LOWER": {"IN": ["fibrillation","fib"]}}
              ],
              attributes={"problem_type": "cardiovascular"}),

    TargetRule("LVAD", "problem", 
              pattern=[
                  {"LOWER": {"IN": ["lvad"]}},
              ],
              attributes={"problem_type": "cardiovascular"}),

    TargetRule("cardiac arrest", "problem",
              pattern=[
                  {"LOWER": {"IN": ["cardiac"]}},
                  {"LOWER": {"IN": ["arrest"]}}
              ],
              attributes={"problem_type": "cardiovascular"}),

    TargetRule("pulmonary hypertension", "problem",
              pattern=[
                  {"LOWER": {"IN": ["pulmonary","pulm"]}},
                  {"LOWER": {"IN": ["hypertension","htn"]}}
              ],
              attributes={"problem_type": "cardiovascular"}),

    TargetRule("rosc", "problem",
              pattern=[
                  {"LOWER": {"IN": ["rosc"]}}
              ],
              attributes={"problem_type": "cardiovascular"}),

    TargetRule("ventricular_dysrhythmias", "problem",
              pattern=[
                  {"LOWER": {"IN": ["vtach","vfib"]}}
              ],
              attributes={"problem_type": "cardiovascular"}),

    TargetRule("stemi", "problem",
              pattern=[
                  {"LOWER": {"IN": ["stemi","nstemi","mi"]}}
              ],
              attributes={"problem_type": "cardiovascular"}),
]

pulmonary_rules = [
    TargetRule("intubated", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["intubated","ventilator","vent","vented","ventilatory","ventilation","vented","ventilating","ventilator"]}},
              ],
              attributes={"problem_type": "pulmonary"}),

    TargetRule("ards", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["ards"]}},
              ],
              attributes={"problem_type": "pulmonary"}),

    TargetRule("COPD", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["copd","emphysema",]}},
              ],
              attributes={"problem_type": "pulmonary"}),

    TargetRule("respiratory failure", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["respiratory","resp"]}},
                  {"LOWER": {"IN": ["failure"]}},
              ],
              attributes={"problem_type": "pulmonary"}),

    TargetRule("pulmonary fibrosis", "PROBLEM",
                pattern=[
                    {"LOWER": {"IN": ["pulmonary","pulm"]}},
                    {"LOWER": {"IN": ["fibrosis"]}}
                ],
                attributes={"problem_type": "pulmonary"}),

    TargetRule("ild", "PROBLEM",
                pattern=[
                    {"LOWER": {"IN": ["ild"]}},
                ],
                attributes={"problem_type": "pulmonary"}),
]

gastrointestinal_rules = [
    TargetRule("bowel perf", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["bowel"]}},
                  {"LOWER": {"IN": ["perforation","perf","perforated"]}},
              ],
              attributes={"problem_type": "gastrointestinal"}),

    TargetRule("bowel perf", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["perforated","perf"]}},
                  {"LOWER": {"IN": ["bowel", "appendix","appendicitis","appy"]}},
              ],
              attributes={"problem_type": "gastrointestinal"}),

    TargetRule("ostomy", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["ostomy","ileostomy","colostomy"]}},
              ],
              attributes={"problem_type": "gastrointestinal"}),

    TargetRule("peritonitis", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["peritonitis"]}},
              ],
              attributes={"problem_type": "gastrointestinal"}),

    TargetRule("colorectal", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["colorectal"]}},
              ],
              attributes={"problem_type": "gastrointestinal"}),
    
    TargetRule("ex lap", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["ex","exploratory"]}},
                  {"LOWER": {"IN": ["lap","laparotomy"]}},
              ],
              attributes={"problem_type": "gastrointestinal"}),

    TargetRule("perforation", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["perforation"]}},
              ],
              attributes={"problem_type": "gastrointestinal"}),

    TargetRule("bowel resection", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["sigmoidectomy","colectomy","resection",]}},
              ],
              attributes={"problem_type": "gastrointestinal"}),
              
    TargetRule("SBO", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["sbo"]}},
              ],
              attributes={"problem_type": "gastrointestinal"}),

    TargetRule("diverticulitis", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["diverticulitis"]}},
              ],
              attributes={"problem_type": "gastrointestinal"}),

    TargetRule("tpn", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["tpn"]}},
              ],
              attributes={"problem_type": "gastrointestinal"}),

    TargetRule("GI bleed", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["rectal","gi","esophageal",]}},
                  {"LOWER": {"IN": ["bleed","bleeding","bleeds","hemorrhage"]}},
              ],
              attributes={"problem_type": "gastrointestinal"}),
]

hepatology_rules = [
    TargetRule("ESLD", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["cirrhosis","cirrhotic","esld","hepatitis","hepatic","hepatorenal","lft","liver","variceal","ascites",]}},
              ],
              attributes={"problem_type": "hepatology"}),
]

renal_rules = [
    TargetRule("esrd", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["esrd","cr","creatinine","renal"]}},
              ],
              attributes={"problem_type": "renal"}),

    TargetRule("acute renal failure", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["acute"]}},
                  {"LOWER": {"IN": ["renal","kidney"]}},
                  {"LOWER": {"IN": ["failure"]}}                  
              ],
              attributes={"problem_type": "renal"}),

    TargetRule("calci", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["calciphylaxis"]}},
              ],
              attributes={"problem_type": "renal"}),

    TargetRule("dialysis", "PROBLEM",
                pattern=[
                    {"LOWER": {"IN": ["dialysis","hd","pd","crrt","cvvhd","cvvh","cvvhd","dialyze"]}}
                ],
                attributes={"problem_type": "renal"}),

    TargetRule("aki", "PROBLEM",
                pattern=[
                    {"LOWER": {"IN": ["aki"]}}
                ],
                attributes={"problem_type": "renal"}),

        TargetRule("ckd", "PROBLEM",
                pattern=[
                    {"LOWER": {"IN": ["ckd","ckd4","ckd5"]}}
                ],
                attributes={"problem_type": "renal"}),

    TargetRule("CKD Stage #", "problem", 
              pattern=[
                  {"LOWER": {"IN" : ["ckd"]}},
                  {"LOWER": {"IN" : ["stage"]}},
                  {"LOWER": {"IN" : ["i","ii","iii","iiia","iiib","1","2","3","3a","3b","one","two","three"]}},
              ],
              attributes={"problem_type": "renal"}),

    TargetRule("renal transplant", "problem", 
              pattern=[
                  {"LOWER": {"IN" : ["renal","kidney"]}},
                  {"LOWER": {"IN" : ["transplant","tx"]}},
              ],
              attributes={"problem_type": "renal"}),
]

dementia_rules = [
    TargetRule("gen neuro", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["dementia","alzheimers","alzheimer's","alzheimer","lewy","frontotemporal","ftd"]}},
              ],
              attributes={"problem_type": "dementia"}),
]

neurology_rules = [

    TargetRule("gen neuro", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["demyelinating","seizure","dysphasic","iph","anoxic","stroke","cva","tbi","coma","parkinsons","parkinson's","parkinson","huntingtons","huntington's","huntington"]}},
              ],
              attributes={"problem_type": "neurology"}),

    TargetRule("anoxic brain injury", "problem", 
              pattern=[
                  {"LOWER": "anoxic"},
                  {"LOWER": "brain"},
                  {"LOWER": "injury"}
              ],
              attributes={"problem_type": "neurology"}),

    TargetRule("cerebral palsy", "problem", 
              pattern=[
                  {"LOWER": "cerebral"},
                  {"LOWER": "palsy"},
              ],
              attributes={"problem_type": "neurology"}),

    TargetRule("mass effect", "problem", 
              pattern=[
                  {"LOWER": "mass"},
                  {"LOWER": "effect"},
              ],
              attributes={"problem_type": "neurology"}),

    TargetRule("traumatic brain injury", "problem", 
              pattern=[
                  {"LOWER": "traumatic"},
                  {"LOWER": "brain"},
                  {"LOWER": "injury"}
              ],
              attributes={"problem_type": "neurology"}),

    TargetRule("Dysphagia", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["dysphagia","swallowing","st","swallow","aspiration","aspirate","aspirated"]}},
              ],
              attributes={"problem_type": "neurology"}),
]

infectious_rules = [
    TargetRule("necrotizing", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["necrotizing"]}},
              ],
              attributes={"problem_type": "infectious"}),

    TargetRule("necrotizing fash", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["necrotizing"]}},
                  {"LOWER": {"IN": ["fasciitis","fash","fascitis"]}},
              ],
              attributes={"problem_type": "infectious"}),

    TargetRule("septic shock", "problem", 
              pattern=[
                  {"LOWER": "septic"},
                  {"LOWER": "shock"}
              ],
              attributes={"problem_type": "infectious"}),

    TargetRule("gen infection", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["infection","infections","sepsis","septic","bacteremia","bacterial","viral","fungal","parasitic","infectious","mrsa","mdro"]}},
              ],
              attributes={"problem_type": "infectious"}),

    TargetRule("C DIFF", "problem", 
              pattern=[
                  {"LOWER": {"IN": ["c","c."]}},
                  {"LOWER": {"IN": ["diff"]}}
              ],
              attributes={"problem_type": "infectious"}),

    TargetRule("septic emboli", "problem", 
              pattern=[
                  {"LOWER": {"IN": ["septic"]}},
                  {"LOWER": {"IN": ["emboli","embolus"]}}
              ],
              attributes={"problem_type": "infectious"}),

    TargetRule("UTI", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["uti","urosepsis","pyelo","pyelonephritis"]}},
              ],
              attributes={"problem_type": "infectious"}),

    TargetRule("HIV", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["hiv","aids"]}},
              ],
              attributes={"problem_type": "infectious"}),

    TargetRule("endocarditis", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["endocarditis"]}},
              ],
              attributes={"problem_type": "infectious"}),

    TargetRule("osteo", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["osteo","osteomyelitis"]}},
              ],
              attributes={"problem_type": "infectious"}),

    TargetRule("covid", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["covid"]}},
              ],
              attributes={"problem_type": "infectious"}),
]

trauma_rules = [
    TargetRule("hip fracture", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["hip","femur"]}},
                  {"LOWER": {"IN": ["fracture","fx"]}},
              ],
              attributes={"problem_type": "trauma"}),

    TargetRule("brain bleeds", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["sdh","sah"]}},
              ],
              attributes={"problem_type": "trauma"}),    
]

vascular_rules = [
    TargetRule("amputation", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["amputation","amputate","bka","aka"]}},
              ],
              attributes={"problem_type": "vascular"}),

    TargetRule("gangrene", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["gangrene"]}},
              ],
              attributes={"problem_type": "vascular"}),

    TargetRule("aortic aneurysm", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["aortic"]}},
                  {"LOWER": {"IN": ["aneurysm"]}},
              ],
              attributes={"problem_type": "vascular"}),

    TargetRule("aortic dissection", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["aortic"]}},
                  {"LOWER": {"IN": ["dissection"]}},
              ],
              attributes={"problem_type": "vascular"}),

    TargetRule("bypass", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["bypass"]}},
              ],
              attributes={"problem_type": "vascular"}),

]

met_end_rules = [


    TargetRule("hypoglycemia", "problem", 
              pattern=[
                  {"LOWER": {"IN": ["hypoglycemia","hypoglycemic"]}},
              ],
              attributes={"problem_type": "met_end"}),

]

genetic_rules = [
    TargetRule("OI", "problem", 
              pattern=[
                  {"LOWER": {"IN": ["OI"]}},
              ],
              attributes={"problem_type": "genetic"}),
]

hematology_rules = [
    TargetRule("anemia", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["anemia"]}},
              ],
              attributes={"problem_type": "hematology"}),
]

premature_rules = [
    
]

fetal_rules = [

]

unknown_rules = [
    TargetRule("ftt", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN": ["ftt","cachexia","cachectic","po","deconditioning","deconditioned","nutrition","malnutrition"]}},
              ],
              attributes={"problem_type": "unknown"}),

    TargetRule("failure to thrive", "PROBLEM", 
              pattern=[
                  {"LOWER": "failure"},
                  {"LOWER": "to"},
                  {"LOWER": "thrive"}
              ],
              attributes={"problem_type": "unknown"}),

    TargetRule("poor po intake", "PROBLEM", 
              pattern=[
                  {"LOWER": {"IN" : ["poor","no"]}},
                  {"LOWER": {"IN" : ["po"]}},
                  {"LOWER": {"IN" : ["intake"]}}
              ],
              attributes={"problem_type": "unknown"}),

    TargetRule("weight loss", "PROBLEM", 
              pattern=[
                  {"LOWER": "weight"},
                  {"LOWER": "loss"}
              ],
              attributes={"problem_type": "unknown"}),


    TargetRule("stage_4", "PROBLEM",
              pattern=[
                    {"LOWER": {"IN": ["stage"]}},
                    {"IS_PUNCT": True, "OP": "?"},
                    {"LOWER": {"IN": ["iv","4","four"]}},
              ],
              on_match=disambiguate_stage_4)
                
]

target_rules = symptom_rules + goal_rules + support_rules + cancer_solid_rules + cancer_heme_rules + cardiovascular_rules + pulmonary_rules + gastrointestinal_rules + hepatology_rules + renal_rules + dementia_rules + neurology_rules + infectious_rules + trauma_rules + vascular_rules + met_end_rules + genetic_rules + hematology_rules + premature_rules + fetal_rules + unknown_rules 