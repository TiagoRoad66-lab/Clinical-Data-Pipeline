# Clinical Data Pipeline: Technical Design & Gap Analysis

**Project:** Multi-Site Clinical Data Management System Integration  
**Author:** Tiago Fernandes 
**Date:** October 2025  
**Version:** 1.0  
**Purpose:** Portfolio demonstration with production-readiness analysis

---

## Executive Summary

This document accompanies a demonstration clinical data pipeline project that simulates multi-site trial data collection, quality management, and query tracking. While the demonstration uses synthetic data and simplified workflows, this document outlines the **architectural considerations**, **production requirements**, and **implementation strategies** necessary for a real-world Clinical Data Management System (CDMS) integration with Electronic Data Capture (EDC) systems.

**Key Insight:** The demonstration project proves **conceptual understanding** of clinical data workflows. This document proves **practical knowledge** of production implementation requirements.

---

## Table of Contents

1. [Current Demo Capabilities](#1-current-demo-capabilities)
2. [Production Environment Requirements](#2-production-environment-requirements)
3. [Gap Analysis](#3-gap-analysis)
4. [Architectural Design Proposals](#4-architectural-design-proposals)
5. [Key Questions for Implementation](#5-key-questions-for-implementation)
6. [Technology Trade-offs](#6-technology-trade-offs)
7. [Regulatory Compliance Considerations](#7-regulatory-compliance-considerations)
8. [Future Enhancements](#8-future-enhancements)

---

## 1. Current Demo Capabilities

### What the Demo Shows

✅ **Core Competencies Demonstrated:**
- Multi-site data generation with realistic variance
- Data quality issue identification (without auto-correction)
- Query generation and tracking system
- Derived variable calculation (Day of Study)
- Relational data modeling across CRF domains
- Flag-based quality control (not correction-based)
- SQL database design with normalized schema
- Cross-site data quality monitoring

### Technology Stack
- **Language:** Python 3.x
- **Data Processing:** Pandas
- **Data Generation:** Faker library
- **Storage:** SQLite
- **Output Format:** SQL tables

### Limitations (By Design)
- Uses synthetic data (not real EDC integration)
- Simplified query workflow (no multi-stakeholder routing)
- No audit trail for data changes
- No SAS output format
- No CDISC SDTM mapping
- No external data import functionality
- No configuration-driven ETL

---

## 2. Production Environment Requirements

### Typical Clinical Data Operations Stack

Based on industry standards for pharmaceutical/biotech clinical trials:

| Component | Typical Production Technology |
|-----------|------------------------------|
| **EDC System** | Medrio, Medidata Rave, Veeva Vault, Oracle Clinical One |
| **CDMS** | SAS-based (custom), Medidata Rave, Oracle Clinical |
| **Programming Language** | SAS (primary), R/Python (secondary) |
| **Data Storage** | SAS datasets (.sas7bdat), Oracle DB, SQL Server |
| **Standards** | CDISC SDTM, ADaM, Define-XML |
| **Validation** | SAS validation scripts, edit checks |
| **Reporting** | SAS, JMP, Spotfire, Tableau |

### Operational Workflow

```
┌─────────────────────────────────────────────────────────────┐
│  Site Data Entry (EDC - Medrio)                             │
└─────────────┬───────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│  API Export (Scheduled/Manual)                               │
│  • Full dumps or incremental                                 │
│  • JSON/XML format                                           │
│  • Authentication via OAuth/API keys                         │
└─────────────┬───────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│  Data Transfer & Validation                                  │
│  • Reconciliation report                                     │
│  • Format validation                                         │
│  • Completeness checks                                       │
└─────────────┬───────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│  ETL Process (Driven by DMP)                                 │
│  • Variable mapping                                          │
│  • Derivations                                               │
│  • Format conversions                                        │
└─────────────┬───────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│  CDMS Raw Data Files (SAS datasets)                          │
│  • One file per CRF × 3 variants:                            │
│    - Raw data (.sas7bdat)                                    │
│    - Audit trail (_audit.sas7bdat)                           │
│    - Record IDs (_recid.sas7bdat)                            │
└─────────────┬───────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│  Data Quality Review                                         │
│  • Automated edit checks                                     │
│  • Manual review                                             │
│  • Query generation                                          │
└─────────────┬───────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│  Query Management & Resolution                               │
│  • Route to clinical team/sites                              │
│  • Track responses                                           │
│  • Apply corrections                                         │
│  • Document audit trail                                      │
└─────────────┬───────────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────────────────────────┐
│  Data Finalization & Lock                                    │
│  • All queries resolved                                      │
│  • Database lock                                             │
│  • SDTM/ADaM generation                                      │
│  • Statistical analysis                                      │
└─────────────────────────────────────────────────────────────┘
```

---

## 3. Gap Analysis

### Critical Gaps Between Demo and Production

| # | Component | Demo Status | Production Requirement | Priority |
|---|-----------|-------------|------------------------|----------|
| 1 | **EDC Integration** | ❌ Synthetic data only | ✅ Medrio API integration | **CRITICAL** |
| 2 | **DMP Configuration** | ❌ Hard-coded logic | ✅ Configuration-driven ETL | **CRITICAL** |
| 3 | **Output Format** | ❌ SQLite tables | ✅ SAS datasets (.sas7bdat) | **CRITICAL** |
| 4 | **Audit Trail** | ❌ No change tracking | ✅ Full audit trail per 21 CFR Part 11 | **CRITICAL** |
| 5 | **File Variants** | ❌ Single file per domain | ✅ Three variants (raw/audit/recid) | **HIGH** |
| 6 | **Query Workflow** | ⚠️ Basic tracking only | ✅ Multi-stakeholder routing & SLA | **HIGH** |
| 7 | **Clinical Requests** | ⚠️ Auto-generated only | ✅ Manual + imports + flags | **HIGH** |
| 8 | **Reconciliation** | ❌ No validation reporting | ✅ Data transfer document | **HIGH** |
| 9 | **CDISC Mapping** | ❌ Custom schema | ✅ SDTM domain structure | **MEDIUM** |
| 10 | **External Imports** | ❌ Not supported | ✅ Lab data, ePRO, imaging | **MEDIUM** |
| 11 | **Validation Scripts** | ❌ No SAS validation | ✅ SAS edit check programs | **MEDIUM** |
| 12 | **User Management** | ❌ No RBAC | ✅ Role-based access control | **LOW** |

---

## 4. Architectural Design Proposals

### 4.1 EDC API Integration

**Requirement:** Pull data from Medrio EDC via RESTful API

**Proposed Architecture:**

```python
# api_connector.py - Production-ready API module

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import logging
from datetime import datetime
from typing import Optional, Dict, List

class MedrioAPIConnector:
    """
    Connects to Medrio EDC API with authentication, retry logic,
    and incremental data pull capabilities.
    """
    
    def __init__(self, config: Dict):
        """
        Initialize API connector with configuration
        
        Args:
            config: Dictionary containing:
                - base_url: Medrio API endpoint
                - api_key: Authentication key
                - api_secret: Authentication secret
                - timeout: Request timeout in seconds
                - max_retries: Maximum retry attempts
        """
        self.base_url = config['base_url']
        self.api_key = config['api_key']
        self.api_secret = config['api_secret']
        self.timeout = config.get('timeout', 30)
        self.session = self._create_session(config.get('max_retries', 3))
        self.logger = logging.getLogger(__name__)
    
    def _create_session(self, max_retries: int) -> requests.Session:
        """Create session with retry strategy"""
        session = requests.Session()
        retry_strategy = Retry(
            total=max_retries,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("https://", adapter)
        return session
    
    def authenticate(self) -> str:
        """
        Authenticate and retrieve access token
        
        Returns:
            Access token for subsequent API calls
        """
        # Implementation depends on Medrio's OAuth flow
        pass
    
    def pull_form_data(
        self, 
        study_id: str, 
        form_oid: str, 
        since_date: Optional[datetime] = None,
        subjects: Optional[List[str]] = None
    ) -> Dict:
        """
        Pull CRF data for specific form
        
        Args:
            study_id: Study identifier in Medrio
            form_oid: Form OID from Medrio metadata
            since_date: Pull only data modified after this date (incremental)
            subjects: Optional list of subject IDs to pull (for selective refresh)
            
        Returns:
            Dictionary containing form data and metadata
        """
        # Implementation with pagination handling
        pass
    
    def get_audit_trail(self, study_id: str, record_id: str) -> List[Dict]:
        """
        Retrieve audit trail for specific record
        
        Args:
            study_id: Study identifier
            record_id: Unique record identifier
            
        Returns:
            List of audit trail entries
        """
        pass
```

**Key Design Decisions:**

1. **Retry Logic:** Use exponential backoff for failed requests
2. **Incremental Pulls:** Support `since_date` parameter to avoid full refreshes
3. **Rate Limiting:** Respect API rate limits with proper delays
4. **Error Handling:** Catch and log all API errors with context
5. **Authentication:** Store tokens securely, refresh before expiration

**Questions to Ask Before Implementation:**
- What is Medrio's API rate limit?
- Does Medrio support incremental exports (delta)?
- What authentication method is used (OAuth 2.0, API keys)?
- What is the response format (JSON, XML)?
- Are there sandbox/test environments available?
- What is the API versioning strategy?

---

### 4.2 Data Management Plan (DMP) Configuration System

**Requirement:** Configuration-driven ETL that adapts to protocol amendments

**Proposed Architecture:**

```yaml
# dmp_config.yaml - Study-specific configuration

study:
  id: "PROTO-2025-001"
  name: "Phase II Oncology Trial"
  version: "2.0"
  effective_date: "2025-01-15"

global_settings:
  cdms_variable_length_max: 8  # SAS legacy compatibility
  date_format: "ISO8601"
  missing_value_codes: ["-", "NA", "N/A", "UNK"]
  controlled_terminology_version: "CDISC_CT_2024-09-27"

forms:
  demographics:
    medrio_form_oid: "DM_FORM_V2"
    medrio_form_name: "Demographics"
    cdms_domain: "DM"
    output_dataset: "dm_raw"
    
    fields:
      - source_field: "dm_subjid"
        cdms_variable: "SUBJID"
        label: "Subject Identifier"
        type: "character"
        length: 12
        required: true
        primary_key: true
        
      - source_field: "dm_sex_coded"
        cdms_variable: "SEX"
        label: "Sex"
        type: "numeric"
        length: 8
        format: "SEX."
        required: true
        controlled_terminology:
          1: "Male"
          2: "Female"
          9: "Unknown"
        edit_checks:
          - type: "range"
            min: 1
            max: 9
            severity: "ERROR"
          - type: "codelist"
            allowed_values: [1, 2, 9]
            severity: "ERROR"
      
      - source_field: "dm_birthdate"
        cdms_variable: "BRTHDT"
        label: "Date of Birth"
        type: "date"
        length: 8
        format: "DATE9."
        required: true
        derivations:
          - target_variable: "AGE"
            formula: "floor((RFSTDTC - BRTHDT) / 365.25)"
            label: "Age at First Dose"
        edit_checks:
          - type: "date_logic"
            rule: "BRTHDT < today()"
            message: "Birth date cannot be in the future"
            severity: "ERROR"
          - type: "date_range"
            min_date: "1950-01-01"
            max_date: "2024-12-31"
            severity: "WARNING"

  vital_signs:
    medrio_form_oid: "VS_FORM_V2"
    medrio_form_name: "Vital Signs"
    cdms_domain: "VS"
    output_dataset: "vs_raw"
    repeating: true
    
    fields:
      - source_field: "vs_temp_c"
        cdms_variable: "VSTEMP"
        label: "Temperature (Celsius)"
        type: "numeric"
        length: 8
        format: "8.1"
        required: false
        edit_checks:
          - type: "range"
            min: 35.0
            max: 42.0
            severity: "ERROR"
          - type: "range"
            min: 36.0
            max: 39.0
            severity: "WARNING"
            query_text: "Temperature out of expected range. Please verify."
          - type: "missing_comment"
            condition: "VSTEMP < 36.0 OR VSTEMP > 39.0"
            required_field: "vs_comment"
            severity: "ERROR"
            query_text: "Comment required for out-of-range temperature."

derived_variables:
  - variable: "STUDYDAY"
    label: "Study Day"
    formula: "(visit_date - first_dose_date)"
    note: "Day 0 = first dose date"
    applies_to: ["VS", "AE", "CM", "EX"]
```

**Implementation:**

```python
# dmp_processor.py

import yaml
from typing import Dict, Any
import pandas as pd

class DMPProcessor:
    """
    Processes data according to DMP specifications.
    Configuration-driven to adapt to protocol amendments.
    """
    
    def __init__(self, dmp_config_path: str):
        """Load and validate DMP configuration"""
        with open(dmp_config_path, 'r') as f:
            self.config = yaml.safe_load(f)
        self._validate_config()
    
    def _validate_config(self):
        """Validate DMP configuration structure"""
        required_keys = ['study', 'global_settings', 'forms']
        for key in required_keys:
            if key not in self.config:
                raise ValueError(f"DMP config missing required key: {key}")
    
    def transform_form_data(
        self, 
        source_df: pd.DataFrame, 
        form_name: str
    ) -> pd.DataFrame:
        """
        Transform source data according to DMP mappings
        
        Args:
            source_df: Raw data from EDC
            form_name: Form identifier in DMP config
            
        Returns:
            Transformed DataFrame ready for CDMS
        """
        form_config = self.config['forms'][form_name]
        target_df = pd.DataFrame()
        
        # Apply field mappings
        for field in form_config['fields']:
            source_col = field['source_field']
            target_col = field['cdms_variable']
            
            if source_col in source_df.columns:
                target_df[target_col] = source_df[source_col]
                
                # Apply type conversions
                if field['type'] == 'date':
                    target_df[target_col] = pd.to_datetime(target_df[target_col])
                elif field['type'] == 'numeric':
                    target_df[target_col] = pd.to_numeric(
                        target_df[target_col], 
                        errors='coerce'
                    )
                
                # Apply controlled terminology mappings
                if 'controlled_terminology' in field:
                    # Map codes to labels if needed
                    pass
        
        # Calculate derived variables
        if 'derivations' in form_config:
            target_df = self._apply_derivations(target_df, form_config)
        
        return target_df
    
    def apply_edit_checks(
        self, 
        df: pd.DataFrame, 
        form_name: str
    ) -> pd.DataFrame:
        """
        Run edit checks and generate query DataFrame
        
        Args:
            df: Data to validate
            form_name: Form identifier
            
        Returns:
            DataFrame of generated queries
        """
        queries = []
        form_config = self.config['forms'][form_name]
        
        for field in form_config['fields']:
            if 'edit_checks' not in field:
                continue
                
            for check in field['edit_checks']:
                # Implement each check type
                if check['type'] == 'range':
                    queries.extend(
                        self._check_range(df, field, check)
                    )
                elif check['type'] == 'date_logic':
                    queries.extend(
                        self._check_date_logic(df, field, check)
                    )
                # ... other check types
        
        return pd.DataFrame(queries)
```

**Benefits:**
- Protocol amendments only require YAML changes, not code changes
- Version control of DMP configurations
- Easy to review mappings with clinical team
- Supports multiple study versions simultaneously

---

### 4.3 SAS Dataset Output

**Requirement:** Export data as SAS datasets with proper metadata

**Proposed Implementation:**

```python
# sas_exporter.py

import pyreadstat
import pandas as pd
from typing import Dict, Optional
from pathlib import Path

class SASDatasetExporter:
    """
    Export DataFrames to SAS datasets (.sas7bdat) with proper metadata.
    Generates three variants per CRF: raw, audit, and record ID.
    """
    
    def __init__(self, output_dir: Path, dmp_config: Dict):
        self.output_dir = Path(output_dir)
        self.dmp_config = dmp_config
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def export_raw_data(
        self,
        df: pd.DataFrame,
        dataset_name: str,
        form_config: Dict
    ) -> Path:
        """
        Export raw data variant with variable labels and formats
        
        Args:
            df: DataFrame to export
            dataset_name: Name of SAS dataset (e.g., 'dm_raw')
            form_config: Form configuration from DMP
            
        Returns:
            Path to created SAS dataset
        """
        # Prepare metadata
        variable_labels = {}
        variable_formats = {}
        
        for field in form_config['fields']:
            var_name = field['cdms_variable']
            variable_labels[var_name] = field['label']
            if 'format' in field:
                variable_formats[var_name] = field['format']
        
        # Ensure SAS-compatible column names (max 8 chars for legacy)
        df_export = df.copy()
        if self.dmp_config['global_settings']['cdms_variable_length_max'] == 8:
            df_export.columns = [col[:8].upper() for col in df_export.columns]
        
        # Export to SAS
        output_path = self.output_dir / f"{dataset_name}.sas7bdat"
        pyreadstat.write_sas7bdat(
            df_export,
            str(output_path),
            column_labels=variable_labels,
            variable_value_labels=variable_formats
        )
        
        return output_path
    
    def export_audit_trail(
        self,
        audit_df: pd.DataFrame,
        dataset_name: str
    ) -> Path:
        """
        Export audit trail variant
        
        Standard audit columns:
        - RECORDID: Link to raw data record
        - FIELDNAME: Variable that was changed
        - OLDVALUE: Previous value
        - NEWVALUE: Current value
        - CHANGEREASON: Reason for change
        - CHANGEDBY: User who made change
        - CHANGEDDATE: Timestamp of change
        - REVIEWEDBY: User who reviewed change
        - REVIEWDATE: Timestamp of review
        """
        output_path = self.output_dir / f"{dataset_name}_audit.sas7bdat"
        
        audit_labels = {
            'RECORDID': 'Record Identifier',
            'FIELDNAME': 'Field Name',
            'OLDVALUE': 'Previous Value',
            'NEWVALUE': 'New Value',
            'CHANGEREASON': 'Reason for Change',
            'CHANGEDBY': 'Changed By User',
            'CHANGEDDATE': 'Date/Time of Change',
            'REVIEWEDBY': 'Reviewed By User',
            'REVIEWDATE': 'Date/Time of Review'
        }
        
        pyreadstat.write_sas7bdat(
            audit_df,
            str(output_path),
            column_labels=audit_labels
        )
        
        return output_path
    
    def export_record_ids(
        self,
        recid_df: pd.DataFrame,
        dataset_name: str
    ) -> Path:
        """
        Export record ID variant for linking queries and corrections
        
        Standard columns:
        - RECORDID: Unique record identifier
        - SUBJID: Subject ID
        - FORMOID: Form OID from EDC
        - INSTANCENUM: Instance number for repeating forms
        - EDCKEY: Original EDC system key
        """
        output_path = self.output_dir / f"{dataset_name}_recid.sas7bdat"
        
        recid_labels = {
            'RECORDID': 'Record Identifier',
            'SUBJID': 'Subject Identifier',
            'FORMOID': 'Form OID',
            'INSTANCENUM': 'Instance Number',
            'EDCKEY': 'EDC System Key'
        }
        
        pyreadstat.write_sas7bdat(
            recid_df,
            str(output_path),
            column_labels=recid_labels
        )
        
        return output_path
    
    def generate_sas_validation_script(
        self,
        dataset_name: str,
        form_config: Dict
    ) -> Path:
        """
        Generate SAS program to validate imported data
        
        Creates .sas file with:
        - PROC CONTENTS (metadata verification)
        - PROC MEANS (range checks)
        - DATA step validation (edit checks)
        """
        sas_code = f"""
/******************************************************************************
* Program: validate_{dataset_name}.sas
* Purpose: Validate {dataset_name} dataset after import
* Generated: {pd.Timestamp.now()}
******************************************************************************/

/* Set library */
libname cdms "path/to/cdms";

/* Verify dataset structure */
proc contents data=cdms.{dataset_name} varnum;
run;

/* Check numeric ranges */
proc means data=cdms.{dataset_name} n nmiss min max mean std;
    var _numeric_;
run;

/* Custom edit checks */
data validation_flags;
    set cdms.{dataset_name};
    
"""
        
        # Add edit checks from DMP
        for field in form_config['fields']:
            if 'edit_checks' not in field:
                continue
            
            var_name = field['cdms_variable']
            for check in field['edit_checks']:
                if check['type'] == 'range':
                    sas_code += f"""
    /* Range check for {var_name} */
    if {var_name} < {check['min']} or {var_name} > {check['max']} then do;
        put "ERROR: {var_name} out of range for record " RECORDID=;
        flag_{var_name}_range = 1;
    end;
"""
        
        sas_code += """
run;

/* Generate validation report */
proc freq data=validation_flags;
    tables flag_: / missing;
run;
"""
        
        script_path = self.output_dir / f"validate_{dataset_name}.sas"
        script_path.write_text(sas_code)
        
        return script_path
```

**Key Considerations:**
- SAS variable names limited to 8 characters in legacy systems (32 in modern SAS)
- Must include variable labels and formats
- Date formats must be SAS-compatible (DATE9., DATETIME20., etc.)
- Generate validation scripts for biostatistics team

---

### 4.4 Audit Trail Implementation

**Requirement:** Track all data changes for regulatory compliance

**Proposed Schema:**

```sql
-- audit_trail table structure

CREATE TABLE audit_trail (
    audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    record_id VARCHAR(50) NOT NULL,              -- Links to source record
    domain VARCHAR(10) NOT NULL,                  -- CRF domain (DM, VS, AE, etc.)
    subject_id VARCHAR(20) NOT NULL,              -- Subject identifier
    site_id VARCHAR(10) NOT NULL,                 -- Site identifier
    field_name VARCHAR(50) NOT NULL,              -- Variable that changed
    old_value TEXT,                               -- Previous value (NULL if new record)
    new_value TEXT,                               -- Current value
    change_type VARCHAR(20) NOT NULL,             -- INSERT, UPDATE, DELETE
    change_reason TEXT,                           -- Reason code or free text
    changed_by_user VARCHAR(50) NOT NULL,         -- Username
    changed_by_role VARCHAR(50),                  -- User role at time of change
    changed_datetime TIMESTAMP NOT NULL,          -- When change occurred
    reviewed_by_user VARCHAR(50),                 -- QC reviewer
    reviewed_datetime TIMESTAMP,                  -- When reviewed
    review_status VARCHAR(20),                    -- PENDING, APPROVED, REJECTED
    electronic_signature VARCHAR(255),            -- Hash of change for Part 11
    query_id VARCHAR(20),                         -- Associated query if applicable
    import_batch_id VARCHAR(50),                  -- If part of batch import
    comments TEXT,                                -- Additional context
    
    -- Metadata
    created_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    modified_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Indexes for performance
    INDEX idx_record_id (record_id),
    INDEX idx_subject_id (subject_id),
    INDEX idx_changed_datetime (changed_datetime),
    INDEX idx_query_id (query_id)
);
```

**Implementation:**

```python
# audit_trail.py

from datetime import datetime
from typing import Optional, Any
import hashlib
import pandas as pd

class AuditTrailManager:
    """
    Manage audit trail for all data changes.
    Ensures 21 CFR Part 11 compliance.
    """
    
    def log_change(
        self,
        record_id: str,
        domain: str,
        subject_id: str,
        site_id: str,
        field_name: str,
        old_value: Any,
        new_value: Any,
        change_reason: str,
        changed_by_user: str,
        changed_by_role: str,
        query_id: Optional[str] = None
    ) -> str:
        """
        Log a data change to audit trail
        
        Returns:
            Audit ID of created record
        """
        audit_entry = {
            'record_id': record_id,
            'domain': domain,
            'subject_id': subject_id,
            'site_id': site_id,
            'field_name': field_name,
            'old_value': str(old_value) if old_value is not None else None,
            'new_value': str(new_value) if new_value is not None else None,
            'change_type': 'INSERT' if old_value is None else 'UPDATE',
            'change_reason': change_reason,
            'changed_by_user': changed_by_user,
            'changed_by_role': changed_by_role,
            'changed_datetime': datetime.now(),
            'query_id': query_id,
            'review_status': 'PENDING',
            'electronic_signature': self._generate_signature(
                record_id, field_name, old_value, new_value, changed_by_user
            )
        }
        
        # Insert into database
        audit_id = self._insert_audit_record(audit_entry)
        return audit_id
    
    def _generate_signature(
        self,
        record_id: str,
        field_name: str,
        old_value: Any,
        new_value: Any,
        user: str
    ) -> str:
        """
        Generate electronic signature hash for 21 CFR Part 11 compliance
        """
        signature_string = f"{record_id}|{field_name}|{old_value}|{new_value}|{user}|{datetime.now().isoformat()}"
        return hashlib.sha256(signature_string.encode()).hexdigest()
    
    def get_record_history(self, record_id: str) -> pd.DataFrame:
        """
        Retrieve complete audit trail for a specific record
        """
        query = """
        SELECT * FROM audit_trail 
        WHERE record_id = ?
        ORDER BY changed_datetime ASC
        """
        # Execute query and return DataFrame
        pass
    
    def get_subject_changes(
        self,
        subject_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> pd.DataFrame:
        """
        Retrieve all changes for a subject within date range
        """
        pass
```

---

### 4.5 Clinical Request Workflow System

**Requirement:** Handle multiple types of clinical requests with routing and SLA tracking

**Proposed Architecture:**

```python
# clinical_requests.py

from enum import Enum
from datetime import datetime, timedelta
from typing import List, Optional
import pandas as pd

class RequestType(Enum):
    """Types of clinical requests"""
    QUERY = "Query"                          # Data clarification query
    CORRECTION = "Correction"                # Direct data correction
    IMPORT = "Import"                        # External data import (labs, ePRO)
    FLAG = "Flag"                            # Protocol deviation, exclusion flag
    DEVIATION = "Protocol Deviation"         # Protocol violation documentation
    SAE = "Serious Adverse Event"            # Expedited SAE reporting

class RequestPriority(Enum):
    """Priority levels for requests"""
    CRITICAL = "Critical"     # Safety-related, requires immediate action
    HIGH = "High"            # Impacts analysis, resolve within 48h
    NORMAL = "Normal"        # Standard query, resolve within 5 days
    LOW = "Low"              # Nice to have, no deadline

class RequestStatus(Enum):
    """Workflow status"""
    DRAFT = "Draft"
    SUBMITTED = "Submitted"
    ASSIGNED = "Assigned"
    IN_REVIEW = "In Review"
    PENDING_SITE = "Pending Site Response"
    RESOLVED = "Resolved"
    CLOSED = "Closed"
    CANCELLED = "Cancelled"

class ClinicalRequest:
    """
    Represents a clinical request with full workflow tracking
    """
    
    def __init__(
        self,
        request_type: RequestType,
        priority: RequestPriority,
        subject_id: str,
        site_id: str,
        domain: str,
        field_name: Optional[str] = None,
        issue_description: str = "",
        created_by: str = ""
    ):
        self.request_id = self._generate_request_id()
        self.request_type = request_type
        self.priority = priority
        self.status = RequestStatus.DRAFT
        self.subject_id = subject_id
        self.site_id = site_id
        self.domain = domain
        self.field_name = field_name
        self.issue_description = issue_description
        self.created_by = created_by
        self.created_date = datetime.now()
        self.assigned_to = None
        self.sla_deadline = self._calculate_sla()
        self.resolution_notes = None
        self.resolved_by = None
        self.resolved_date = None
        
    def _generate_request_id(self) -> str:
        """Generate unique request ID"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        return f"REQ_{timestamp}"
    
    def _calculate_sla(self) -> datetime:
        """Calculate SLA deadline based on priority"""
        sla_hours = {
            RequestPriority.CRITICAL: 4,
            RequestPriority.HIGH: 48,
            RequestPriority.NORMAL: 120,  # 5 days
            RequestPriority.LOW: 240      # 10 days
        }
        hours = sla_hours.get(self.priority, 120)
        return self.created_date + timedelta(hours=hours)
    
    def assign_to(self, user: str, role: str):
        """Assign request to user"""
        self.assigned_to = user
        self.assigned_role = role
        self.status = RequestStatus.ASSIGNED
        self.assigned_date = datetime.now()
    
    def submit_to_site(self, query_text: str):
        """Submit query to site for response"""
        self.query_text = query_text
        self.status = RequestStatus.PENDING_SITE
        self.submitted_to_site_date = datetime.now()
    
    def resolve(self, resolution_notes: str, resolved_by: str):
        """Mark request as resolved"""
        self.resolution_notes = resolution_notes
        self.resolved_by = resolved_by
        self.resolved_date = datetime.now()
        self.status = RequestStatus.RESOLVED
    
    def close(self, closed_by: str):
        """Close request after QC review"""
        self.closed_by = closed_by
        self.closed_date = datetime.now()
        self.status = RequestStatus.CLOSED
    
    def is_overdue(self) -> bool:
        """Check if request has exceeded SLA"""
        if self.status in [RequestStatus.RESOLVED, RequestStatus.CLOSED, RequestStatus.CANCELLED]:
            return False
        return datetime.now() > self.sla_deadline

class ClinicalRequestManager:
    """
    Manages clinical request workflow with routing and tracking
    """
    
    def __init__(self, db_connection):
        self.db = db_connection
        self.routing_rules = self._load_routing_rules()
    
    def _load_routing_rules(self) -> dict:
        """
        Load routing rules for request assignment
        
        Example:
        - SAE requests → Medical Monitor
        - Lab import requests → Data Manager
        - Site queries → CRA for that site
        """
        return {
            RequestType.SAE: {'role': 'Medical Monitor', 'notify_immediately': True},
            RequestType.IMPORT: {'role': 'Data Manager', 'notify_immediately': False},
            RequestType.QUERY: {'role': 'CRA', 'route_by_site': True},
            RequestType.FLAG: {'role': 'Clinical Lead', 'notify_immediately': False}
        }
    
    def create_request(self, request: ClinicalRequest) -> str:
        """
        Create new clinical request and route according to rules
        """
        # Auto-assign based on routing rules
        routing_rule = self.routing_rules.get(request.request_type)
        if routing_rule:
            assigned_user = self._get_user_by_role(
                routing_rule['role'], 
                request.site_id if routing_rule.get('route_by_site') else None
            )
            request.assign_to(assigned_user, routing_rule['role'])
            
            # Send notifications
            if routing_rule.get('notify_immediately'):
                self._send_urgent_notification(request)
        
        # Save to database
        request_id = self._save_request(request)
        return request_id
    
    def get_overdue_requests(self) -> List[ClinicalRequest]:
        """Retrieve all overdue requests"""
        query = """
        SELECT * FROM clinical_requests
        WHERE status NOT IN ('RESOLVED', 'CLOSED', 'CANCELLED')
        AND sla_deadline < ?
        """
        # Execute and return
        pass
    
    def get_requests_by_site(self, site_id: str) -> pd.DataFrame:
        """Get all requests for a specific site"""
        pass
    
    def generate_sla_report(self) -> pd.DataFrame:
        """
        Generate SLA compliance report
        
        Returns DataFrame with:
        - Total requests by priority
        - % resolved within SLA
        - Average resolution time
        - Currently overdue requests
        """
        pass
    
    def bulk_import_external_data(
        self,
        data_source: str,
        data_df: pd.DataFrame,
        import_mapping: dict
    ) -> str:
        """
        Handle bulk import of external data (labs, ePRO, imaging)
        
        Creates import request and validates data before loading
        """
        import_request = ClinicalRequest(
            request_type=RequestType.IMPORT,
            priority=RequestPriority.NORMAL,
            subject_id="MULTIPLE",
            site_id="CENTRAL_LAB",
            domain=data_source,
            issue_description=f"Bulk import from {data_source}: {len(data_df)} records",
            created_by="system"
        )
        
        # Validate import data
        validation_results = self._validate_import_data(data_df, import_mapping)
        
        if validation_results['errors']:
            import_request.status = RequestStatus.PENDING_SITE
            import_request.resolution_notes = f"Validation failed: {validation_results['errors']}"
        else:
            # Load data
            self._load_import_data(data_df, import_mapping)
            import_request.resolve(
                f"Successfully imported {len(data_df)} records",
                "system"
            )
        
        self.create_request(import_request)
        return import_request.request_id
```

---

### 4.6 Data Reconciliation and Transfer Validation

**Requirement:** Validate data transfer completeness before CDMS load

**Proposed Implementation:**

```python
# reconciliation.py

import pandas as pd
from typing import Dict, List, Tuple
from datetime import datetime

class DataReconciliationEngine:
    """
    Validates data transfer between EDC and CDMS.
    Generates Data Transfer Document (DTD) for sign-off.
    """
    
    def reconcile_transfer(
        self,
        source_data: Dict[str, pd.DataFrame],  # EDC data by form
        target_data: Dict[str, pd.DataFrame],  # CDMS data by form
        transfer_id: str
    ) -> Dict:
        """
        Perform complete reconciliation of data transfer
        
        Returns:
            Dictionary containing reconciliation report
        """
        report = {
            'transfer_id': transfer_id,
            'transfer_date': datetime.now(),
            'overall_status': 'PASS',
            'checks_performed': [],
            'discrepancies': []
        }
        
        # Check 1: Record count reconciliation
        count_check = self._reconcile_record_counts(source_data, target_data)
        report['checks_performed'].append(count_check)
        if not count_check['passed']:
            report['overall_status'] = 'FAIL'
            report['discrepancies'].extend(count_check['issues'])
        
        # Check 2: Subject-level reconciliation
        subject_check = self._reconcile_subjects(source_data, target_data)
        report['checks_performed'].append(subject_check)
        if not subject_check['passed']:
            report['overall_status'] = 'FAIL'
            report['discrepancies'].extend(subject_check['issues'])
        
        # Check 3: Data completeness
        completeness_check = self._check_mandatory_fields(target_data)
        report['checks_performed'].append(completeness_check)
        if not completeness_check['passed']:
            report['overall_status'] = 'WARN'
            report['discrepancies'].extend(completeness_check['issues'])
        
        # Check 4: Date logic validation
        date_check = self._validate_date_logic(target_data)
        report['checks_performed'].append(date_check)
        if not date_check['passed']:
            report['overall_status'] = 'FAIL'
            report['discrepancies'].extend(date_check['issues'])
        
        # Check 5: Cross-form consistency
        consistency_check = self._check_cross_form_consistency(target_data)
        report['checks_performed'].append(consistency_check)
        if not consistency_check['passed']:
            report['overall_status'] = 'WARN'
            report['discrepancies'].extend(consistency_check['issues'])
        
        # Check 6: Duplicate detection
        duplicate_check = self._detect_duplicates(target_data)
        report['checks_performed'].append(duplicate_check)
        if not duplicate_check['passed']:
            report['overall_status'] = 'FAIL'
            report['discrepancies'].extend(duplicate_check['issues'])
        
        return report
    
    def _reconcile_record_counts(
        self,
        source_data: Dict[str, pd.DataFrame],
        target_data: Dict[str, pd.DataFrame]
    ) -> Dict:
        """Compare record counts between source and target"""
        issues = []
        
        for form_name in source_data.keys():
            source_count = len(source_data[form_name])
            target_count = len(target_data.get(form_name, pd.DataFrame()))
            
            if source_count != target_count:
                issues.append({
                    'form': form_name,
                    'issue_type': 'RECORD_COUNT_MISMATCH',
                    'source_count': source_count,
                    'target_count': target_count,
                    'difference': source_count - target_count
                })
        
        return {
            'check_name': 'Record Count Reconciliation',
            'passed': len(issues) == 0,
            'issues': issues
        }
    
    def _reconcile_subjects(
        self,
        source_data: Dict[str, pd.DataFrame],
        target_data: Dict[str, pd.DataFrame]
    ) -> Dict:
        """Verify all subjects transferred correctly"""
        issues = []
        
        # Get unique subjects from demographics
        source_subjects = set(source_data['demographics']['subject_id'])
        target_subjects = set(target_data['demographics']['SUBJID'])
        
        missing_in_target = source_subjects - target_subjects
        extra_in_target = target_subjects - source_subjects
        
        if missing_in_target:
            issues.append({
                'issue_type': 'MISSING_SUBJECTS',
                'count': len(missing_in_target),
                'subject_ids': list(missing_in_target)
            })
        
        if extra_in_target:
            issues.append({
                'issue_type': 'EXTRA_SUBJECTS',
                'count': len(extra_in_target),
                'subject_ids': list(extra_in_target)
            })
        
        return {
            'check_name': 'Subject Reconciliation',
            'passed': len(issues) == 0,
            'issues': issues
        }
    
    def _check_mandatory_fields(self, target_data: Dict[str, pd.DataFrame]) -> Dict:
        """Check completeness of mandatory fields"""
        issues = []
        
        mandatory_fields = {
            'demographics': ['SUBJID', 'SEX', 'BRTHDT'],
            'dosing': ['SUBJID', 'EXSTDTC'],
            'vital_signs': ['SUBJID', 'VSDTC', 'VSTEST']
        }
        
        for form, fields in mandatory_fields.items():
            if form not in target_data:
                continue
            
            df = target_data[form]
            for field in fields:
                if field in df.columns:
                    missing_count = df[field].isna().sum()
                    if missing_count > 0:
                        issues.append({
                            'form': form,
                            'field': field,
                            'issue_type': 'MANDATORY_FIELD_MISSING',
                            'missing_count': missing_count,
                            'missing_percentage': (missing_count / len(df)) * 100
                        })
        
        return {
            'check_name': 'Mandatory Field Completeness',
            'passed': len(issues) == 0,
            'issues': issues
        }
    
    def _validate_date_logic(self, target_data: Dict[str, pd.DataFrame]) -> Dict:
        """Validate date relationships"""
        issues = []
        
        # Example: Birth date < Screening date < Enrollment < First dose
        if 'demographics' in target_data and 'dosing' in target_data:
            # Merge to check logic
            merged = target_data['demographics'].merge(
                target_data['dosing'],
                on='SUBJID'
            )
            
            # Check birth date < first dose
            invalid = merged[merged['BRTHDT'] >= merged['EXSTDTC']]
            if len(invalid) > 0:
                issues.append({
                    'issue_type': 'DATE_LOGIC_VIOLATION',
                    'rule': 'Birth date must precede first dose date',
                    'violation_count': len(invalid),
                    'affected_subjects': invalid['SUBJID'].tolist()
                })
        
        return {
            'check_name': 'Date Logic Validation',
            'passed': len(issues) == 0,
            'issues': issues
        }
    
    def _check_cross_form_consistency(self, target_data: Dict[str, pd.DataFrame]) -> Dict:
        """Check consistency across forms"""
        issues = []
        
        # Example: Demographics sex should match adverse events sex
        if 'demographics' in target_data and 'adverse_events' in target_data:
            dm_sex = target_data['demographics'][['SUBJID', 'SEX']].drop_duplicates()
            ae_sex = target_data['adverse_events'][['SUBJID', 'SEX']].drop_duplicates()
            
            merged = dm_sex.merge(ae_sex, on='SUBJID', suffixes=('_DM', '_AE'))
            inconsistent = merged[merged['SEX_DM'] != merged['SEX_AE']]
            
            if len(inconsistent) > 0:
                issues.append({
                    'issue_type': 'CROSS_FORM_INCONSISTENCY',
                    'fields': 'SEX (Demographics vs Adverse Events)',
                    'inconsistent_count': len(inconsistent),
                    'affected_subjects': inconsistent['SUBJID'].tolist()
                })
        
        return {
            'check_name': 'Cross-Form Consistency',
            'passed': len(issues) == 0,
            'issues': issues
        }
    
    def _detect_duplicates(self, target_data: Dict[str, pd.DataFrame]) -> Dict:
        """Detect duplicate records"""
        issues = []
        
        for form_name, df in target_data.items():
            # Define key columns for duplicate check
            key_cols = ['SUBJID']
            if 'VISITNUM' in df.columns:
                key_cols.append('VISITNUM')
            
            duplicates = df[df.duplicated(subset=key_cols, keep=False)]
            if len(duplicates) > 0:
                issues.append({
                    'form': form_name,
                    'issue_type': 'DUPLICATE_RECORDS',
                    'duplicate_count': len(duplicates),
                    'affected_records': duplicates[key_cols].to_dict('records')
                })
        
        return {
            'check_name': 'Duplicate Detection',
            'passed': len(issues) == 0,
            'issues': issues
        }
    
    def generate_dtd(self, reconciliation_report: Dict) -> str:
        """
        Generate Data Transfer Document for sign-off
        
        Returns:
            Path to generated PDF report
        """
        # Implementation would create formatted PDF with:
        # - Transfer summary
        # - All checks performed
        # - Pass/Fail status
        # - Discrepancy details
        # - Signature blocks for DM and Biostat
        pass
```

---

## 5. Key Questions for Implementation

### Questions to Ask BEFORE Starting Development

#### **EDC Integration Questions:**
1. What is the Medrio API endpoint and authentication method?
2. What is the API rate limit? Can we batch requests?
3. Does Medrio support incremental exports (delta) or only full dumps?
4. What is the response format (JSON/XML) and schema?
5. Are there test/sandbox environments for development?
6. What is the typical data volume per export?
7. How are repeating forms handled in the API response?
8. What metadata is included (audit trail, user info, timestamps)?

#### **DMP Configuration Questions:**
1. Who maintains the DMP? (Data Manager, Biostatistics, IT?)
2. How often do protocol amendments occur?
3. What is the process for DMP version control?
4. Are there templates/standards for variable naming?
5. Which CDISC controlled terminology version is used?
6. How are derived variables documented?
7. What edit check specifications exist?
8. Who signs off on DMP changes?

#### **SAS Environment Questions:**
1. What version of SAS is being used?
2. Are there variable name length restrictions (8-char legacy)?
3. What SAS formats/libraries are available?
4. Where are SAS datasets stored (network path, database)?
5. Who has access to run SAS programs?
6. Are there SAS macro libraries we should use?
7. What validation scripts already exist?

#### **Workflow Questions:**
1. Who are the key stakeholders (CRA, DM, Medical Monitor, Biostat)?
2. What is the escalation path for critical issues?
3. What are the SLA requirements by priority level?
4. How are queries routed to sites? (Email, portal, EDC system?)
5. What approval workflows exist for data corrections?
6. How are protocol deviations flagged and tracked?
7. Who performs final database lock?

#### **Regulatory Questions:**
1. Is this study FDA-regulated? EMA? Other?
2. What Part 11 requirements apply?
3. Is electronic signature required for data changes?
4. What audit trail detail is required?
5. Are there inspection-readiness requirements?
6. What validation documentation is needed for the ETL process?

---

## 6. Technology Trade-offs

### Python vs SAS for ETL

| Aspect | Python | SAS |
|--------|--------|-----|
| **Pros** | - Modern, flexible<br>- Great libraries (pandas, numpy)<br>- Easy API integration<br>- Version control friendly | - Industry standard in pharma<br>- Built-in validation<br>- Familiar to biostat teams<br>- Regulatory acceptance |
| **Cons** | - Requires training for SAS users<br>- Need pyreadstat for SAS output<br>- Less common in legacy systems | - Expensive licensing<br>- Less flexible for APIs<br>- Harder to version control<br>- Steeper learning curve |
| **Recommendation** | Use Python for ETL, output to SAS datasets | Use Python for ETL, output to SAS datasets |

### SQLite vs Enterprise Database

| Aspect | SQLite | PostgreSQL/Oracle |
|--------|--------|-------------------|
| **Pros** | - Zero configuration<br>- Single file<br>- Perfect for demos<br>- Portable | - Multi-user<br>- Better performance<br>- Transaction support<br>- Backup/recovery |
| **Cons** | - No multi-user concurrency<br>- Limited for production<br>- No user management | - Requires DBA<br>- Infrastructure needed<br>- More complex | **Recommendation** | Demo/development only | Production requirement |

### Configuration: YAML vs Database

| Aspect | YAML Files | Database Tables |
|--------|------------|-----------------|
| **Pros** | - Human-readable<br>- Version control<br>- Easy to review<br>- No DB dependency | - Queryable<br>- Multi-user updates<br>- Audit trail<br>- Referential integrity |
| **Cons** | - Manual merging<br>- No validation<br>- Concurrent edit issues | - Requires UI for editing<br>- More complex<br>- DB dependency |
| **Recommendation** | Early development, simple studies | Production, complex studies |

---

## 7. Regulatory Compliance Considerations

### 21 CFR Part 11 Requirements

**Electronic Records:**
- ✅ Audit trail for all data changes
- ✅ Time-stamped entries (UTC preferred)
- ✅ User identification for all actions
- ✅ Ability to generate accurate copies

**Electronic Signatures:**
- ✅ Unique to one individual
- ✅ Cannot be reused or reassigned
- ✅ Cryptographically secure (SHA-256 or better)
- ✅ Linked to record permanently

**System Validation:**
- ✅ IQ/OQ/PQ documentation
- ✅ Test scripts and results
- ✅ Change control procedures
- ✅ Disaster recovery plan

### ICH-GCP Requirements

**Data Management:**
- ✅ Source data verification
- ✅ Query management and resolution
- ✅ Data correction procedures
- ✅ Database lock procedures

**Quality Control:**
- ✅ Edit check specifications
- ✅ Range validation
- ✅ Consistency checks
- ✅ Medical coding

---

## 8. Future Enhancements

### Phase 2: Advanced Features

1. **Machine Learning for Data Quality**
   - Anomaly detection for out-of-range values
   - Predictive models for query generation
   - Pattern recognition for data entry errors

2. **Real-Time Data Monitoring**
   - Live dashboards for enrollment rates
   - Real-time query status
   - Site performance scorecards

3. **CDISC SDTM/ADaM Automation**
   - Automated SDTM mapping
   - Define-XML generation
   - ADaM dataset creation

4. **ePRO Integration**
   - Patient-reported outcomes import
   - Wearable device data integration
   - Real-time safety monitoring

5. **Advanced Reporting**
   - Automated study metrics dashboards
   - Enrollment forecasting
   - Data quality trending

---

## Conclusion

This technical design document demonstrates:

1. **Conceptual Understanding:** The demo project proves grasp of clinical data workflows
2. **Production Readiness:** This document shows knowledge of real-world requirements
3. **Strategic Thinking:** Trade-off analysis shows mature decision-making
4. **Regulatory Awareness:** Compliance considerations show industry knowledge
5. **Adaptability:** Question-first approach shows flexibility to specific environments

**Key Message for Interviewers:**  
*"My demo shows I understand the WHAT of clinical data management. This document shows I understand the HOW and WHY for production implementation. I'm ready to adapt to your specific technology stack and processes."*

---

## Appendix: Additional Resources

### Recommended Reading
- FDA 21 CFR Part 11 Guidance
- ICH-GCP E6(R2) Guidelines
- CDISC SDTM Implementation Guide
- Medrio API Documentation

### Training Needs Assessment
- [ ] Medrio API hands-on training
- [ ] Advanced SAS programming
- [ ] CDISC standards certification
- [ ] Clinical trial operations overview
- [ ] Regulatory compliance workshop

---

**Document Control:**
- Version: 1.0
- Last Updated: October 2025
- Next Review: Upon interview feedback
- Status: Draft for Discussion