# FastAPI for Machine Learning - Video 1: Introduction to APIs

## Overview
This Repository covers FastAPI from an ML/AI perspective, focusing on building, deploying, and scaling APIs for machine learning models.

---

## Course Structure

### Part 1: FastAPI Fundamentals
- Focus on core FastAPI concepts without ML
- Build a small project to learn fundamentals
- Strong foundation before moving to ML applications

### Part 2: Connecting FastAPI with Machine Learning
- Build APIs for pre-trained ML models
- Convert Jupyter notebook models to production APIs
- Connect APIs to websites for real-world deployment

### Part 3: Deployment
- Deploy ML APIs to cloud services (AWS)
- Learn industry-grade code practices
- Dockerize applications
- Deploy containerized APIs to production

---

## What is an API?

### Definition
**API (Application Programming Interface)** is a mechanism that enables software components (like front end and back end) to communicate with each other using a defined set of rules, protocols, and data formats.

**Simple explanation**: An API is a **connector** between two pieces of software.

### The Restaurant Analogy
- **Customer** = Front end (user interface)
- **Kitchen/Chef** = Back end (business logic, database)
- **Waiter** = API (connects customer with kitchen)

**Flow**:
1. Customer orders food (user makes request)
2. Waiter takes order to kitchen (API receives request)
3. Chef prepares food (back end processes request)
4. Waiter brings food back (API returns response)
5. Customer receives meal (user gets result)

---

## The Pre-API Era: Monolithic Architecture

### Example: IRCTC Railway System

**Components without API**:
- **Database**: Stores train information
- **Back End**: Contains `fetch_trains()` function to query database
- **Front End**: Form where users enter station names and dates
- All components exist in a **single application/folder**

### Characteristics of Monolithic Architecture
- Front end and back end are **tightly coupled**
- Everything developed in one directory
- Direct communication between components
- No separation of concerns

### Problems with Monolithic Architecture

#### Problem 1: Cannot Share Data with External Applications
**Scenario**: Companies like MakeMyTrip, Yatra, and Goibibo want access to IRCTC's train data.

**Challenge**:
- Cannot give direct database access (security risk)
- Cannot share back end (tightly coupled with front end)
- No way to monetize data for external parties

#### Problem 2: Cannot Support Multiple Platforms
**Scenario**: Need to build website, Android app, and iOS app.

**Challenges**:
- Must build 3 separate monolithic applications
- Each uses different technology stack:
  - Website: Python/PHP
  - Android: Java
  - iOS: Swift
- Must maintain 3 independent databases and back ends
- Same updates needed across all 3 platforms
- Expensive to maintain 3 teams

---

## How APIs Solve These Problems

### Solution Architecture

```
┌─────────────┐
│  Database   │
└──────┬──────┘
       │
┌──────▼──────┐
│  Back End   │
│             │
│fetch_trains()│
└──────┬──────┘
       │
┌──────▼──────┐
│     API     │ (Publicly accessible endpoints)
│             │
│/trains      │
└──────┬──────┘
       │
       ├────────────┬────────────┬────────────┐
       │            │            │            │
    ┌──▼──┐    ┌───▼───┐   ┌────▼───┐   ┌───▼────┐
    │Front│    │MakeMyTrip│  │ Yatra  │   │Goibibo │
    │ End │    │          │  │        │   │        │
    └─────┘    └──────────┘  └────────┘   └────────┘
```

### Key Changes
1. **Decoupling**: Back end and front end are separate applications
2. **API Layer**: Back end exposed through publicly accessible endpoints
3. **Universal Access**: Any application can access back end through API

### Benefits

#### ✅ Solves Problem 1: Data Sharing
- External companies access data through API endpoints
- No direct database or back end access
- Can apply security constraints and validation
- Enables revenue generation through API access

#### ✅ Solves Problem 2: Multi-Platform Support
- **One database** serves all platforms
- **One back end** handles all logic
- **Multiple front ends** (website, Android, iOS)
- All platforms communicate through the same API
- Reduced maintenance cost and complexity

---

## API Communication Details

### HTTP Protocol
All communication between applications and API happens over **HTTP** (HyperText Transfer Protocol).

### JSON Data Format
APIs return responses in **JSON (JavaScript Object Notation)** format.

**Why JSON?**
- **Universal format** understood by all programming languages
- Java, Python, PHP, Swift can all process JSON
- Similar to Python dictionaries in structure

**Example**:
```json
{
  "train_name": "Rajdhani Express",
  "departure": "10:00 AM",
  "arrival": "6:00 PM"
}
```

---

## APIs in Machine Learning

### Traditional Software vs ML Perspective

| **Software Perspective** | **ML Perspective** |
|-------------------------|-------------------|
| Database stores data | ML Model makes predictions |
| Back end queries database | Back end loads model and gets predictions |
| Returns data from database | Returns predictions from model |

### ML API Architecture

```
┌─────────────────┐
│   ML Model      │ (Trained model stored as file)
│  (Binary File)  │
└────────┬────────┘
         │
┌────────▼────────┐
│   Back End      │
│                 │
│  predict()      │ (Loads model, makes predictions)
└────────┬────────┘
         │
┌────────▼────────┐
│      API        │ (Public endpoints)
│                 │
│  /predict       │
└────────┬────────┘
         │
         ├──────────┬──────────┬──────────┐
         │          │          │          │
    ┌────▼───┐  ┌──▼──┐   ┌───▼──┐  ┌───▼───┐
    │Website │  │Android│  │ iOS  │  │External│
    │        │  │ App   │  │ App  │  │Clients │
    └────────┘  └───────┘  └──────┘  └────────┘
```

### Example: ChatGPT/OpenAI

**How OpenAI uses APIs**:
1. OpenAI trains GPT models on massive datasets
2. Model stored and accessible through back end
3. API layer exposes model through endpoints
4. Multiple applications access the same model:
   - ChatGPT website
   - ChatGPT mobile apps
   - External companies (Zomato chatbots, Amazon review summarization, RAG systems)

**Benefits**:
- One model serves all platforms
- External companies can integrate GPT capabilities
- Consistent experience across all interfaces
- Scalable architecture

### Example: Amazon Recommender System

**Traditional Approach** (Monolithic):
- Build separate recommender for website
- Build separate recommender for Android app
- Build separate recommender for iOS app
- 3x the work and maintenance

**API Approach**:
- One ML model
- One back end
- One API
- Three separate front ends (website, Android, iOS)
- All use the same API for recommendations

---

## Key Takeaways

1. **APIs are connectors** between software components
2. **Monolithic architecture** tightly couples components, limiting scalability
3. **API architecture** enables:
   - Data/model sharing with external parties
   - Multi-platform support with single back end
   - Reduced maintenance costs
   - Better scalability
4. **In ML**, APIs expose trained models to multiple applications
5. **Communication** happens via HTTP protocol
6. **Data exchange** uses JSON format (universal)
7. **FastAPI** is the industry-standard framework for building ML APIs

---

## Next Video Preview
- Benefits of FastAPI vs other API frameworks
- Setting up FastAPI development environment
- Building your first API

---

## Industry Context
- 9 out of 10 companies use FastAPI for ML model APIs
- FastAPI enables scalable, robust, industry-grade APIs
- Essential skill for AI/ML career development
- Used by major companies for production ML systems