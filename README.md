# Q-R-Based Check-In System

A simple system to manage event check-ins using QR codes. This project allows organizers to create events, generate QR codes, and track attendee check-ins efficiently.

**Live Demo:** *(if hosted, add your link here)*

## Features
- Generate unique QR codes for events
- Scan QR codes to mark attendance
- User authentication and role-based access
- Lightweight and easy to deploy

## Tech Stack
- Backend: Python, Flask
- Database: SQLite (or your choice)
- QR Code generation: `qrcode` Python library
- Frontend: HTML/CSS/JS (basic templates)

## Getting Started
1. Clone the repository:
```bash
git clone https://github.com/restapi404/Q-R-Based-Check-In-System.git
cd Q-R-Based-Check-In-System
```
2. Create a virtual environment:
```bash
python -m venv env
```
3. Install dependencies:
```bash
pip install -r requirements.txt
```
4. Run the server:
```bash
python main.py
```
5. Open `http://localhost:5000` in your browser.

## How to Add New Events
- Use the admin interface to create a new event.
- A unique QR code will be generated automatically for attendees.

## Contribution
Feel free to fork the repository, submit issues, or open pull requests to improve the project.

## License
MIT License © 2025
