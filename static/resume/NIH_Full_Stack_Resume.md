# [Your Name]
**Research Software Engineer | Computational Scientist | Full-Stack Developer**

[Your Email] | [Your Phone] | [Your Location]  
[LinkedIn] | [GitHub: github.com/savantlab] | [Website/Portfolio]

---

## PROFILE

Full-stack software engineer with proven research impact—resolved a fundamental paradox in cognitive science while building production-grade infrastructure at scale. Combines deep technical expertise (Python, JavaScript, Swift, PostgreSQL, Docker) with scientific rigor and algorithmic thinking. Experienced building systems that process millions of records, automate research workflows, and generate publishable insights.

---

## RESEARCH IMPACT

### Mental Rotation Paradox Resolution | *Cognitive Science*
**Breakthrough:** Invalidated the allocentric model of spatial cognition—a theoretical framework accepted for decades despite failing to constrain mental rotation behavior.

**Technical Achievement:**
- Built comprehensive ML/NLP research platform analyzing 50+ years of literature (280+ papers, 1970-present)
- Designed 6-stage pipeline: async scraping → TF-IDF vectorization → topic modeling (LDA) → citation prediction (Random Forest) → clustering → LLM synthesis
- Automated systematic review process reducing months of manual work to hours
- **Publication in preparation:** "Resolving the Mental Rotation Paradox: Invalidating the Allocentric Model"

**Tools:** Python, scikit-learn, pandas, d6tflow, asyncio, BeautifulSoup, Jupyter

---

## TECHNICAL EXPERTISE

**Languages:** Python, JavaScript, Swift, SQL, HTML/CSS  
**Backend:** FastAPI, Flask, Django, Node.js/Express, REST APIs, GraphQL  
**Frontend:** Vue 3, Vite, TailwindCSS, vanilla JS, responsive design  
**Databases:** PostgreSQL, SQLite, SQLAlchemy ORM, database optimization  
**Infrastructure:** Docker, Docker Compose, Nginx, Gunicorn, Redis, Celery  
**Data Science:** scikit-learn, pandas, NumPy, TF-IDF, LDA, Random Forest, K-means  
**NLP/ML:** Topic modeling, semantic analysis, citation prediction, network analysis  
**Testing/Automation:** Selenium, pytest, CI/CD, ChromeDriver  
**DevOps:** Multi-container orchestration, environment management, production deployment  
**Research Tools:** Systematic review methodology, data visualization, Jupyter notebooks

---

## PROFESSIONAL PROJECTS

### TaxBudget Allocator | *Full-Stack Django Application* | 2024-Present
**Problem:** System degraded linearly (O(n)) making it unusable beyond 10,000 users  
**Solution:** Algorithmic optimization + caching architecture achieving O(1) constant time

**Performance Improvements:**
- **50,000x faster** at 1M users (50s → 1ms response time)
- **Scalability:** 10,000 user limit → unlimited users
- **Database reduction:** 99.9%+ fewer queries (10×n → 10 rows total)

**Technical Implementation:**
- 3-tier caching: Redis (O(1)) → Summary tables (O(10)) → Live calculation fallback
- Incremental aggregate updates via Celery background workers
- Pre-calculated summary tables with running statistics
- Production deployment with Docker Compose, PostgreSQL, Gunicorn

**Tech stack:** Django, PostgreSQL, Redis, Celery, Docker Compose, algorithmic optimization

**Research contribution:** Demonstrates practical application of complexity theory to real-world scalability problems

---

### Savantlab Portfolio | *Research Infrastructure Platform* | 2024-Present
**Problem:** Need for professional research portfolio with persistent database and REST APIs  
**Solution:** Full-stack application with Docker orchestration and production-ready infrastructure

