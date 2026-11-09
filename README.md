# AI-Powered Interview Evaluation & Resume Analysis System

An intelligent final year project that analyzes candidate resumes, conducts AI-assisted interview evaluation, and generates structured hiring insights through a clean web interface.

## Project Title

**AI-Powered Interview Evaluation & Resume Analysis System**

## Project Overview

This project is designed to support recruiters, HR teams, and academic evaluators by automating two major tasks:

1. Resume analysis and candidate profiling
2. Interview evaluation and performance scoring

The system uses Artificial Intelligence and Natural Language Processing to extract resume data, match skills with job requirements, evaluate interview responses, and generate an overall candidate assessment report.

## Problem Statement

Manual resume screening and interview evaluation are time-consuming, inconsistent, and difficult to scale. This project addresses that problem by building an AI-driven platform that can:

- Parse and analyze resumes automatically
- Identify candidate skills, education, and experience
- Compare candidate profiles with job requirements
- Evaluate interview responses using AI
- Generate fair, fast, and structured performance reports

## Objectives

- Automate resume screening
- Reduce recruiter workload
- Improve consistency in candidate evaluation
- Provide skill-gap and job-match insights
- Create a simple and modern UI for interview and resume analysis workflows

## Core Features

- Resume upload in PDF or DOCX format
- Resume text extraction and section detection
- Skill, education, and experience extraction
- Job description matching
- Candidate score generation
- AI-based interview question analysis
- Identity verification with ID upload + live selfie face matching
- Communication and confidence evaluation
- Final candidate ranking dashboard
- Admin panel for managing interviews and reports
- Downloadable evaluation report

## Suggested UI Modules

The system should have a clear and simple user interface with the following pages:

### 1. Landing Page

- Project title and description
- Quick overview of features
- Role selection for candidate or recruiter
- Navigation to login and dashboard

### 2. Dashboard

- Total resumes uploaded
- Interviews completed
- Top candidates
- Recent evaluation activity

### 3. Resume Analysis Page

- Upload resume
- Extracted resume details preview
- Skills and experience summary
- Resume score and job-match score

### 4. Interview Evaluation Page

- Candidate name and job role
- Interview questions and recorded answers
- AI evaluation panel
- Communication, technical, and confidence score

### 5. Reports Page

- Candidate-wise report table
- Filter by role or score
- Export or download report

### 6. Admin/Login Page

- Secure candidate and recruiter login
- Candidate management
- Job description management

## Required Components

### Frontend

- HTML5
- CSS3
- JavaScript
- React.js or Next.js
- Tailwind CSS or Bootstrap
- Chart library such as Chart.js or Recharts

### Backend

- Python
- FastAPI or Flask
- REST API endpoints
- File upload handling
- Authentication module

### AI and NLP

- Rule-based scoring engine
- spaCy
- NLTK
- scikit-learn
- Sentence Transformers

### Database

- MySQL / SQLite (Relational SQL)
- MongoDB (Document DB with PyMongo & Motor drivers)
- SQLAlchemy ORM

### Other Tools

- Git and GitHub
- Postman
- Docker optional
- VS Code

## Suggested System Architecture

```text
Frontend UI
    |
    v
Backend API (FastAPI)
    |
    +-- Resume Parser Module
    +-- Job Matching Module
    +-- Interview Evaluation Module
    +-- Report Generator
    |
    +---> MySQL / SQLite (Relational Data)
    +---> MongoDB (Document Store)
```

## Suggested Folder Structure

```text
Final_Year_Project/
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
├── backend/
│   ├── app/
│   │   ├── auth.py
│   │   ├── database.py (SQL + MongoDB)
│   │   ├── models.py
│   │   ├── questions_bank.py
│   │   ├── schemas.py
│   │   └── services.py
│   ├── requirements.txt
│   └── main.py
├── uploads/
├── .env
└── README.md
```

## Recommended Technology Stack

- Frontend: React.js
- Backend: FastAPI
- Database: MySQL + MongoDB
- Authentication: JWT + role-based access
- AI Layer: Rule-based analysis by default, optional Ollama/OpenAI integration later
- File Parsing: `pdfplumber`, `python-docx`

## Prerequisites

Install the following before running the project:

- Node.js 18+
- Python 3.10+
- MySQL Server 8+ or SQLite
- MongoDB Server 6+ (optional for document storage)
- Git

## Environment Variables

Create a `.env` file in the project root:

```env
DATABASE_URL=mysql+pymysql://root:password@localhost:3306/ai_interview_system
MONGODB_URL=mongodb://localhost:27017
MONGODB_DB_NAME=ai_interview_system
SECRET_KEY=your_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
AI_PROVIDER=rule-based
OPENAI_API_KEY=
OLLAMA_BASE_URL=http://localhost:11434
UPLOAD_DIR=../uploads
```

## AI Provider Modes & Local LLM Setup

The project supports both local rule-based fallback and **100% Local LLMs via Ollama**:

- `ollama`: **Recommended Local LLM mode**. Runs open-source models (e.g., `llama3`, `mistral`, `phi3`) locally on your machine without sending data to external paid APIs.
- `rule-based`: Built-in local NLP keyword and section analysis engine (used automatically as a graceful fallback if Ollama is offline).

### Running Ollama Locally

