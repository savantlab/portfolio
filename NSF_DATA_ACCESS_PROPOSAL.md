# NSF Funding Data Access Request
## Quantifying Research Impact of Unconstrained Constructs

**Date:** December 30, 2025  
**Project:** Archimedes - Mental Rotation Citation Network Analysis  
**Investigator:** Stephanie King, Savantlab  
**Contact:** [via savantlab.org/contact]

---

## Executive Summary

We request NSF funding database access to calculate precise financial impact of research built on the unconstrained "mental rotation" construct introduced by Shepard & Metzler (1971). Our preliminary citation network analysis identifies **8,600+ papers** citing foundational mental rotation research. Access to NSF award data would enable quantification of:

- Direct research costs for studies using mental rotation as core construct
- Funding allocated to standardized tests built on invalid foundations
- Investment in educational interventions based on unconstrained measures
- Total taxpayer dollars directed toward methodologically compromised research

**Estimated Impact:** $200M-$750M (current rough estimate without funding data)

---

## The Problem: Unconstrained Constructs in Funded Research

### What Happened

1. **Shepard & Metzler (1971)** introduced "mental rotation" without sufficient operational constraints
   - Authors acknowledged limitations that were subsequently ignored
   - Construct lacks clear boundary conditions
   - Citations: 6,107 papers (OpenAlex); ~9,000 (Google Scholar)

2. **Vandenberg & Kuse (1978)** operationalized the unconstrained construct as a standardized test
   - Became standard measure in spatial ability research
   - Citations: 2,566 papers
   - Widely used in NSF-funded studies

3. **50+ years of propagation** through research literature
   - Meta-analyses built on invalid measures
   - Educational policy influenced by flawed assessments
   - STEM ability research using compromised foundations

### Current Citation Network Analysis

Our OpenAlex API analysis reveals:

- **Shepard & Metzler citations:** 6,097 papers (post-1972, medical papers filtered)
- **Vandenberg & Kuse citations:** 2,534 papers
- **Overlap (citing both):** 797 papers
- **Combined unique papers:** ~8,600 papers
- **Temporal span:** 1972-2025 (53 years of contamination)

**Gap:** We can identify WHICH papers cite the unconstrained construct, but not HOW MUCH NSF funding supported this research.

---

## Why NSF Funding Data is Critical

### 1. Precise Cost Calculation

**Current Method (Estimates):**
- Assume average cost per paper: $50K-$200K
- Multiply by estimated affected papers
- Result: Wide range ($200M-$750M)

**With NSF Data:**
- Match citing papers to NSF award database
- Sum actual grant amounts for affected studies
- Calculate precise taxpayer investment in compromised research
- Result: Exact financial impact

### 2. Identification of Core vs. Peripheral Use

Not all citing papers are equally affected:

**CRITICAL Contamination (need funding data):**
- Papers where mental rotation is PRIMARY research question
- Studies developing/validating the Mental Rotation Test
- Educational interventions based on mental rotation assessment
- Meta-analyses using mental rotation as key outcome measure

**MODERATE Contamination (lower priority):**
- Papers citing mental rotation as background context
- Studies using mental rotation as one of many measures

**NSF data enables classification by:**
- Grant abstract mentions of "mental rotation"
- Award amounts to high-contamination studies
- Program officers/directorates involved

### 3. Field-Specific Impact Analysis

NSF funding data provides:
- **Directorate breakdown:** BCS (Behavioral & Cognitive Sciences), EHR (Education), etc.
- **Program-level detail:** Perception/Action/Cognition, STEM Education, etc.
- **Temporal trends:** When did funding peak? Is it still being awarded?
- **Institutional patterns:** Which universities received the most affected funding?

### 4. Policy Impact Assessment

**Educational Research:**
- How much EHR funding supported spatial ability interventions using MRT?
- What educational policies were influenced by NSF-funded mental rotation research?

**Gender Differences Research:**
- Funding for studies using Mental Rotation Test to assess sex differences
- Impact on STEM pipeline research and policy

**Neuroscience:**
- fMRI studies of "mental rotation" without clear operational definition
- What fraction of cognitive neuroscience funding went to undefined processes?

---

## Methodology

### Data Sources We Have

1. **Citation Networks (OpenAlex API)**
   - Papers citing Shepard & Metzler (1971)
   - Papers citing Vandenberg & Kuse (1978)
   - Metadata: DOI, title, authors, year, journal, citation counts