**Key Features:**
- **Database:** PostgreSQL with SQLAlchemy ORM (4 data models: BlogPost, Project, ReadingList, TechnicalImplementation)
- **REST APIs:** Complete CRUD endpoints with token-based authentication
- **Infrastructure:** Multi-container Docker Compose setup (Flask + PostgreSQL + persistent volumes)
- **DevOps:** Two-branch strategy (production main, full-featured deploy)
- **CLI Tools:** Command-line interface for reading list management
- **Automation:** Selenium/ChromeDriver lifecycle management

**Production deployment:** Gunicorn workers, environment-based configuration, persistent data storage

**Tech stack:** Flask, PostgreSQL, Docker Compose, SQLAlchemy, Gunicorn, Nginx, Selenium

**Built in 2 sessions:** Demonstrates rapid full-stack delivery with architectural maturity

---

### Flea Market Vendor System | *Pay-What-You-Can Application Platform* | 2024
**Problem:** Local flea market needed vendor application system with flexible pricing and email notifications  
**Solution:** Modern full-stack application with payment processing and passwordless authentication

**Key Features:**
- **Backend:** FastAPI with async request handling, PostgreSQL database, Alembic migrations
- **Frontend:** Vue 3 + Vite + TailwindCSS responsive interface
- **Payments:** Stripe integration with pay-what-you-can pricing model
- **Authentication:** JWT-based passwordless auth with OTP via email
- **Email:** Mailgun integration for notifications and authentication codes
- **Admin workflow:** Vendor approval system with status tracking

**Architecture:**
- RESTful API design with Pydantic schemas for validation
- Service layer pattern separating business logic from routes
- Database models with proper relationships and constraints
- Environment-based configuration for development/production

**Tech stack:** FastAPI, Vue 3, PostgreSQL, Stripe, Mailgun, JWT, TailwindCSS

**Community impact:** Enables accessible flea market participation with flexible payment options

---

### Mental Rotation Research Platform | *Research Automation System* | 2024-Present
**Problem:** Manual literature review is time-intensive and non-reproducible  
**Solution:** End-to-end research automation with ML/NLP pipeline

**System Components:**
1. **Async Web Scraper:** Google Scholar data collection with intelligent rate limiting, progress checkpointing
2. **ML Pipeline:** d6tflow orchestration with cached task outputs and dependency management
3. **NLP Analysis:** TF-IDF vectorization (1000+ features), topic discovery, citation prediction
4. **LLM Integration:** Auto-generated structured prompts for meta-analysis at scale
5. **CLI Tools:** `mental-rotation-scrape`, `mental-rotation-analyze`, `mental-rotation-reading`
6. **Installable Package:** Publication-ready Python library with comprehensive documentation

**Research Output:**
- 280+ papers collected and analyzed (2024-2025)
- Historical data pipeline ready (1970-2023)
- Automated monthly updates via cron
- Visualization dashboards and statistical analysis

**Tech stack:** Python, scikit-learn, pandas, d6tflow, asyncio, BeautifulSoup, LDA, Random Forest, K-means

**Scientific contribution:** Enables systematic analysis revealing patterns invisible to manual review

---

### Parallel Critiques: Discourse Analysis | *Computational Social Science* | 2024
**Problem:** Understanding ideological transmission and radicalization through text analysis  
**Solution:** Rigorous NLP methodology revealing conceptual architectures in discourse

**Methodology:**
- TF-IDF vectorization of 1000+ page corpus
- N-gram analysis (bigrams, trigrams)
- Network co-occurrence analysis (concept relationship mapping)
- Thematic clustering and terminology framework analysis

**Key Findings:**
- **16% semantic similarity, 75% conceptual overlap** between disparate texts
- **3x network density difference** revealing operationalized vs. abstract ideologies
- Identified transformation points from abstract critique to concrete threat identification
- Mapped implicit terminology frameworks and strategic framing

**Technical Achievement:**
- Custom NetworkX graphs visualizing concept co-occurrence
- Comprehensive Jupyter analysis notebooks with matplotlib visualizations
- Automated thematic clustering across 10 categories

