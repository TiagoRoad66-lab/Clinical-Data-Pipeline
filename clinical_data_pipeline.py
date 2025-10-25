import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import sqlite3
import numpy as np

# Initialize Faker for realistic-looking data
fake = Faker()

# --- 1. DATA GENERATION (MIMICKING CRF PULLS FROM MULTIPLE SITES) ---

def generate_synthetic_data(num_animals=50, num_visits_per_animal=5):
    """
    Generates five related datasets simulating core clinical/pre-clinical CRFs
    from multiple clinical sites WITH REALISTIC DATA QUALITY ISSUES:
    1. Screening (SC) - Initial screening visit
    2. Demographics (DM) - Includes Site ID
    3. Dosing/Exposure (EX) - Contains the critical first dosing date per site
    4. Vital Signs/Observations (VS) - Contains measurement data with site info
    5. Study Completion (CO) - End of study visit
    
    Multi-site complexity includes:
    - Different enrollment rates per site
    - Site-specific start dates (staggered site activation)
    - REALISTIC DATA DISCREPANCIES requiring queries
    """
    print("--- 1. Generating Synthetic Multi-Site CRF Data (with quality issues) ---")

    # Define sites with different characteristics (US sites)
    sites = ['US01', 'US02', 'US03']
    site_start_dates = {
        'US01': datetime(2025, 1, 1),   # First site activated
        'US02': datetime(2025, 1, 15),  # Second site activated 2 weeks later
        'US03': datetime(2025, 2, 1)    # Third site activated 1 month later
    }
    
    # Site enrollment distribution (some sites enroll more subjects)
    site_weights = [0.4, 0.35, 0.25]  # Site 01 enrolls 40%, Site 02 35%, Site 03 25%
    
    # Generate animal IDs with site prefix (sequential per site: US0101, US0102, etc.)
    site_assignments = random.choices(sites, weights=site_weights, k=num_animals)
    
    animal_ids = []
    site_counters = {site: 1 for site in sites}
    
    for site in site_assignments:
        animal_id = f"{site}{site_counters[site]:02d}"  # US0101, US0102, etc.
        animal_ids.append(animal_id)
        site_counters[site] += 1
    
    # 1. SCREENING VISIT (SC) - Initial screening data
    data_sc = []
    for idx, animal_id in enumerate(animal_ids):
        site_id = animal_id[:4]  # Extract site from animal ID
        site_activation = site_start_dates[site_id]
        
        # Screening happens 7-21 days before site activation
        screening_date = site_activation - timedelta(days=random.randint(7, 21))
        
        age_value = round(random.uniform(1.0, 5.0), 1)
        age_unit = random.choice(['Years', 'Months'])
        
        data_sc.append({
            'AnimalID': animal_id,
            'SiteID': site_id,
            'ScreeningDate': screening_date.strftime('%Y-%m-%d'),
            'AnimalName': fake.first_name(),
            'ConsentSigned': random.choice(['Yes', 'No', None]),  # Some missing
            'AntigenTest_Leishmania': random.choice(['Negative', 'Positive', None]),
            'AntigenTest_Dirofilaria': random.choice(['Negative', 'Positive', None]),
            'Species': random.choice(['Dog', 'Rat', 'Monkey']),
            'Sex': random.choice(['M', 'F', None]),  # Some missing
            'Age': age_value,
            'AgeUnit': age_unit
        })
    df_sc = pd.DataFrame(data_sc)
    
    # INTRODUCE DATA QUALITY ISSUES IN SCREENING
    # Issue 1: Missing consent signature (protocol violation)
    missing_consent_indices = random.sample(range(len(df_sc)), k=int(num_animals * 0.05))
    for idx in missing_consent_indices:
        df_sc.at[idx, 'ConsentSigned'] = None
    
    # Issue 2: Positive antigen tests (should be exclusion criteria)
    positive_test_indices = random.sample(range(len(df_sc)), k=int(num_animals * 0.03))
    for idx in positive_test_indices:
        df_sc.at[idx, 'AntigenTest_Leishmania'] = 'Positive'
    
    # Issue 3: Missing antigen test results
    missing_test_indices = random.sample(range(len(df_sc)), k=int(num_animals * 0.04))
    for idx in missing_test_indices:
        df_sc.at[idx, 'AntigenTest_Dirofilaria'] = None
    
    print(f"SC Data Generated: {len(df_sc)} screening records.")
    print(f"⚠️  {len(missing_consent_indices)} missing consent signatures")
    print(f"⚠️  {len(positive_test_indices)} positive antigen tests (potential exclusion)")
    print(f"⚠️  {len(missing_test_indices)} missing antigen test results")
    
    # 2. Demographics (DM)
    data_dm = {
        'AnimalID': animal_ids,
        'SiteID': [aid[:4] for aid in animal_ids],
        'Species': [df_sc[df_sc['AnimalID'] == aid]['Species'].values[0] for aid in animal_ids],
        'DoseGroup': random.choices(['Low', 'Mid', 'High', 'Control'], k=num_animals),
        'Sex': [df_sc[df_sc['AnimalID'] == aid]['Sex'].values[0] for aid in animal_ids],
        'BirthDate': [fake.date_of_birth(minimum_age=1, maximum_age=2).strftime('%Y-%m-%d') 
                      for _ in range(num_animals)],
        'EnrollmentDate': [fake.date_between(start_date='-60d', end_date='today').strftime('%Y-%m-%d') 
                           for _ in range(num_animals)]
    }
    df_dm = pd.DataFrame(data_dm)
    
    # INTRODUCE DATA QUALITY ISSUES IN DEMOGRAPHICS
    # Issue: Invalid BirthDate (future dates - data entry error)
    invalid_birth_indices = random.sample(range(len(df_dm)), k=int(num_animals * 0.02))
    for idx in invalid_birth_indices:
        df_dm.at[idx, 'BirthDate'] = (datetime.now() + timedelta(days=random.randint(1, 30))).strftime('%Y-%m-%d')
    
    print(f"DM Data Generated: {len(df_dm)} records across {len(sites)} sites.")
    print(f"Site Distribution: {df_dm['SiteID'].value_counts().to_dict()}")
    print(f"⚠️  Introduced {len(invalid_birth_indices)} invalid BirthDates (future dates)")

    # 3. Dosing/Exposure (EX) - KEY DATE for Day of Study Calculation
    # IMPORTANT: First dose date is DAY 0
    data_ex = []
    for idx, row in df_dm.iterrows():
        animal_id = row['AnimalID']
        site_id = row['SiteID']
        
        # First dose occurs within 14 days of site activation
        site_activation = site_start_dates[site_id]
        dosing_date = site_activation + timedelta(days=random.randint(0, 14))
        
        data_ex.append({
            'AnimalID': animal_id,
            'SiteID': site_id,
            'FirstDoseDate': dosing_date.strftime('%Y-%m-%d'),
            'Compound': 'Experimental Drug X',
            'DoseLevel_mg': random.choice([10, 25, 50, 100])
        })
    df_ex = pd.DataFrame(data_ex)
    
    # INTRODUCE DATA QUALITY ISSUES IN DOSING
    # Issue: Dosing date before enrollment date (protocol violation or data error)
    dose_before_enroll_indices = random.sample(range(len(df_ex)), k=int(num_animals * 0.04))
    for idx in dose_before_enroll_indices:
        animal_id = df_ex.at[idx, 'AnimalID']
        enroll_date = pd.to_datetime(df_dm[df_dm['AnimalID'] == animal_id]['EnrollmentDate'].values[0])
        df_ex.at[idx, 'FirstDoseDate'] = (enroll_date - timedelta(days=5)).strftime('%Y-%m-%d')
    
    df_ex.set_index('AnimalID', inplace=True)
    print(f"EX Data Generated: {len(df_ex)} records.")
    print(f"⚠️  Introduced {len(dose_before_enroll_indices)} dosing dates before enrollment")

    # 4. Vital Signs/Observations (VS)
    data_vs = []
    for idx, row in df_dm.iterrows():
        animal_id = row['AnimalID']
        site_id = row['SiteID']
        
        # Site-specific measurement variability
        site_temp_offset = {'US01': 0.0, 'US02': 0.2, 'US03': -0.1}
        
        for visit in range(1, num_visits_per_animal + 1):
            visit_day = visit * random.randint(3, 7)
            
            weight = round(random.uniform(5.0, 30.0), 2)
            heart_rate = random.randint(80, 150)
            temperature = round(random.uniform(36.5, 38.0) + site_temp_offset[site_id], 1)
            
            # INTRODUCE DATA QUALITY ISSUES
            if random.random() < 0.03:
                temperature = round(random.choice([34.5, 35.0, 40.5, 41.0]), 1)
            
            if random.random() < 0.04:
                weight = None
            
            requires_comment = (temperature < 36.0 or temperature > 39.0)
            has_comment = random.random() < 0.3 if requires_comment else random.random() < 0.1
            comment = fake.sentence() if has_comment else None
            
            data_vs.append({
                'AnimalID': animal_id,
                'SiteID': site_id,
                'VisitDayNum': visit_day,
                'VisitNumber': visit,
                'Weight_kg': weight,
                'HeartRate_bpm': heart_rate,
                'Temperature_C': temperature,
                'Comment': comment,
                'Observation_ID': fake.uuid4(),
                'DataEntryDate': (datetime.now() - timedelta(days=random.randint(0, 30))).strftime('%Y-%m-%d')
            })
    df_vs = pd.DataFrame(data_vs)
    
    temp_out_range = len(df_vs[(df_vs['Temperature_C'] < 36.0) | (df_vs['Temperature_C'] > 39.0)])
    missing_weights = df_vs['Weight_kg'].isna().sum()
    missing_comments_when_required = len(df_vs[
        ((df_vs['Temperature_C'] < 36.0) | (df_vs['Temperature_C'] > 39.0)) & 
        (df_vs['Comment'].isna())
    ])
    
    print(f"VS Data Generated: {len(df_vs)} records.")
    print(f"⚠️  Introduced {temp_out_range} out-of-range temperature values")
    print(f"⚠️  Introduced {missing_weights} missing weight values")
    print(f"⚠️  {missing_comments_when_required} out-of-range temperatures without required comments")

    # 5. STUDY COMPLETION VISIT (CO)
    data_co = []
    for idx, row in df_dm.iterrows():
        animal_id = row['AnimalID']
        site_id = row['SiteID']
        
        # Completion visit happens ~30-45 days after first dose
        first_dose = pd.to_datetime(df_ex.loc[animal_id, 'FirstDoseDate'])
        completion_date = first_dose + timedelta(days=random.randint(30, 45))
        
        # Study completion status
        completion_status = random.choice(['Completed', 'Early Termination', 'Withdrawn', None])
        reason_for_early_term = None
        if completion_status == 'Early Termination':
            reason_for_early_term = random.choice([
                'Adverse Event', 
                'Protocol Violation', 
                'Animal Health Concerns',
                None  # Missing reason
            ])
        
        data_co.append({
            'AnimalID': animal_id,
            'SiteID': site_id,
            'CompletionDate': completion_date.strftime('%Y-%m-%d') if completion_status else None,
            'CompletionStatus': completion_status,
            'ReasonForEarlyTermination': reason_for_early_term,
            'FinalWeight_kg': round(random.uniform(5.0, 30.0), 2) if completion_status else None,
            'OverallHealthStatus': random.choice(['Good', 'Fair', 'Poor', None]),
            'AdverseEventsReported': random.choice(['Yes', 'No', None])
        })
    df_co = pd.DataFrame(data_co)
    
    # INTRODUCE DATA QUALITY ISSUES IN COMPLETION
    # Issue 1: Missing completion status
    missing_completion_indices = random.sample(range(len(df_co)), k=int(num_animals * 0.06))
    for idx in missing_completion_indices:
        df_co.at[idx, 'CompletionStatus'] = None
        df_co.at[idx, 'CompletionDate'] = None
    
    # Issue 2: Early termination without reason
    early_term_no_reason = df_co[
        (df_co['CompletionStatus'] == 'Early Termination') & 
        (df_co['ReasonForEarlyTermination'].isna())
    ]
    
    print(f"CO Data Generated: {len(df_co)} completion records.")
    print(f"⚠️  {len(missing_completion_indices)} missing completion status")
    print(f"⚠️  {len(early_term_no_reason)} early terminations without reason")

    return df_sc, df_dm, df_ex, df_vs, df_co

