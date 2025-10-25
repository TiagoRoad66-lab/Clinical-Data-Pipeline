# Multi-Site Clinical Data Pipeline with Query Management

A Python-based demonstration of clinical data management workflows, simulating realistic multi-site trial operations from data collection through quality control and query resolution. This project showcases understanding of data integrity principles, regulatory compliance requirements, and production-ready architecture for pharmaceutical clinical trials.

---

## 🎯 Project Overview

This pipeline demonstrates a complete clinical data workflow for multi-site trials:

1. **Data Generation**: Simulates Case Report Form (CRF) data from 3 US clinical sites
2. **Quality Control**: Identifies data discrepancies requiring site resolution
3. **Query Management**: Generates actionable query reports (without auto-correction)
4. **Data Wrangling**: Merges multi-domain data with derived variable calculations
5. **Database Output**: Produces analysis-ready datasets with quality flags

### Key Principle: **Identify, Don't Correct**

This project follows Good Clinical Practice (GCP) guidelines: data quality issues are **flagged and queried**, never automatically corrected. All discrepancies require source verification.

---

## 🏥 Clinical Trial Scenario

**Study Type**: Pre-clinical animal study  
**Sites**: 3 US sites (US01, US02, US03)  
**Subjects**: 120 animals  
**CRF Domains**: Screening, Demographics, Dosing, Vital Signs, Study Completion  
**Observations**: 720+ longitudinal measurements  
**Data Quality Issues**: ~77 queries requiring resolution

---

## 📋 Features

### **Realistic Data Quality Issues**
The pipeline intentionally introduces real-world discrepancies:
- Missing required fields (consent signatures, weights)
- Out-of-range vital signs (temperature, heart rate)
- Invalid dates (birth dates in future)
- Protocol deviations (dosing before enrollment)
- Missing required comments for abnormal values
- Positive screening tests (exclusion criteria violations)
- Incomplete study completion data

### **Query Management System**
- Automated query generation with severity classification (Critical/High/Medium)
- Query categorization (Missing Data, Out of Range, Protocol Deviation, etc.)
- NO automatic data correction (follows 21 CFR Part 11 principles)
- Query tracking with status and resolution workflow

### **Multi-Site Complexity**
- Staggered site activation dates
- Variable enrollment rates per site
- Site-specific measurement variations (calibration differences)
- Cross-site data quality monitoring

### **Derived Variables**
- **Day of Study calculation** (Day 0 = first dose date)
- Screening period duration
- Site-level aggregations

### **Database Output**
Six normalized tables in SQLite:
1. `screening_data` - Screening visit CRF
2. `observation_data` - Main dataset with quality flags
3. `completion_data` - Study completion records
4. `data_queries` - Query reports for site resolution
5. `site_summary` - Site-level performance metrics
6. `query_summary_by_site` - Query distribution analysis

---

## 🚀 Quick Start

### Prerequisites

```bash
python 3.8+
pip install -r requirements.txt
```

### Installation

```bash
# Clone the repository
git clone https://github.com/TiagoRoad66-lab/clinical-data-pipeline.git
cd clinical-data-pipeline

# Install dependencies
pip install -r requirements.txt

# Run the pipeline
python clinical_data_pipeline.py
```

### Expected Output

```
================================================================================
 MULTI-SITE CLINICAL DATA PIPELINE WITH QUERY MANAGEMENT
 Simulating realistic data quality issues requiring site resolution
================================================================================

--- 1. Generating Synthetic Multi-Site CRF Data (with quality issues) ---
DM Data Generated: 120 records across 3 sites.
⚠️  Introduced 4 missing Sex values
⚠️  Introduced 2 invalid BirthDates (future dates)

--- 2. Data Quality Check: Generating Query Reports ---
📋 Generated 77 data queries requiring site resolution:
   - Critical: 7
   - High: 4
   - Medium: 66

--- 5. Exporting Data to SQL Database ---
✅ Exported main data to 'observation_data' table
✅ Exported 77 queries to 'data_queries' table
```

---

## 📊 Database Schema

### Main Tables

**screening_data** (120 records)
- Consent status, antigen testing, demographics

**observation_data** (720 records)
- Longitudinal vital signs with quality flags
- Includes `DataQualityFlag` and `FlagReason` columns

**data_queries** (~77 records)
- Query ID, type, severity, query text, status

**completion_data** (120 records)
- Study disposition and final assessments

**site_summary** (3 records)
- Aggregated metrics per site

---

## 💡 Use Cases

### For Data Managers
- Example of systematic data quality checking
- Query generation workflow
- Cross-site monitoring approach

### For Biostatisticians
- Understanding data flags before analysis
- Site-level quality metrics
- Clean vs. flagged data separation

### For Clinical Research
- Protocol deviation identification
- Screening failure tracking
- Query resolution workflow

### For Business Intelligence
Connect to `clinical_data_db.sqlite` with PowerBI/Tableau for:
- Data quality dashboards
- Site performance scorecards
- Query aging reports
- Enrollment tracking

