# Q-Airline

This project is a modern web application using **Vue.js** for the frontend, **FastAPI** for the backend, and **Supabase** for storage and CDN. 

## Features
- **Frontend**: Interactive and dynamic UI built with Vue.js.
- **Backend**: High-performance REST API powered by FastAPI.
- **Storage**: File storage, database, and authentication handled by Supabase.
- **CDN**: Efficient content delivery for static assets via Supabase.

---

## Getting Started

### Prerequisites
- **Node.js** (v16+ recommended)
- **Python** (3.8+)
- **Supabase Account** (to configure your backend storage and CDN)

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/darklord1611/Q-Airline
   cd Q-Airline
   ```

2. **Setup Frontend**:
   ```bash
   cd frontend # remember to setup your env variables according to README.md in frontend folder
   npm i
   npm run dev
   ```

3. **Setup Backend**:
   ```bash
   cd backend # remember to setup your env variables according to README.md in backend folder
   pip install requirements.txt
   python -m uvicorn main:app --port 8000 --reload # or source start.sh
   ```