# --- 2. DATA QUALITY CHECK AND QUERY GENERATION ---

def generate_data_quality_queries(df_sc, df_dm, df_ex, df_vs, df_co):
    """
    Identifies data discrepancies that require site queries.
    Does NOT auto-correct - generates query reports for manual resolution.
    """
    print("\n--- 2. Data Quality Check: Generating Query Reports ---")
    
    queries = []
    query_id_counter = 1
    
    # SCREENING QUERIES
    # Query: Missing consent signature
    missing_consent = df_sc[df_sc['ConsentSigned'].isna() | (df_sc['ConsentSigned'] == 'No')]
    for idx, row in missing_consent.iterrows():
        queries.append({
            'QueryID': f"QRY_{query_id_counter:04d}",
            'QueryType': 'Protocol Violation',
            'Severity': 'Critical',
            'SiteID': row['SiteID'],
            'AnimalID': row['AnimalID'],
            'Domain': 'Screening',
            'Field': 'ConsentSigned',
            'Issue': 'Consent signature missing or marked as "No"',
            'QueryText': f"Please confirm consent was properly obtained for {row['AnimalID']} ({row['AnimalName']}). Current value: {row['ConsentSigned']}",
            'Status': 'Open',
            'DateOpened': datetime.now().strftime('%Y-%m-%d')
        })
        query_id_counter += 1
    
    # Query: Positive antigen tests (exclusion criteria)
    positive_tests = df_sc[
        (df_sc['AntigenTest_Leishmania'] == 'Positive') | 
        (df_sc['AntigenTest_Dirofilaria'] == 'Positive')
    ]
    for idx, row in positive_tests.iterrows():
        test_type = 'Leishmania' if row['AntigenTest_Leishmania'] == 'Positive' else 'Dirofilaria'
        queries.append({
            'QueryID': f"QRY_{query_id_counter:04d}",
            'QueryType': 'Inclusion/Exclusion Criteria',
            'Severity': 'Critical',
            'SiteID': row['SiteID'],
            'AnimalID': row['AnimalID'],
            'Domain': 'Screening',
            'Field': f'AntigenTest_{test_type}',
            'Issue': f'Positive {test_type} test - potential exclusion criterion',
            'QueryText': f"Subject {row['AnimalID']} has positive {test_type} antigen test. Please verify if subject meets inclusion criteria or if test result is erroneous.",
            'Status': 'Open',
            'DateOpened': datetime.now().strftime('%Y-%m-%d')
        })
        query_id_counter += 1
    
    # Query: Missing antigen tests
    missing_tests = df_sc[
        df_sc['AntigenTest_Leishmania'].isna() | 
        df_sc['AntigenTest_Dirofilaria'].isna()
    ]
    for idx, row in missing_tests.iterrows():
        queries.append({
            'QueryID': f"QRY_{query_id_counter:04d}",
            'QueryType': 'Missing Data',
            'Severity': 'High',
            'SiteID': row['SiteID'],
            'AnimalID': row['AnimalID'],
            'Domain': 'Screening',
            'Field': 'AntigenTests',
            'Issue': 'Required antigen test result(s) missing',
            'QueryText': f"Please provide missing antigen test results for {row['AnimalID']}.",
            'Status': 'Open',
            'DateOpened': datetime.now().strftime('%Y-%m-%d')
        })
        query_id_counter += 1
    
    # DEMOGRAPHICS QUERIES
    missing_sex = df_dm[df_dm['Sex'].isna()]
    for idx, row in missing_sex.iterrows():
        queries.append({
            'QueryID': f"QRY_{query_id_counter:04d}",
            'QueryType': 'Missing Data',
            'Severity': 'High',
            'SiteID': row['SiteID'],
            'AnimalID': row['AnimalID'],
            'Domain': 'Demographics',
            'Field': 'Sex',
            'Issue': 'Sex field is missing',
            'QueryText': f"Please provide the sex for {row['AnimalID']}",
            'Status': 'Open',
            'DateOpened': datetime.now().strftime('%Y-%m-%d')
        })
        query_id_counter += 1
    
    # Invalid birth dates
    df_dm_check = df_dm.copy()
    df_dm_check['BirthDate'] = pd.to_datetime(df_dm_check['BirthDate'], errors='coerce')
    invalid_births = df_dm_check[df_dm_check['BirthDate'] > datetime.now()]
    for idx, row in invalid_births.iterrows():
        queries.append({
            'QueryID': f"QRY_{query_id_counter:04d}",
            'QueryType': 'Data Inconsistency',
            'Severity': 'Critical',
            'SiteID': row['SiteID'],
            'AnimalID': row['AnimalID'],
            'Domain': 'Demographics',
            'Field': 'BirthDate',
            'Issue': f"Birth date is in the future",
            'QueryText': f"Please verify and correct the birth date for {row['AnimalID']}. Current value appears to be a future date.",
            'Status': 'Open',
            'DateOpened': datetime.now().strftime('%Y-%m-%d')
        })
        query_id_counter += 1
    
    # DOSING QUERIES
    df_merged_check = df_ex.reset_index().merge(df_dm[['AnimalID', 'EnrollmentDate']], on='AnimalID')
    df_merged_check['FirstDoseDate'] = pd.to_datetime(df_merged_check['FirstDoseDate'])
    df_merged_check['EnrollmentDate'] = pd.to_datetime(df_merged_check['EnrollmentDate'])
    dose_before_enroll = df_merged_check[df_merged_check['FirstDoseDate'] < df_merged_check['EnrollmentDate']]
    
    for idx, row in dose_before_enroll.iterrows():
        queries.append({
            'QueryID': f"QRY_{query_id_counter:04d}",
            'QueryType': 'Protocol Deviation',
            'Severity': 'Critical',
            'SiteID': row['SiteID'],
            'AnimalID': row['AnimalID'],
            'Domain': 'Dosing',
            'Field': 'FirstDoseDate',
            'Issue': f"First dose date precedes enrollment date",
            'QueryText': f"Please verify the first dose date for {row['AnimalID']}. Current date precedes enrollment, which may indicate protocol deviation or data entry error.",
            'Status': 'Open',
            'DateOpened': datetime.now().strftime('%Y-%m-%d')
        })
        query_id_counter += 1
    
    # VITAL SIGNS QUERIES
    temp_out_range = df_vs[(df_vs['Temperature_C'] < 36.0) | (df_vs['Temperature_C'] > 39.0)]
    for idx, row in temp_out_range.iterrows():
        queries.append({
            'QueryID': f"QRY_{query_id_counter:04d}",
            'QueryType': 'Out of Range Value',
            'Severity': 'Medium',
            'SiteID': row['SiteID'],
            'AnimalID': row['AnimalID'],
            'Domain': 'Vital Signs',
            'Field': 'Temperature_C',
            'Issue': f"Temperature ({row['Temperature_C']}°C) is outside expected range",
            'QueryText': f"Please verify temperature reading of {row['Temperature_C']}°C for {row['AnimalID']} on Visit {row['VisitNumber']}. If correct, please provide clinical explanation.",
            'Status': 'Open',
            'DateOpened': datetime.now().strftime('%Y-%m-%d')
        })
        query_id_counter += 1
    
    missing_weights = df_vs[df_vs['Weight_kg'].isna()]
    for idx, row in missing_weights.iterrows():
        queries.append({
            'QueryID': f"QRY_{query_id_counter:04d}",
            'QueryType': 'Missing Data',
            'Severity': 'Medium',
            'SiteID': row['SiteID'],
            'AnimalID': row['AnimalID'],
            'Domain': 'Vital Signs',
            'Field': 'Weight_kg',
            'Issue': f"Weight measurement is missing",
            'QueryText': f"Please provide weight measurement for {row['AnimalID']} at Visit {row['VisitNumber']}.",
            'Status': 'Open',
            'DateOpened': datetime.now().strftime('%Y-%m-%d')
        })
        query_id_counter += 1
    
    missing_comments = df_vs[
        ((df_vs['Temperature_C'] < 36.0) | (df_vs['Temperature_C'] > 39.0)) & 
        (df_vs['Comment'].isna())
    ]
    for idx, row in missing_comments.iterrows():
        queries.append({
            'QueryID': f"QRY_{query_id_counter:04d}",
            'QueryType': 'Missing Required Comment',
            'Severity': 'Medium',
            'SiteID': row['SiteID'],
            'AnimalID': row['AnimalID'],
            'Domain': 'Vital Signs',
            'Field': 'Comment',
            'Issue': f"Comment required for out-of-range temperature but not provided",
            'QueryText': f"Temperature for {row['AnimalID']} at Visit {row['VisitNumber']} is {row['Temperature_C']}°C (out of range). Please provide clinical comment.",
            'Status': 'Open',
            'DateOpened': datetime.now().strftime('%Y-%m-%d')
        })
        query_id_counter += 1
    
    # COMPLETION QUERIES
    missing_completion = df_co[df_co['CompletionStatus'].isna()]
    for idx, row in missing_completion.iterrows():
        queries.append({
            'QueryID': f"QRY_{query_id_counter:04d}",
            'QueryType': 'Missing Data',
            'Severity': 'High',
            'SiteID': row['SiteID'],
            'AnimalID': row['AnimalID'],
            'Domain': 'Study Completion',
            'Field': 'CompletionStatus',
            'Issue': 'Study completion status missing',
            'QueryText': f"Please provide study completion status for {row['AnimalID']}.",
            'Status': 'Open',
            'DateOpened': datetime.now().strftime('%Y-%m-%d')
        })
        query_id_counter += 1
    
    early_term_no_reason = df_co[
        (df_co['CompletionStatus'] == 'Early Termination') & 
        (df_co['ReasonForEarlyTermination'].isna())
    ]
    for idx, row in early_term_no_reason.iterrows():
        queries.append({
            'QueryID': f"QRY_{query_id_counter:04d}",
            'QueryType': 'Missing Required Field',
            'Severity': 'High',
            'SiteID': row['SiteID'],
            'AnimalID': row['AnimalID'],
            'Domain': 'Study Completion',
            'Field': 'ReasonForEarlyTermination',
            'Issue': 'Early termination reason not provided',
            'QueryText': f"Subject {row['AnimalID']} marked as 'Early Termination' but reason not provided. Please specify reason.",
            'Status': 'Open',
            'DateOpened': datetime.now().strftime('%Y-%m-%d')
        })
        query_id_counter += 1
    
    df_queries = pd.DataFrame(queries)
    
    if len(df_queries) > 0:
        print(f"\n📋 Generated {len(df_queries)} data queries requiring site resolution:")
        print(f"   - Critical: {len(df_queries[df_queries['Severity'] == 'Critical'])}")
        print(f"   - High: {len(df_queries[df_queries['Severity'] == 'High'])}")
        print(f"   - Medium: {len(df_queries[df_queries['Severity'] == 'Medium'])}")
        print(f"\nQueries by Site:")
        print(df_queries['SiteID'].value_counts())
        print(f"\nTop Query Types:")
        print(df_queries['QueryType'].value_counts().head())
    
    return df_queries

