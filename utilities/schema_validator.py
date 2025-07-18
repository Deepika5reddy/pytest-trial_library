REQUIRED_FIELDS = {
    "tl_sponsored_trial_uuid": str,
    "sponsored_trial_nct_id": str,
    "distance_to_closest_location_in_miles": float,
    "sponsored_trial_name": str,
    "sponsored_trial_study_url": str,
    "sponsored_trial_brief_summary" : str,
    "sponsored_trial_conditions" : str,
    "sponsored_trial_phase": str,
    "sponsored_trial_inclusion_criteria": list,
    "sponsored_trial_exclusion_criteria": list,
    "closest_principal_investigator_email": (str, type(None)),

}
