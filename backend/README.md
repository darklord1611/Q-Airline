## Supabase Project Setup Guide

This guide will help you create a new project on **Supabase** and import a SQL file to set up your database.

---

### Step 1: Create a Supabase Account

1. Go to [Supabase](https://supabase.com).
2. Sign up for an account or log in if you already have one.
3. Once logged in, you’ll be redirected to the dashboard.

---

### Step 2: Create a New Project

1. Click the **"New Project"** button in the dashboard.
2. Fill in the following details:
   - **Project Name**: Enter a name for your project.
   - **Database Password**: Create a secure password for your database.
   - **Region**: Choose the region closest to your target audience.
3. Click **"Create New Project"** to initialize your project.

> **Note:** Supabase will take a few moments to set up your project.

---

### Step 3: Access the Database

1. Once your project is ready, go to the **"Database"** tab in your Supabase dashboard.
2. Scroll down to the **Connection Pooling** or **Connection Details** section.
   - Note the **Connection String** and database credentials. These will be useful for external connections.

---

### Step 4: Import a SQL File to Create a Database

#### Option 1: Using the Supabase Dashboard

1. Navigate to the **"SQL Editor"** tab in the Supabase dashboard.
2. Click the **"New Query"** button.
3. Open the file `schema.sql` in a text editor and copy its contents.
4. Paste the SQL script into the query editor.
5. Click **"Run"** to execute the SQL script.

## Backend

Create `.env` file and copy env variables from .env.example into `.env` file

```sh
$ pip install -r requirements.txt
```

```sh
# Khởi chạy ứng dụng demo cho Linux/Mac
$ source start.sh 
```

```sh
# Khởi chạy ứng dụng demo cho Windows
$ python3 -m uvicorn main:app --port 8000 --reload 
```

Go to `http://localhost:8000/docs` to see the API docs and related endpoints