# RKV SPORTS

A comprehensive platform for managing sports activities on campus. RKV SPORTS offers a seamless experience for tournament management, live score updates, notifications, and detailed information about the Physical Education Department (PET). The project is designed to cater to both students/players and faculty/organizers, making sports events organized and engaging.

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction
RKV SPORTS is aimed at digitizing and simplifying campus sports management by allowing students to register for tournaments, receive notifications, and access real-time scores. The platform also empowers faculty to organize and oversee sports events efficiently.

## Features
- User authentication and role-based login (students/players and faculty/organizers).
- Live updates for scores and event notifications.
- A dedicated section for PET information and sports news.
- Easy registration for upcoming tournaments and events.
- Comprehensive tournament management for faculty.

## Technology Stack
- **Frontend**: React.js, Next.js
- **Backend**: FastAPI
- **Database**: MongoDB

## Installation
To set up the project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Harshad712/RKV-SPORTS-API.git
   cd RKV-Sports

2. **Create a virtual environment** (optional but recommended):

    ```bash
    python -m venv venv
    ```

   Activate the virtual environment:

   - **On Windows**:

     ```bash
     venv\Scripts\activate
     ```

   - **On macOS/Linux**:

     ```bash
     source venv/bin/activate
     ```

3. **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

## Running the Server

1. **Run the FastAPI server**:

    ```bash
    fastapi dev main.py
    ```
    ```windows
    python -m uvicorn main:app --reload
    ```

2. **Access the API**:

   The server will start at `http://127.0.0.1:8000`. You can view the automatically generated interactive API docs at: `http://127.0.0.1:8000/docs`