2. **Contamination Analysis**
   - Medical papers filtered out
   - Year constraint (1972+)
   - Temporal distribution analysis
   - Field/concept classification

### Data We Need from NSF

1. **Award Database Access**
   - NSF Award Search API or bulk data export
   - Fields needed:
     - Award ID
     - Award amount
     - PI names
     - Institution
     - Abstract
     - Keywords
     - Program officer
     - Directorate/Division
     - Award date

2. **Matching Strategy**
   - Match PI names + publication years
   - Match grant abstracts containing "mental rotation" keywords
   - Cross-reference NSF-acknowledged papers (many publications cite award numbers)

3. **Classification Protocol**
   - **HIGH:** Mental rotation is primary construct in grant abstract
   - **MODERATE:** Mental Rotation Test used as key measure
   - **LOW:** Mental rotation cited as background literature

---

## Expected Outputs

### 1. Precise Financial Impact Report

```
MENTAL ROTATION CONTAMINATION: NSF FUNDING ANALYSIS
====================================================

Direct NSF Investment (HIGH contamination):
- Total award amount: $XXX million
- Number of grants: XXX
- Average grant size: $XXX
- Peak funding period: YYYY-YYYY

Moderate NSF Investment (MODERATE contamination):
- Total award amount: $XXX million
- Number of grants: XXX

Fields Affected:
- Cognitive Psychology: $XXX million (XXX grants)
- Education Research: $XXX million (XXX grants)
- Neuroscience: $XXX million (XXX grants)
- Gender Studies: $XXX million (XXX grants)

Institutions Most Affected:
1. [University]: $XXX million (XX grants)
2. [University]: $XXX million (XX grants)
...
```

### 2. Temporal Analysis

- Funding trends 1972-2025
- Did funding accelerate despite unresolved conceptual issues?
- When were the largest awards made?
- Is contaminated research still being funded?

### 3. Program-Level Accountability

- Which NSF programs funded the most affected research?
- Which program officers oversaw these awards?
- Opportunity for targeted correction procedures

### 4. Institutional Dashboard

- University-by-university breakdown
- Enables institutional quality control
- Supports researcher notification systems

---

## Value Proposition for NSF

### 1. Accountability & Transparency

- Demonstrates NSF commitment to research quality
- Enables quantification of methodological oversight costs
- Supports future prevention of similar contamination

### 2. Correction Pathway Development

With precise funding data, NSF can:
- Notify PIs of upstream conceptual failures
- Require correction/clarification in future work
- Establish best practices for construct validation
- Prevent future awards to unconstrained research

### 3. Model for Broader Scientific Correction

Mental rotation case demonstrates:
- Systematic contamination tracking is feasible
- Financial impact is quantifiable
- Correction procedures can be developed
- Model extends to other unconstrained constructs (fMRI methods, p-hacking, etc.)

### 4. AI Training Corpus Integrity

- Scientific literature is training data for AI
- Contaminated papers propagate errors to AI systems
- NSF funding data enables integrity scoring
- Supports development of verified scientific corpus

---

## Precedent & Legal Basis

### NSF Data Access Precedent

1. **Award Data is Public Information**
   - NSF Award Search publicly available
   - FOIA requests for bulk data access granted
   - Academic researchers routinely analyze NSF portfolios

2. **Research Integrity Mandate**
   - NSF has mission to ensure research quality
   - Methodological oversight is NSF responsibility
   - Contamination analysis serves NSF mission

3. **Similar Analyses Conducted**
   - Meta-research on NSF funding patterns (bibliometrics)
   - Program evaluation studies
   - Research impact assessments

### Data Use Restrictions We Accept

- **Confidentiality:** We will NOT publish PI-identifiable information without consent
- **Aggregation:** Reports will use aggregate statistics unless specific PI/institutional opt-in
- **Purpose Limitation:** Data used ONLY for mental rotation contamination analysis
- **Audit Trail:** Complete documentation of methodology and data handling
- **IRB Compliance:** If required for PI notification phase

---

## Timeline & Deliverables

### Phase 1: Data Access & Matching (3 months)
- Obtain NSF award database access
- Match publications to NSF awards
- Classify contamination severity
- **Deliverable:** Matched dataset with funding amounts

### Phase 2: Analysis & Quantification (2 months)
- Calculate total financial impact
- Field-specific breakdowns
- Temporal trends analysis
- Institutional patterns
- **Deliverable:** Comprehensive funding impact report