# --- 3. DATA WRANGLING (WITHOUT AUTO-CORRECTION) ---

def calculate_day_of_study(df_sc, df_dm, df_ex, df_vs, df_co):
    """
    Merges dataframes and calculates Day of Study (DoS).
    IMPORTANT: First dose date is DAY 0 (not DAY 1)
    """
    print("\n--- 3. Wrangling Multi-Site Data (Flagging Issues, Not Correcting) ---")
    
    # Merge all data
    df_merged = df_vs.merge(df_dm, on=['AnimalID', 'SiteID'], how='left')
    df_merged = df_merged.merge(
        df_ex[['SiteID', 'FirstDoseDate', 'DoseLevel_mg']], 
        on=['AnimalID', 'SiteID'], 
        how='left'
    )
    df_merged = df_merged.merge(
        df_sc[['AnimalID', 'SiteID', 'ScreeningDate', 'AnimalName']], 
        on=['AnimalID', 'SiteID'], 
        how='left'
    )
    
    # Convert dates
    df_merged['FirstDoseDate'] = pd.to_datetime(df_merged['FirstDoseDate'], errors='coerce')
    df_merged['EnrollmentDate'] = pd.to_datetime(df_merged['EnrollmentDate'], errors='coerce')
    df_merged['BirthDate'] = pd.to_datetime(df_merged['BirthDate'], errors='coerce')
    df_merged['ScreeningDate'] = pd.to_datetime(df_merged['ScreeningDate'], errors='coerce')

    # Calculate SimulatedVisitDate
    df_merged['SimulatedVisitDate'] = df_merged.apply(
        lambda row: row['FirstDoseDate'] + timedelta(days=row['VisitDayNum']) 
        if pd.notna(row['FirstDoseDate']) else None, 
        axis=1
    )
    
    # Calculate Day of Study (DOS) - DAY 0 is first dose date
    df_merged['DayOfStudy'] = (df_merged['SimulatedVisitDate'] - df_merged['FirstDoseDate']).dt.days
    
    # Calculate screening period
    df_merged['DaysScreeningToFirstDose'] = (df_merged['FirstDoseDate'] - df_merged['EnrollmentDate']).dt.days

    # ADD DATA QUALITY FLAGS (only for records with actual issues)
    df_merged['DataQualityFlag'] = None
    df_merged['FlagReason'] = None

    # Flag 1: Missing critical data
    missing_data_mask = (df_merged['Sex'].isna()) | (df_merged['Weight_kg'].isna())
    df_merged.loc[missing_data_mask, 'DataQualityFlag'] = 'QUERY_REQUIRED'
    df_merged.loc[missing_data_mask, 'FlagReason'] = 'Missing critical data'
    
    # Flag 2: Out of range temperature (only if not already flagged)
    out_of_range_mask = ((df_merged['Temperature_C'] < 36.0) | (df_merged['Temperature_C'] > 39.0)) & df_merged['DataQualityFlag'].isna()
    df_merged.loc[out_of_range_mask, 'DataQualityFlag'] = 'QUERY_REQUIRED'
    df_merged.loc[out_of_range_mask, 'FlagReason'] = 'Out of range temperature'
    
    # Flag 3: Protocol deviation (only if not already flagged AND actually negative)
    protocol_deviation_mask = (df_merged['DaysScreeningToFirstDose'] < 0) & df_merged['DataQualityFlag'].isna()
    df_merged.loc[protocol_deviation_mask, 'DataQualityFlag'] = 'PROTOCOL_DEVIATION'
    df_merged.loc[protocol_deviation_mask, 'FlagReason'] = 'Dose before enrollment'
    
    # Select final columns
    df_final = df_merged[[
        'AnimalID',
        'SiteID',
        'AnimalName',
        'Species', 
        'Sex',
        'DoseGroup',
        'DoseLevel_mg',
        'BirthDate',
        'ScreeningDate',
        'EnrollmentDate',
        'FirstDoseDate',
        'SimulatedVisitDate',
        'VisitNumber',
        'DayOfStudy',
        'DaysScreeningToFirstDose',
        'Weight_kg', 
        'HeartRate_bpm',
        'Temperature_C',
        'Comment',
        'DataQualityFlag',
        'FlagReason',
        'DataEntryDate'
    ]].sort_values(by=['SiteID', 'AnimalID', 'DayOfStudy'])
    
    flagged_records = df_final[df_final['DataQualityFlag'].notna()]
    
    print(f"Final Merged Dataset Created: {len(df_final)} records.")
    print(f"Data spans {df_final['SiteID'].nunique()} sites with {df_final['AnimalID'].nunique()} unique animals.")
    print(f"⚠️  {len(flagged_records)} records flagged for data quality review ({len(flagged_records)/len(df_final)*100:.1f}%)")
    
    return df_final

