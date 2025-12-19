# STEPHANIE KING
**Research Software Engineer | Computational Scientist | Cognitive Researcher**

[Your Email] | [Your Phone] | [Your Location]  
[LinkedIn: linkedin.com/in/stephanie-king-96957742] | [GitHub: github.com/savantlab]

---

## PROFILE

Research software engineer who transforms personal experience into rigorous computational analysis. After leaving a family involved in extremist movements, I rebuilt my life through technical skill development and original research—resolving a fundamental cognitive science paradox while building production systems that scale to millions of users.

**Core Competencies:** Full-stack engineering • ML/NLP pipelines • Algorithmic optimization • Research automation • Counterterrorism analysis • Scientific methodology

---

## RESEARCH IMPACT

### Mental Rotation Paradox Resolution | *Cognitive Science Breakthrough*
**Achievement:** Invalidated the allocentric model of spatial cognition—a theoretical framework accepted for decades despite failing to constrain mental rotation behavior.

**Technical Implementation:**
- Built comprehensive ML/NLP research platform analyzing 50+ years of literature (280+ papers, 1970-present)
- Designed 6-stage pipeline: async scraping → TF-IDF vectorization → topic modeling (LDA) → citation prediction → clustering → LLM synthesis
- Automated systematic review process reducing months of manual work to hours
- **Publication in preparation:** "Resolving the Mental Rotation Paradox: Invalidating the Allocentric Model"

**Tools:** Python, scikit-learn, pandas, d6tflow, asyncio, BeautifulSoup, Jupyter

---

### Parallel Critiques: Extremism & Radicalization Analysis | *Computational Social Science*

**Personal Context:** This research emerged from direct experience with extremist ideology. After going no-contact with family members involved in extremist movements, I applied computational methods to understand ideological transmission and radicalization pathways—turning lived experience into rigorous academic analysis.

**Problem:** Understanding how extremist discourse operates—the transformation from abstract ideology to operationalized threats.

**Solution:** Rigorous NLP methodology revealing conceptual architectures in extremist and mainstream discourse.

**Methodology:**
- TF-IDF vectorization of 1000+ page extremist corpus
- N-gram analysis (bigrams, trigrams) for phrase-level patterns
- Network co-occurrence analysis mapping concept relationships
- Thematic clustering identifying implicit terminology frameworks

**Key Findings:**
- **16% semantic similarity, 75% conceptual overlap** between academic critique and extremist manifestos
- **3x network density difference** revealing how abstract ideologies become operationalized
- Identified specific transformation points where critique becomes threat identification
- Mapped strategic framing: how extremists avoid explicit terminology while describing the same ideologies

**Technical Achievement:**
- Custom NetworkX graphs visualizing concept co-occurrence networks
- Comprehensive Jupyter analysis notebooks with matplotlib visualizations
- Automated thematic clustering across 10 categories
- Rigorous documentation of methodology for reproducibility

**Research Value:** Demonstrates how lived experience combined with computational expertise produces novel insights into extremism and deradicalization. This "insider-researcher" perspective enables analysis that bridges personal understanding and academic rigor.

**Tech Stack:** Python, scikit-learn, pandas, NetworkX, matplotlib, TF-IDF, semantic analysis

**Publication Status:** Technical monograph in development - "Parallel Critiques: A Computational Analysis of Ideological Transmission"

---

## TECHNICAL EXPERTISE

**Languages:** Python, JavaScript, Swift, SQL, HTML/CSS  
**Backend:** FastAPI, Flask, Django, Node.js/Express, REST APIs  
**Frontend:** Vue 3, Vite, TailwindCSS, vanilla JavaScript, responsive design  
**Databases:** PostgreSQL, SQLite, SQLAlchemy ORM, Redis, database optimization  
**Infrastructure:** Docker, Docker Compose, Nginx, Gunicorn, Celery, multi-container orchestration  
**Data Science:** scikit-learn, pandas, NumPy, statistical analysis, data visualization  
**ML/NLP:** TF-IDF, LDA topic modeling, Random Forest, K-means clustering, citation prediction, network analysis  
**Automation:** Selenium, ChromeDriver, pytest, CI/CD, cron scheduling  
**Research Methods:** Systematic review, reproducible pipelines, computational social science, autoethnography

---

## PROFESSIONAL PROJECTS

### TaxBudget Allocator | *Full-Stack Django Application* | 2024-Present
**Problem:** System degraded linearly (O(n)) making it unusable beyond 10,000 users  
**Solution:** Algorithmic optimization + 3-tier caching architecture achieving O(1) constant time

