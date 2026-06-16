# PASSWORD_CHECKING

<p align="center">
    <img src="image.png" alt="Password Checking" width="700">
</p>

A password strength evaluation project that analyzes passwords using multiple algorithms and approaches, including:

* Brute Force
* Dynamic Programming
* Greedy Algorithm
* Mathematical Model

---

# Table of Contents

* [Overview](#overview)
* [Requirements](#requirements)
* [Installation](#installation)

  * [Install Python](#install-python)
  * [Create a Virtual Environment](#create-a-virtual-environment)
  * [Activate the Virtual Environment](#activate-the-virtual-environment)
  * [Install Dependencies](#install-dependencies)
* [Project Structure](#project-structure)
* [Running the Project](#running-the-project)
* [Modules Description](#modules-description)
* [Example Usage](#example-usage)

---

# Overview

This project evaluates password strength using different algorithms and security rules.

Features:

* Password analysis
* Password strength scoring
* Multiple algorithm implementations
* Educational and research purposes

---

# Requirements

* Python 3.8 or later
* Windows, Linux, or macOS

Check your Python version:

```bash
python --version
```

or

```bash
python3 --version
```

---

# Installation

## Install Python

### Windows

Download Python from:

https://www.python.org/downloads/

During installation, make sure to enable:

```text
Add Python to PATH
```

Verify installation:

```bash
python --version
```

### Linux (Ubuntu/Debian)

```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### macOS

```bash
brew install python
```

---

## Create a Virtual Environment

Navigate to the project directory:

```bash
cd PASSWORD_CHECKING
```

Create a virtual environment named `env`:

```bash
python -m venv env
```

or

```bash
python3 -m venv env
```

---

## Activate the Virtual Environment

### Windows (Command Prompt)

```cmd
env\Scripts\activate.bat
```

### Windows (PowerShell)

```powershell
.\env\Scripts\Activate.ps1
```

### Linux

```bash
source env/bin/activate
```

### macOS

```bash
source env/bin/activate
```

After activation, your terminal should display:

```text
(env)
```

---

## Install Dependencies

If a `requirements.txt` file exists:

```bash
pip install -r requirements.txt
```

To verify installed packages:

```bash
pip list
```

---

# Project Structure

```text
PASSWORD_CHECKING/
│
├── algorithms/
│   ├── Brute_Force.py
│   ├── Dynamic_Programming.py
│   ├── Greedy.py
│   └── Math_Model.py
│
├── env/
│
├── __init__.py
├── image.png
├── passwords.txt
├── pwd_checking.py
├── README.md
└── rules.py
```

---

# Modules Description

## algorithms/

Contains all password evaluation algorithms.

### Brute_Force.py

Implements a brute-force based password analysis approach.

### Dynamic_Programming.py

Implements password evaluation using dynamic programming techniques.

### Greedy.py

Implements a greedy strategy for fast password assessment.

### Math_Model.py

Uses mathematical formulas and models to estimate password strength.

---

## rules.py

Defines password validation and scoring rules, such as:

* Minimum length
* Uppercase letters
* Lowercase letters
* Digits
* Special characters
* Additional security constraints

---

## passwords.txt

Contains password samples used for testing.

---

## **init**.py

Main entry point of the application.

Responsible for:

* Loading passwords
* Applying evaluation algorithms
* Generating results
* Displaying password strength reports

---

# Running the Project

Activate the virtual environment first.

Run the main application:

```bash
python __init__.py
```

or

```bash
python3 __init__.py
```

---

# Example Usage

Example content of `passwords.txt`:

```text
123456
password
Admin123
Admin@123
P@ssw0rd2025
```

Run:

```bash
python __init__.py
```