# --- 4. EXPLORATORY DATA ANALYSIS ---

def perform_eda(df, df_queries):
    """
    Performs EDA with data quality reporting.
    """
    print("\n--- 4. Exploratory Data Analysis (with Data Quality Metrics) ---")
    
    # Data Quality Summary
    print("\n=== DATA QUALITY SUMMARY ===")
    print(f"Total Records: {len(df)}")
    print(f"Records Flagged: {df['DataQualityFlag'].notna().sum()} ({df['DataQualityFlag'].notna().sum()/len(df)*100:.1f}%)")
    print(f"Open Queries: {len(df_queries[df_queries['Status'] == 'Open'])}")
    
    # Missing Values Report
    print("\n=== MISSING DATA REPORT ===")
    missing_report = df.isnull().sum()
    missing_report = missing_report[missing_report > 0].sort_values(ascending=False)
    if len(missing_report) > 0:
        print(missing_report)
    else:
        print("No missing values detected")
    
    # Site-level Data Quality
    print("\n=== SITE-LEVEL DATA QUALITY ===")
    site_quality = df.groupby('SiteID').agg({
        'DataQualityFlag': lambda x: x.notna().sum(),
        'AnimalID': 'nunique'
    }).rename(columns={'DataQualityFlag': 'FlaggedRecords', 'AnimalID': 'TotalAnimals'})
    site_quality['FlagRate_%'] = (site_quality['FlaggedRecords'] / df.groupby('SiteID').size() * 100).round(2)
    print(site_quality)
    
    # Descriptive statistics for CLEAN data only
    clean_df = df[df['DataQualityFlag'].isna()]
    print(f"\n=== DESCRIPTIVE STATISTICS (Clean Data Only: {len(clean_df)} records) ===")
    print(clean_df[['Weight_kg', 'HeartRate_bpm', 'Temperature_C', 'DayOfStudy']].describe())
    
    # Site enrollment
    print("\n=== SITE ENROLLMENT ===")
    print(df.groupby('SiteID')['AnimalID'].nunique().sort_values(ascending=False))