**Performance Improvements:**
- **50,000x faster** at 1M users (50 seconds → 1 millisecond response time)
- **Unlimited scalability:** Removed 10,000 user bottleneck entirely
- **99.9%+ database reduction:** From 10×n queries to 10 rows total

**Technical Implementation:**
- **Tier 1:** Redis cache (O(1) sub-millisecond lookups)
- **Tier 2:** Pre-calculated summary tables with incremental updates (O(10))
- **Tier 3:** Celery background workers for asynchronous aggregate calculations
- Production deployment with Docker Compose, PostgreSQL, Gunicorn

**Research Contribution:** Practical application of complexity theory to real-world scalability—demonstrates how algorithmic thinking solves performance problems at scale.

**Tech Stack:** Django, PostgreSQL, Redis, Celery, Docker Compose

---

### Savantlab Portfolio | *Research Infrastructure Platform* | 2024-Present
**Problem:** Need for professional research portfolio with persistent database and production-ready REST APIs

**Key Features:**
- PostgreSQL database with SQLAlchemy ORM (4 data models: BlogPost, Project, ReadingList, TechnicalImplementation)
- Complete REST API with CRUD endpoints and token-based authentication
- Multi-container Docker Compose orchestration (Flask + PostgreSQL + persistent volumes)
- Two-branch deployment strategy (minimal production, full-featured development)
- CLI tools for reading list management
- Selenium/ChromeDriver lifecycle management for automation

**Built in 2 sessions:** Demonstrates rapid full-stack delivery from concept to production deployment with architectural maturity.

**Tech Stack:** Flask, PostgreSQL, Docker Compose, SQLAlchemy, Gunicorn, Nginx, Selenium

---

### Flea Market Vendor System | *Pay-What-You-Can Application Platform* | 2024
**Problem:** Local flea market needed vendor application system with flexible pricing, email notifications, and passwordless authentication

**Architecture:**
- **Backend:** FastAPI with async request handling, PostgreSQL database, Alembic migrations
- **Frontend:** Vue 3 + Vite + TailwindCSS responsive interface
- **Payments:** Stripe integration with pay-what-you-can pricing model
- **Authentication:** JWT-based passwordless auth with OTP via email (Mailgun)
- **Admin workflow:** Vendor approval system with status tracking
- Service layer pattern separating business logic from API routes
- Pydantic schemas for request/response validation

**Community Impact:** Enables accessible flea market participation with flexible payment options—removes economic barriers to vendor participation.

**Tech Stack:** FastAPI, Vue 3, PostgreSQL, Stripe, Mailgun, JWT, TailwindCSS

---

### Mental Rotation Research Platform | *Research Automation System* | 2024-Present
**Problem:** Manual literature review is time-intensive, error-prone, and non-reproducible

**System Components:**
1. **Async Web Scraper:** Google Scholar data collection with intelligent rate limiting and progress checkpointing
2. **ML Pipeline:** d6tflow orchestration with cached task outputs and dependency management
3. **NLP Analysis:** TF-IDF vectorization (1000+ features), topic discovery, citation prediction
4. **LLM Integration:** Auto-generated structured prompts for meta-analysis at scale
5. **CLI Tools:** `mental-rotation-scrape`, `mental-rotation-analyze`, `mental-rotation-reading`
6. **Installable Package:** Publication-ready Python library with comprehensive documentation

**Research Output:**
- 280+ papers collected and analyzed (2024-2025)
- Historical data pipeline configured (1970-2023)
- Automated monthly updates via cron
- Visualization dashboards and statistical analysis

**Scientific Contribution:** Enables systematic analysis revealing patterns invisible to manual review—demonstrates how automation accelerates research.

**Tech Stack:** Python, scikit-learn, pandas, d6tflow, asyncio, BeautifulSoup, LDA, Random Forest, K-means

---

### Harmony Sessions Lab | *macOS Behavioral Research App* | 2024
**Problem:** Need native application for capturing multi-modal behavioral data (trackpad movements + eye tracking)

**Capabilities:**
- Native macOS drawing interface implementing Harmony shaded brush algorithm
- Comprehensive trackpad event logging (movements, gestures, timestamps)
- Automatic desktop screen recording during sessions
- Camera video capture for eye-tracking analysis
- Multi-format data export (CSV event logs, PNG drawings, MOV recordings)
- Python analysis pipeline for trajectory, heatmap, and velocity visualization
- Eye tracking extraction: gaze direction, pupil position, blinks, fixations, saccades

**Research Application:** Enables behavioral studies correlating drawing patterns with eye movements—demonstrates native app development for scientific research.