---

## 🏗️ Architecture & Design

### Production Considerations

This demonstration uses simplified tools (Python, SQLite) for portability. For production implementation with Electronic Data Capture (EDC) systems like Medrio and Clinical Data Management Systems (CDMS) using SAS, see:

📄 **[Technical Design Document](docs/technical_design_doc.md)**

The technical design document covers:
- EDC API integration patterns
- Data Management Plan (DMP) configuration systems
- SAS dataset output with proper metadata
- Audit trail implementation (21 CFR Part 11)
- Clinical request workflow management
- CDISC SDTM mapping considerations
- Data reconciliation and validation

### Key Design Decisions

**Why Python?**
- Portable demonstration (no expensive licenses required)
- Easy to showcase on GitHub
- Concepts translate to any language (SAS, R, etc.)

**Why SQLite?**
- Single-file database (easy to share)
- SQL-compatible (concepts apply to Oracle, PostgreSQL, etc.)
- Sufficient for demonstration purposes

**Why No Auto-Correction?**
- Regulatory compliance (21 CFR Part 11, ICH-GCP)
- Data integrity principles
- Audit trail requirements
- Source verification necessity

---

## 📂 Project Structure

```
clinical-data-pipeline/
├── clinical_data_pipeline.py          # Main pipeline script
├── requirements.txt                   # Python dependencies
├── README.md                          # This file
├── LICENSE                            # MIT License
├── clinical_data_db.sqlite            # Output database (generated)
└── docs/
    └── technical_design_document.md   # Production architecture guide
```

---

## 🔬 Sample Queries Generated

| Query Type | Example |
|------------|---------|
| **Missing Data** | "Please provide the sex for US0105" |
| **Protocol Violation** | "Subject US0142 has dosing date before enrollment. Please verify." |
| **Out of Range** | "Temperature of 40.5°C for US0233 at Visit 3 is outside expected range. Please verify and provide clinical explanation." |
| **Inclusion/Exclusion** | "Subject US0178 has positive Leishmania test. Please verify if subject meets inclusion criteria." |
| **Missing Comment** | "Temperature for US0156 at Visit 2 is 35.1°C (out of range). Please provide clinical comment explaining this value." |

---

## 🎓 Concepts Demonstrated

### Clinical Data Management
- Multi-site data integration
- CRF domain relationships (Screening → Demographics → Dosing → Observations → Completion)
- Derived variable calculations (Day of Study)
- Query generation and tracking

### Data Quality
- Range validation
- Logic checks (date relationships)
- Completeness verification
- Cross-form consistency
- Protocol deviation detection

### Software Engineering
- ETL pipeline design
- Relational database modeling
- Data quality frameworks
- Separation of concerns (flag vs. correct)

### Regulatory Compliance
- GCP alignment (no auto-correction)
- Audit trail concepts
- Query documentation
- Data integrity principles

---

## 🛠️ Technologies Used

- **Python 3.8+** - Core programming language
- **Pandas** - Data manipulation and analysis
- **Faker** - Realistic synthetic data generation
- **SQLite** - Lightweight database engine

---

## 📈 Future Enhancements

Potential extensions for learning or production use:

- [ ] Mock API connector for EDC systems
- [ ] SAS dataset output using pyreadstat
- [ ] CDISC SDTM domain mapping
- [ ] Audit trail table with change tracking
- [ ] Query workflow with routing and SLA tracking
- [ ] External data import functionality (labs, ePRO)
- [ ] Data reconciliation reporting
- [ ] PowerBI dashboard templates

---

## 📖 Documentation

- **[Technical Design Document](docs/technical_design_document.md)** - Production architecture and gap analysis
- **[Code Comments](clinical_data_pipeline.py)** - Inline documentation

---

## 🤝 Contributing

This is a demonstration project for portfolio purposes. However, feedback and suggestions are welcome:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Tiago Fernandes**

- GitHub: [@TiagoRoad66-lab](https://github.com/TiagoRoad66-lab)
- LinkedIn: [Tiago Fernandes](www.linkedin.com/in/tiago-fernandes-6487a7aa)
- Email: x.tiago@hotmail.com

---

## 🙏 Acknowledgments

- Clinical trial data structure based on CDISC standards
- Inspired by real-world pharmaceutical data management workflows
- Built to demonstrate understanding of regulatory requirements and data integrity principles

---

## ⚠️ Disclaimer

This is a **synthetic data demonstration** for educational and portfolio purposes. It is not intended for use with real patient or animal data. Any clinical trial data management system must comply with applicable regulations including 21 CFR Part 11, ICH-GCP, GDPR, HIPAA, and other regional requirements.

---

## 📞 Questions?

For questions about this project or clinical data management concepts, feel free to reach out via:
- GitHub Issues
- LinkedIn message
- Email

---

**Note**: This project demonstrates conceptual understanding of clinical data pipelines. For production implementation, consult the Technical Design Document for considerations regarding EDC integration, CDMS requirements, validation procedures, and regulatory compliance.