### Phase 3: Visualization & Dissemination (2 months)
- Interactive dashboard development
- Institutional reports
- Policy recommendations
- Public-facing contamination database
- **Deliverable:** Archimedes Dashboard with NSF funding integration

### Phase 4: Correction Procedure Development (3 months)
- PI notification protocols
- Institutional correction guidance
- NSF program officer toolkit
- **Deliverable:** Systematic correction framework

**Total Timeline:** 10 months from data access

---

## Broader Impacts

### 1. Research Quality Control

- Systematic method for tracking construct contamination
- Financial accountability for methodological oversight
- Prevention of future unconstrained construct propagation

### 2. Educational Policy

- Correction of STEM ability assessments
- Revision of spatial reasoning interventions
- Evidence-based educational policy

### 3. Institutional Reform

- University-level quality control mechanisms
- Enhanced oversight of construct validity
- Researcher training on conceptual constraints

### 4. Scientific Integrity Infrastructure

- Model for other contamination cases
- Scalable to multiple fields
- Integration with research databases
- AI training corpus filtering

---

## Why This Matters Now

### 1. AI is Training on Contaminated Literature

- Large language models ingest scientific papers
- Unconstrained constructs propagate to AI systems
- Contamination accelerates with AI adoption
- **Urgency:** Clean the corpus before it's too late

### 2. Continued Funding of Compromised Research

- Mental rotation research still being funded
- No systematic notification of upstream failures
- Taxpayer dollars continue flowing to invalid constructs
- **Urgency:** Stop the bleeding

### 3. Policy Consequences

- Educational interventions based on invalid measures
- STEM pipeline research using compromised tests
- Gender differences research with flawed foundations
- **Urgency:** Policy is being made NOW on bad data

### 4. Precedent for Broader Reform

- Mental rotation is ONE unconstrained construct
- Hundreds of similar cases exist (fMRI methods, p-hacking, etc.)
- Archimedes demonstrates systematic correction is feasible
- **Urgency:** Establish model before contamination accelerates

---

## Budget Request

**Data Access:** $0 (NSF Award Search API is free)

**Analysis Personnel:**
- Data scientist: 6 months FTE @ $120K/year = $60K
- Research assistant: 6 months FTE @ $50K/year = $25K

**Infrastructure:**
- Database hosting: $5K
- Visualization platform: $10K

**Dissemination:**
- Dashboard development: $20K
- Report writing/editing: $10K

**Total Budget:** $130K

**ROI Calculation:**
- If mental rotation contamination = $200M (low estimate)
- Cost to quantify = $130K
- ROI = 1,538:1
- **Preventing ONE future contaminated grant pays for entire project**

---

## Conclusion

We have demonstrated:

1. **Feasibility:** Citation network analysis is complete (8,600+ papers identified)
2. **Methodology:** Robust matching protocol for NSF awards
3. **Value:** Precise financial impact quantification
4. **Impact:** Model for broader scientific correction
5. **Urgency:** AI training, continued funding, policy consequences

**We request NSF funding database access to complete this critical analysis.**

The mental rotation contamination is not hypothetical—it's documented, quantified, and currently propagating through research literature and educational policy. NSF has the data to calculate the exact cost. We have the methodology to extract the insight.

Give us access, and we'll show you the bill.

---

## Contact Information

**Investigator:** Stephanie King  
**Institution:** Savantlab  
**Website:** savantlab.org  
**Project Site:** savantlab.org/archimedes  
**Email:** [via savantlab.org/contact]

---

## Appendix: Sample Outputs

### A. Citation Network Statistics
- Total papers analyzed: 8,631
- Year range: 1972-2025
- Top citing journals: [list]
- Temporal distribution: [visualization]

### B. Contamination Classification
- HIGH: Papers with mental rotation as primary construct
- MODERATE: Papers using Mental Rotation Test as key measure
- LOW: Papers citing mental rotation as background

### C. Visualization Dashboard
- Live at: savantlab.org/archimedes/dashboard
- Interactive paper explorer: savantlab.org/archimedes

### D. Technical Documentation
- OpenAlex API methodology
- Citation network mapping
- Deduplication procedures
- Medical paper filtering
- Year constraint rationale

---

**"Give me a place to stand, and I shall move the Earth."** - Archimedes

We have the place. We need NSF's data to calculate the leverage.
