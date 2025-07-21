# Data Delivery Agreement (DDA) - Crohn's Disease Management

## Document Information
- **Domain**: Crohn's Disease Management
- **Stakeholders**: Gastroenterologists, IBD Specialists, Nutritionists, Surgeons, Research Teams
- **Data Owner**: Director of IBD Center
- **Effective Date**: 2024-01-15
- **Review Cycle**: Monthly

## Business Context
The Crohn's Disease Management domain supports comprehensive care for patients with Crohn's disease, a chronic inflammatory bowel condition. This DDA defines data requirements for disease monitoring, treatment optimization, surgical planning, and quality of life assessment.

## Data Entities

### Patient
- **Description**: Crohn's disease patient information
- **Key Attributes**:
  - Patient ID (Primary Key)
  - First Name, Last Name
  - Date of Birth
  - Gender
  - Diagnosis Date
  - Disease Location (Ileum, Colon, Both)
  - Disease Behavior (Inflammatory, Stricturing, Penetrating)
  - Family History of IBD
  - Smoking Status
- **Business Rules**:
  - Patient ID must be unique
  - Diagnosis date cannot be future
  - Disease location must be valid

### Disease Activity Assessment
- **Description**: Clinical disease activity measurements
- **Key Attributes**:
  - Assessment ID (Primary Key)
  - Patient ID (Foreign Key)
  - Assessment Date
  - CDAI Score (Crohn's Disease Activity Index)
  - Harvey-Bradshaw Index
  - CRP Level
  - ESR Level
  - Fecal Calprotectin
  - Physician Global Assessment
- **Business Rules**:
  - Must reference valid Patient ID
  - Assessment date cannot be future
  - CDAI score must be 0-600

### Endoscopy Report
- **Description**: Colonoscopy and endoscopy findings
- **Key Attributes**:
  - Report ID (Primary Key)
  - Patient ID (Foreign Key)
  - Procedure Date
  - Procedure Type (Colonoscopy, Upper Endoscopy, Capsule Endoscopy)
  - Endoscopist
  - Disease Location
  - Ulceration Score
  - Stricture Presence
  - Fistula Presence
  - Biopsy Results
- **Business Rules**:
  - Must reference valid Patient ID
  - Procedure date cannot be future
  - Ulceration score must be 0-3

### Medication Therapy
- **Description**: Medications used in Crohn's treatment
- **Key Attributes**:
  - Therapy ID (Primary Key)
  - Patient ID (Foreign Key)
  - Medication Name
  - Drug Class (5-ASA, Corticosteroids, Immunomodulators, Biologics)
  - Start Date
  - End Date
  - Dosage
  - Frequency
  - Response Assessment
  - Side Effects
- **Business Rules**:
  - Must reference valid Patient ID
  - End date must be after start date
  - Dosage must be positive

### Nutritional Assessment
- **Description**: Nutritional status and dietary interventions
- **Key Attributes**:
  - Assessment ID (Primary Key)
  - Patient ID (Foreign Key)
  - Assessment Date
  - BMI
  - Weight Change
  - Albumin Level
  - Vitamin D Level
  - Iron Studies
  - Dietary Restrictions
  - Nutritional Supplements
- **Business Rules**:
  - Must reference valid Patient ID
  - Assessment date cannot be future
  - BMI must be positive

### Surgical Intervention
- **Description**: Surgical procedures and outcomes
- **Key Attributes**:
  - Surgery ID (Primary Key)
  - Patient ID (Foreign Key)
  - Surgery Date
  - Procedure Type (Resection, Strictureplasty, Fistula Repair)
  - Surgeon
  - Indication
  - Complications
  - Post-op Recovery Time
  - Recurrence at Anastomosis
- **Business Rules**:
  - Must reference valid Patient ID
  - Surgery date cannot be future
  - Recovery time must be positive

### Quality of Life Assessment
- **Description**: Patient-reported quality of life measures
- **Key Attributes**:
  - Assessment ID (Primary Key)
  - Patient ID (Foreign Key)
  - Assessment Date
  - IBD-Q Score
  - SF-36 Score
  - Work Productivity
  - Social Functioning
  - Emotional Well-being
  - Fatigue Level
- **Business Rules**:
  - Must reference valid Patient ID
  - Assessment date cannot be future
  - Scores must be within valid ranges

## Relationships

### Patient Relationships
- **Patient** → **Disease Activity Assessment** (1:N)
  - A patient can have multiple disease activity assessments
  - Each assessment belongs to exactly one patient

- **Patient** → **Endoscopy Report** (1:N)
  - A patient can have multiple endoscopy reports
  - Each report belongs to exactly one patient

- **Patient** → **Medication Therapy** (1:N)
  - A patient can have multiple medication therapies
  - Each therapy belongs to exactly one patient

- **Patient** → **Nutritional Assessment** (1:N)
  - A patient can have multiple nutritional assessments
  - Each assessment belongs to exactly one patient

- **Patient** → **Surgical Intervention** (1:N)
  - A patient can have multiple surgical interventions
  - Each surgery belongs to exactly one patient

- **Patient** → **Quality of Life Assessment** (1:N)
  - A patient can have multiple quality of life assessments
  - Each assessment belongs to exactly one patient

### Treatment Relationships
- **Medication Therapy** → **Disease Activity Assessment** (M:N)
  - Medication therapies can be evaluated against disease activity
  - Disease activity can be influenced by multiple therapies

- **Surgical Intervention** → **Disease Activity Assessment** (M:N)
  - Surgical interventions can be evaluated against disease activity
  - Disease activity can be affected by surgical procedures

### Cross-Domain Relationships
- **Endoscopy Report** → **Surgical Intervention** (M:N)
  - Endoscopy findings can indicate need for surgery
  - Surgical outcomes can be monitored by endoscopy

## Data Quality Requirements

### Completeness
- Patient ID must be present in all related records
- Assessment dates must be provided
- Required clinical scores must be recorded

### Accuracy
- Laboratory values must be within physiological ranges
- Clinical scores must be calculated correctly
- Dates must be in ISO format (YYYY-MM-DD)

### Timeliness
- Disease activity assessments must be updated monthly
- Endoscopy reports must be available within 48 hours
- Medication response must be assessed within 2 weeks

## Access Patterns

### Common Queries
1. Disease activity trends over time
2. Medication efficacy by patient characteristics
3. Surgical outcomes and complications
4. Quality of life correlation with disease activity

### Performance Requirements
- Patient history retrieval: < 2 seconds
- Disease activity trend analysis: < 5 seconds
- Treatment response assessment: < 3 seconds

## Data Governance

### Privacy
- HIPAA compliance for all patient data
- PHI encryption at rest and in transit
- Patient consent required for research use

### Security
- Role-based access control (RBAC)
- Audit logging for all clinical data access
- Two-factor authentication for medical staff

### Compliance
- HIPAA compliance
- FDA reporting for adverse events
- Clinical trial data standards

## Success Metrics
- 98% data completeness across all entities
- < 0.5% data quality issues in production
- 99.9% system availability
- < 3 second average query response time 