# Cyber Security Base 2025, Project I

This project was developed for the Cyber Security Base course at the University of Helsinki. 

The web application is a simple journal application, where users can save, view, and delete journal entries. As a part of the assignment,
the application contains five vulnerabilities from the OWASP Top 10 2021 list. The solutions for these vulnerabilities are also provided in
the source code (commented out).


## Instructions for installation and use

These instructions are specifically for Linux users. The commands may differ slightly depending on the OS. 

### Requirements
* Python 3.12 or higher

### Installation

Clone the repository and move to its root directory:
```bash
git clone https://github.com/uyenmh/cybersecurity-projectI.git
cd cybersecurity-projectI
```

Install the dependencies:
```bash
pip install -r requirements.txt
```

Apply the database migrations:
```bash
python3 manage.py migrate
```

### Use

Start the development server:
```bash
python3 manage.py runserver
```

Then open your browser and navigate to <http://127.0.0.1:8000/>.