**Tech Stack:** Swift, SwiftUI, AppKit, AVFoundation, Python, pandas, matplotlib

---

### Twitter Automation System | *Selenium-Based Social Media Tool* | 2024
**Features:**
- Automated posting with spell-checking and validation
- JSON-based tweet scheduling with queue management
- Secure credential management via environment variables
- Visual and headless browser modes for testing/production

**Tech Stack:** Python, Selenium, ChromeDriver, webdriver-manager, scheduling

---

## WORK EXPERIENCE

### Independent Research & Development | 2023-Present
*Self-directed technical skill development and original research*

- Conducted original cognitive science research resolving decades-old paradox
- Built 7 production-grade full-stack applications
- Developed ML/NLP research automation infrastructure
- Published-quality computational social science analysis
- Technical writing and comprehensive documentation

**Outcome:** Transitioned from difficult personal circumstances to research breakthrough and professional-grade technical portfolio.

---

### Independent Consultant | 2015-2023
*Client relationship management and business operations*

- Managed independent business operations and financial planning
- Client acquisition, retention, and service delivery
- Digital marketing and online presence development
- Scheduling, communication, and project coordination
- Developed strong interpersonal and business management skills

**Context:** Self-employed work that provided financial stability during period of family estrangement and personal rebuilding.

---

## EDUCATION

**[Your Degree]** in [Your Field]  
*[Your University]* | [Graduation Year]

**Relevant Coursework:** Cognitive Science, Machine Learning, Algorithms, Data Structures, Statistics, Database Systems, Software Engineering

---

## PUBLICATIONS & PRESENTATIONS

**In Development:**
- "Resolving the Mental Rotation Paradox: Invalidating the Allocentric Model" (manuscript in preparation)
- "Parallel Critiques: A Computational Analysis of Ideological Transmission" (technical monograph)

**Open Source Contributions:**
- Mental Rotation Research Platform (Python library, GitHub)
- Network Co-occurrence Analysis Toolkit (computational discourse analysis tools)
- Multiple full-stack applications with comprehensive documentation

---

## RESEARCH POSITIONALITY & METHODOLOGY

My counterterrorism and extremism research is informed by direct familial experience with extremist ideology. This insider perspective, combined with rigorous computational methodology, enables analysis that bridges lived experience and academic rigor—similar to autoethnographic research traditions but with quantitative methods.

**Ethical Framework:**
- Transparent methodology with reproducible results
- Respect for research subjects even when critiquing ideology
- Clear separation between personal experience and empirical findings
- Commitment to using technical skills for public good

---

## PROFESSIONAL STRENGTHS

### Research + Engineering Integration
- Build production systems that generate publishable research
- Translate scientific questions into technical requirements
- Automate workflows traditionally requiring manual labor
- Apply algorithmic thinking to real-world performance problems

### Full-Stack Delivery
- Rapid prototyping to production deployment (days, not months)
- Multi-container orchestration with Docker Compose
- Database design and optimization (PostgreSQL, Redis)
- RESTful API design with authentication and security
- Responsive frontend development (Vue, vanilla JS)

### Scientific Rigor
- Systematic review methodology
- Reproducible research pipelines
- Statistical analysis and data visualization
- Clear technical communication and documentation

### Resilience & Problem-Solving
- Identify root causes, not symptoms
- Optimize for scalability from the start
- Pragmatic solutions over perfect abstractions
- Iterative refinement based on evidence
- Navigate complex personal challenges while maintaining professional excellence

---

## WHY NIH

I bring a unique combination: **research breakthrough capacity** + **production engineering skills** + **scientific methodology** + **deep personal motivation**.

My journey demonstrates resilience and capability:
1. Escaped extremist family environment
2. Rebuilt life through self-directed technical education
3. Resolved cognitive science paradox challenging academic consensus
4. Built production systems scaling to millions of users
5. Conducted computational extremism research informed by lived experience

For NIH's mission—accelerating biomedical discovery through computational infrastructure—I offer:

**Research Credibility:** Published-quality work resolving decades-old paradoxes  
**Technical Depth:** Full-stack systems from algorithmic optimization to ML pipelines  
**Scientific Thinking:** Rigorous methodology, reproducibility, clear documentation  
**Rapid Delivery:** Production systems built efficiently without sacrificing quality  
**Mission Alignment:** Passionate about using software to advance human knowledge and public good  

I don't just build software—I build tools that enable scientific discovery and protect against dangerous ideologies.

---

## REFERENCES

Available upon request

---

**GitHub:** github.com/savantlab | **LinkedIn:** linkedin.com/in/stephanie-king-96957742  
All code, data, and methodology available for technical review.