1. **Install Ollama**:
   - macOS: `brew install ollama` or download from [ollama.com](https://ollama.com)
   - Windows/Linux: Download installer from [ollama.com](https://ollama.com)

2. **Start Ollama Service & Download Model**:
   ```bash
   ollama serve
   ollama pull llama3
   ```

3. **Configure Backend `.env`**:
   ```env
   AI_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434
   OLLAMA_MODEL=llama3
   ```

4. **Verify AI Engine Status**:
   Visit `http://127.0.0.1:8000/ai-status` in your browser to inspect local Ollama model connection status.

# Resume Scoring Rules and Saved Analyses

Resume completeness is calculated by a fixed 100-point rubric in the backend. Ollama may
provide a written summary and feedback, but it cannot change either numeric score:

| Criterion | Points | Rule |
| --- | ---: | --- |
| Core sections | 25 | Up to 5 points each for education, experience, projects, certifications, and skills |
| Distinct skills | 20 | 2 points per detected skill, capped at 10 skills |
| Contact details | 10 | Email (4), phone (4), and LinkedIn or portfolio link (2) |
| Career history evidence | 15 | Experience section (5), action-led evidence (up to 5), and dates/durations (5) |
| Measurable impact | 10 | 1 point per quantified outcome, capped at 10 |
| Project evidence | 10 | Projects section (5), project action evidence (up to 3), and a quantified outcome (2) |
| Resume length | 5 | Full points for 250–1,200 words; partial credit for 150–249 or 1,201–1,600 |
| Readable formatting | 5 | 1 point per extracted bullet, capped at 5 |

Job fit is separate from resume completeness. When the job description contains recognized
skills, job fit is 80% required-skill coverage and 20% relevant keyword coverage. Otherwise
it uses keyword coverage. If no usable job description is supplied, the UI marks job fit as
unavailable rather than presenting a fabricated score. The results panel shows the
criterion-by-criterion score and role skills found or not found in the resume.

Uploaded resumes and their analysis are stored in:

- **Reports page:** SQL `candidate_reports` table. The default local SQLite file is
  `backend/ai_interview_system.db`; if `DATABASE_URL` points to MySQL, reports are stored
  there instead. The resume analysis page links directly to the saved report.
- **MongoDB:** `candidate_profiles` stores the latest profile and analysis per user;
  GridFS (`fs.files` / `fs.chunks`) stores the uploaded document. MongoDB is optional.
- **Local uploads:** `backend/uploads/candidates/<user_id>/` keeps a local copy of the uploaded file.

Analysis of text pasted directly into the page is not saved as an uploaded resume or report.
To inspect the configured database connections, open `http://127.0.0.1:8000/db-status`.

## Installation and Run Instructions

### 1. Clone the Project

```bash
git clone <your-repository-url>
cd Final_Year_Project
```

### 2. Create and Activate Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Backend Dependencies

```bash
pip install -r backend/requirements.txt
```

### 4. Create MySQL Database

```sql
CREATE DATABASE ai_interview_system;
```

Update `backend/.env` with your MySQL username, password, host, and database name.
No OpenAI key is required for the current version.

### 5. Install Frontend Dependencies

```bash
cd frontend
npm install
cd ..
```

### 6. Run the Backend

```bash
cd backend
uvicorn main:app --reload
```

Backend will run at:

```text
http://127.0.0.1:8000
```

### 7. Run the Frontend

Open a new terminal:

```bash
cd frontend
npm start
```

Frontend will run at:

```text
http://localhost:3000
```

## Demo Login Credentials

Use these built-in accounts on the landing page:

### Candidate

- Email: `candidate@example.com`
- Password: `candidate123`

### Recruiter

- Email: `recruiter@example.com`
- Password: `recruiter123`

## Current Default Behavior

- Resume analysis is rule-based
- Interview scoring is rule-based
- JWT authentication uses MySQL-backed users
- Reports are stored in the MySQL `candidate_reports` table

## Minimum API Modules to Build

- `POST /auth/login`
- `GET /auth/me`
- `POST /upload-resume`
- `POST /analyze-resume`
- `POST /match-job`
- `POST /evaluate-interview`
- `GET /candidate-report/{id}`
- `GET /dashboard-stats`

## Expected Outputs

- Extracted candidate details
- Resume score
- Skill match percentage
- Interview performance score
- Overall recommendation
- Downloadable candidate report

## Evaluation Metrics

- Resume relevance score
- Skill match score
- Communication score
- Technical accuracy score
- Confidence score
- Final candidate ranking

## Future Enhancements

- Video interview emotion analysis
- Speech-to-text integration
- Multilingual resume analysis
- Bias reduction and fairness checks
- Email notification system
- Role-based access control

## References

Use these references while preparing the report, implementation, and literature review:

1. Jurafsky, D., and Martin, J. H. *Speech and Language Processing*. Pearson.
2. Bird, S., Klein, E., and Loper, E. *Natural Language Processing with Python*. O'Reilly Media.
3. spaCy Documentation: https://spacy.io/
4. scikit-learn Documentation: https://scikit-learn.org/
5. FastAPI Documentation: https://fastapi.tiangolo.com/
6. React Documentation: https://react.dev/
7. Ollama Documentation: https://ollama.com/

## Conclusion

The **AI-Powered Interview Evaluation & Resume Analysis System** is a strong final year project because it combines AI, NLP, web development, and database design into a practical real-world recruitment solution. It is suitable for academic demonstration, report writing, and further product development.
