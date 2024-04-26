from medspacy.postprocess import PostprocessingRule, PostprocessingPattern, Postprocessor
from medspacy.postprocess import postprocessing_functions

postprocess_rules = [
    # Instantiate our rule
    PostprocessingRule(
        # Pass in a list of patterns
        patterns=[
            # The pattern will check if the entitie's section is "patient_instructions"
            PostprocessingPattern(condition=lambda ent: ent._.is_negated, success_value=True),
        ],
        # If all patterns are True, this entity will be removed.
        action=postprocessing_functions.remove_ent,
        description="Remove any negated entities."
    ),
    
]