# --- 5. EXPORT TO SQL DATABASE ---

def export_to_sql(df, df_sc, df_co, df_queries, db_name='clinical_data_db.sqlite'):
    """
    Exports all CRF domains and query reports to SQLite database.
    """
    print("\n--- 5. Exporting Data to SQL Database ---")
    
    try:
        conn = sqlite3.connect(db_name)
        
        # Table 1: Screening data
        df_sc.to_sql('screening_data', conn, if_exists='replace', index=False)
        print(f"✅ Exported screening data to 'screening_data' table")
        
        # Table 2: Main observation data
        df.to_sql('observation_data', conn, if_exists='replace', index=False)
        print(f"✅ Exported main data to 'observation_data' table")
        
        # Table 3: Completion data
        df_co.to_sql('completion_data', conn, if_exists='replace', index=False)
        print(f"✅ Exported completion data to 'completion_data' table")
        
        # Table 4: Data Quality Queries
        df_queries.to_sql('data_queries', conn, if_exists='replace', index=False)
        print(f"✅ Exported {len(df_queries)} queries to 'data_queries' table")
        
        # Table 5: Site summary
        site_summary = df.groupby('SiteID').agg({
            'AnimalID': 'nunique',
            'Weight_kg': 'mean',
            'HeartRate_bpm': 'mean',
            'Temperature_C': 'mean',
            'FirstDoseDate': 'min',
            'SimulatedVisitDate': 'max',
            'DataQualityFlag': lambda x: x.notna().sum()
        }).reset_index()
        
        site_summary.columns = [
            'SiteID', 'TotalAnimals', 'AvgWeight_kg', 'AvgHeartRate_bpm',
            'AvgTemperature_C', 'FirstDoseDate', 'LastVisitDate', 'FlaggedRecords'
        ]
        
        site_summary.to_sql('site_summary', conn, if_exists='replace', index=False)
        print(f"✅ Exported site summary to 'site_summary' table")
        
        # Table 6: Query Summary by Site
        query_summary = df_queries.groupby(['SiteID', 'QueryType']).size().reset_index(name='Count')
        query_summary.to_sql('query_summary_by_site', conn, if_exists='replace', index=False)
        print(f"✅ Exported query summary to 'query_summary_by_site' table")
        
        # Verification
        print("\n--- Database Verification ---")
        print(f"\nSample from screening_data:")
        print(pd.read_sql("SELECT AnimalID, SiteID, AnimalName, ConsentSigned FROM screening_data LIMIT 3", conn))
        
        print(f"\nSample from observation_data:")
        print(pd.read_sql("SELECT AnimalID, SiteID, DayOfStudy, Weight_kg, DataQualityFlag FROM observation_data LIMIT 3", conn))
        
        print(f"\nSample from completion_data:")
        print(pd.read_sql("SELECT AnimalID, SiteID, CompletionStatus, CompletionDate FROM completion_data LIMIT 3", conn))
        
        print(f"\nSample from data_queries:")
        print(pd.read_sql("SELECT QueryID, QueryType, Severity, SiteID, Issue FROM data_queries LIMIT 5", conn))
        
        conn.close()
        
    except Exception as e:
        print(f"❌ An error occurred during SQL export: {e}")