**Tech stack:** Python, scikit-learn, pandas, NetworkX, matplotlib, TF-IDF, semantic analysis

**Research value:** Demonstrates computational methods for analyzing sensitive discourse questions

---

### Harmony Sessions Lab | *macOS Behavioral Research App* | 2024
**Problem:** Need native app for capturing trackpad behavior and eye-tracking data  
**Solution:** Swift/SwiftUI macOS application with multi-modal data capture

**Capabilities:**
- **Drawing interface:** Harmony shaded brush algorithm implementation
- **Behavioral logging:** Comprehensive trackpad event capture (movements, gestures, timestamps)
- **Screen recording:** Automatic desktop capture during sessions
- **Eye tracking:** Camera video capture with frame-by-frame gaze/blink analysis
- **Data export:** CSV event logs, PNG drawings, MOV recordings
- **Analysis pipeline:** Python scripts for trajectory, heatmap, and velocity visualization

**Technical Stack:**
- Swift/SwiftUI/AppKit for native macOS interface
- AVFoundation for video recording
- Python analysis with pandas, matplotlib, NumPy
- Eye tracking extraction (gaze, pupil position, fixations, saccades)

**Research application:** Enables behavioral studies of drawing patterns and eye-movement correlation

**Tech stack:** Swift, SwiftUI, AppKit, AVFoundation, Python, pandas, matplotlib

---

### Twitter Automation System | *Selenium-Based Social Media Tool* | 2024
**Features:**
- Automated Twitter posting with spell-checking and validation
- Tweet scheduling system with JSON-based queue management
- Secure credential management with environment variables
- Visual and headless browser modes for testing/production

**Technical Implementation:**
- Selenium WebDriver automation with ChromeDriver
- Schedule-based task execution
- Custom spell-checking with dictionary validation
- Error handling and retry logic

**Tech stack:** Python, Selenium, ChromeDriver, webdriver-manager, scheduling

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

**Open Source:**
- Mental Rotation Research Platform (Python library, GitHub)
- Network Co-occurrence Analysis Toolkit (computational discourse tools)
- Multiple full-stack applications with comprehensive documentation

---

## PROFESSIONAL STRENGTHS

### Research + Engineering Integration
- Build production systems that generate publishable research
- Translate scientific questions into technical requirements
- Automate workflows that traditionally require manual labor
- Apply algorithmic thinking to real-world performance problems

### Full-Stack Delivery
- Rapid prototyping to production deployment
- Multi-container orchestration (Docker Compose)
- Database design and optimization (PostgreSQL, Redis)
- RESTful API design with proper authentication
- Responsive frontend development (Vue, vanilla JS)

### Scientific Rigor
- Systematic review methodology
- Reproducible research pipelines
- Data visualization and statistical analysis
- Clear technical communication and documentation

### Problem-Solving Philosophy
- Identify root causes, not symptoms
- Optimize for scalability from the start
- Pragmatic solutions over perfect abstractions
- Iterative refinement based on evidence

---

## WHY NIH

I bring a rare combination: **research breakthrough capacity** + **production engineering skills** + **scientific methodology**. 

My mental rotation paradox work demonstrates ability to challenge established scientific consensus with computational evidence. My full-stack projects show I can build systems that scale to millions of users while maintaining research-quality rigor.

For NIH's mission—accelerating biomedical discovery through computational infrastructure—I offer:

1. **Research credibility:** Published-quality work resolving decades-old paradoxes
2. **Technical depth:** Full-stack systems from database optimization to ML pipelines
3. **Scientific thinking:** Rigorous methodology, reproducibility, clear documentation
4. **Rapid delivery:** Production systems built in days, not months
5. **Mission alignment:** Passionate about using software to advance human knowledge

I don't just build software—I build tools that enable scientific discovery.

---

## REFERENCES

Available upon request

---

**GitHub:** github.com/savantlab | **Portfolio:** [Your website]  
All code, data, and methodology available for technical review.
