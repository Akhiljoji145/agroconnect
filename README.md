# AgroConnect Smart Platform

## I. Project Overview
### 1.1 Project Title
AgroConnect Smart Platform

### 1.2 Problem Statement
Farmers often lack a single, unified platform for soil analysis insights, crop recommendations, marketplace access, and inventory tracking. Consumers struggle to discover local produce and track purchases in one place. This results in inefficiencies, reduced income for farmers, and limited transparency for buyers. AgroConnect addresses these gaps by connecting farmers and consumers while providing data-driven support for farming decisions and commerce.

### 1.3 Project Objectives (SMART)
- Build a role‑based web platform (Farmer/Consumer) with registration, login, and dashboards by the end of Sprint 2.
- Implement soil analysis inputs and recommendations, plus farmer feed posting, by Sprint 2.
- Enable marketplace product listing, ordering, and order tracking by Sprint 3.
- Ensure all core modules are integrated and tested by Sprint 3.

### 1.4 Scope of Work
**Included:**
- Farmer registration/login and dashboard
- Consumer registration/login and dashboard
- Soil analysis inputs and recommendation display
- Farmer feed with image and description
- Product listings, inventory management, and orders
- Basic analytics history (recent records)

**Excluded (current stage):**
- Advanced ML crop prediction models
- Real‑time weather API integration
- Payment gateway integration
- Mobile application

### 1.5 Course Outcomes Mapping
- **CO1 (Understand):** Identify real‑life problem in agriculture supply chain.
- **CO2 (Apply):** Gather requirements from farmers/consumers.
- **CO3 (Apply):** Apply Scrum methodology for development.
- **CO4 (Analyse):** Analyze and design system modules and data model.
- **CO5 (Evaluate):** Test each module in iterations.
- **CO6 (Create):** Integrate multiple modules into a working system.
- **CO7 (Apply):** Document and prepare deployment workflow.

---

## II. Requirements Gathering and Analysis
### 2.1 Stakeholder Analysis
- **Farmers:** Need soil analysis, crop recommendations, marketplace access, inventory tracking, and order management.
- **Consumers:** Need product browsing, ordering, and purchase tracking.
- **Project Guide/Instructor:** Requires clear documentation, planning, and Scrum evidence.

**Requirement Gathering Methods:** interviews, informal surveys, and workshop discussions.

### 2.2 Requirements Lists and Definition
**User Stories (functional flow):**
1. As a farmer, I can register and login to access my dashboard.
2. As a farmer, I can record soil parameters and view recommendations.
3. As a farmer, I can post updates with images and descriptions.
4. As a farmer, I can list products and manage inventory.
5. As a farmer, I can view orders and marketplace updates.
6. As a consumer, I can register and login to access my dashboard.
7. As a consumer, I can browse products, order them, and track purchases.

**Functional Requirements:**
- Role‑based registration and login
- Farmer dashboard with soil analysis, feed, inventory, product listings, and orders
- Consumer dashboard with marketplace browsing and order tracking
- Media upload for farmer posts

**Non‑Functional Requirements:**
- Usability: simple, responsive UI
- Security: authenticated access to dashboards
- Performance: fast page load and basic queries
- Reliability: consistent database operations

**Prioritization:**
- **High:** Authentication, dashboards, marketplace, soil analysis
- **Medium:** Analytics history, inventory management enhancements
- **Low:** External API integrations (weather), payments

### 2.3 Use Case Diagrams
Key use cases: Register, Login, Manage Soil Analysis, Post Feed, List Products, Manage Inventory, Place Order, Track Order.

*(Insert use case diagrams here)*

---

## III. Project Planning and Execution
### 3.1 Project Methodology
**Scrum (Agile)** was chosen for incremental delivery, frequent feedback, and risk reduction.

### 3.2 Role Definition
- **Product Owner:** Defines features and priorities.
- **Scrum Master:** Facilitates Scrum practices.
- **Developers:** Implement features and tests.

### 3.3 Sprint Planning
- **Sprint Duration:** 2 weeks
- **Sprint Goal:** deliver complete farmer/consumer workflows and core marketplace.

**Initial Sprint Plan (First 3 Sprints):**
- **Sprint 1:** Authentication flow, base UI, database schema.
- **Sprint 2:** Farmer dashboard (soil analysis, feed, inventory).
- **Sprint 3:** Consumer dashboard, marketplace orders, integration.

**Backlog Process:**
- Product backlog created from user stories.
- Sprint backlog selected based on priority and effort.

**Tracking:**
- Progress tracked using task boards and daily updates.

### 3.4 Sprint Backlog Management
Backlog is refined weekly based on progress and feedback.

### 3.5 Burn Down Charts
- **Completed Sprint Charts:** *(Insert charts here when available)*
- **Ideal Total Burn‑Down:** *(Insert ideal chart for full project timeline)*

### 3.6 Task Division
Tasks assigned based on skills: backend (models, views), frontend (templates), testing, and documentation.

---

## IV. Design and Development (After 3 Sprints)
### 4.1 Design Artifacts
- ER diagram
- Class diagram
- Activity diagram
- Wireframes for dashboards

*(Insert artifacts here)*

### 4.2 Technology Stack
- **Backend:** Python, Django
- **Database:** SQLite (development)
- **Frontend:** HTML, CSS, JavaScript
- **Media:** Pillow for image uploads

### 4.3 Development Progress
- Implemented authentication and role‑based dashboards.
- Added soil analysis, farmer feed, products, inventory, and orders.
- Consumer marketplace browsing and order tracking.

**Challenges & Solutions:**
- Template routing issues resolved by correcting template directory configuration.
- Media uploads enabled via Django media settings.

---

## V. Project Artifacts & Deliverables (After 3 Sprints)
### 5.1 Expected Deliverables
- Completed user stories for farmer/consumer
- Working web prototype
- Database schema and migrations
- Test cases and basic documentation

### 5.2 Project Timeline (Preliminary)
- Week 1–2: Sprint 1
- Week 3–4: Sprint 2
- Week 5–6: Sprint 3

---

## VI. Project Demonstration (if applicable)
### 6.1 Demonstration of Working Prototype
Demonstrate:
- Registration and login
- Farmer dashboard (soil analysis, feed, products)
- Consumer dashboard (browse, order, track)

---

## VII. Questions and Answers
- Be prepared for questions on scope, requirements, planning, methodology, and challenges.
- Incorporate feedback from guide and review panel.

---

## Key Considerations
1. Use clear and concise language.
2. Include visual aids (diagrams, charts, prototypes).
3. Maintain Scrum book with meetings and progress logs.
4. Rehearse presentation for clarity.