# --- MAIN PIPELINE EXECUTION ---

if __name__ == "__main__":
    print("="*80)
    print(" MULTI-SITE CLINICAL DATA PIPELINE WITH QUERY MANAGEMENT")
    print(" Simulating realistic data quality issues requiring site resolution")
    print(" Note: First dose date is considered Day 0")
    print("="*80)
    
    # Step 1: Generate Multi-Site Data (with quality issues)
    df_sc, df_dm, df_ex, df_vs, df_co = generate_synthetic_data(num_animals=120, num_visits_per_animal=6)

    # Step 2: Data Quality Check - Generate Queries (DO NOT AUTO-CORRECT)
    df_queries = generate_data_quality_queries(df_sc, df_dm, df_ex, df_vs, df_co)

    # Step 3: Wrangling (Flag issues, don't fix them)
    df_final_cleaned = calculate_day_of_study(df_sc, df_dm, df_ex, df_vs, df_co)

    # Step 4: EDA with Data Quality Reporting
    perform_eda(df_final_cleaned, df_queries)

    # Step 5: Export to SQL DB
    export_to_sql(df_final_cleaned, df_sc, df_co, df_queries)
    
    print("\n" + "="*80)
    print(" PIPELINE EXECUTION COMPLETE")
    print("="*80)
    print("\n📊 Generated Database Tables:")
    print("   1. screening_data - Screening visit CRF")
    print("   2. observation_data - Main dataset with quality flags")
    print("   3. completion_data - Study completion visit CRF")
    print("   4. data_queries - Query reports for site resolution")
    print("   5. site_summary - Site-level metrics")
    print("   6. query_summary_by_site - Query breakdown by site and type")
    print("\n💡 Next Steps:")
    print("   - Connect PowerBI to visualize data quality metrics")
    print("   - Export query reports to send to sites")
    print("   - Track query resolution status")
    print("   - Analyze screening failures and completion rates")
    print("   - Re-run pipeline after receiving query responses")
    print("="*80)
