# Extract loci from PDF Files - "Mother and Child" and "Evrolab" Laboratories
![PyPI - Version](https://img.shields.io/pypi/v/django?style=for-the-badge&logo=Django&logoColor=green&label=Django&color=hex)

<br>

## Project Overview

This project is dedicated to the extraction of DNA loci information from PDF reports, specifically those generated by the "Mother and Child" and "Evrolab" laboratories.

## Objectives

The primary aim is to extract the father's DNA loci from these PDF documents. Once extracted, this data is utilized to match the loci against a database of potential fathers for paternity determination.

## Challenge and Solution

The quality of the PDF files from "Evrolab" is notably poor, which presents a significant challenge for standard PDF text extraction libraries in Python, such as PyPDF2 and PyMuPDF (fitz).

To overcome this hurdle, the project leverages the AWS Textract microservice. AWS Textract is known for its advanced text recognition capabilities, which are particularly effective in handling documents with poor quality.

<br>

## Key Features - Development stage

### AJAX PDF Upload Form
- **Drag-and-Drop Interface**: Offers a drag-and-drop interface for bulk uploading of PDFs, with built-in validation to accept only PDF files, ensuring asynchronous and efficient file uploads.
<img src="https://github.com/rodionmaulenov/TextExtractPdf/assets/109179333/f9ebaf15-e28e-4989-8eb2-5a533ee91b30" width="300" alt="Drag form">
<img src="https://github.com/rodionmaulenov/TextExtractPdf/assets/109179333/2cbd2336-2f77-43c1-8378-a1dc3d9d1c6a" width="300" alt="Filled drag form">

### Father's Instance Creation
- **Automated Data Extraction**: Automatically extracts data from uploaded father's DNA loci reports, updating the father list in the database for easy data management. Used addditional module for customizing django admin interface.
<img src="https://github.com/rodionmaulenov/TextExtractPdf/assets/109179333/25af857c-01e9-455e-bde8-6a773b4a250d" width="300" alt="Main fathers list">

### Child Loci Input Form
- **Paternity Search**: Facilitates paternity searches by allowing entry of a child's loci. The form accommodates different numbers of loci, ranging from 14 to 22, and includes data validation to ensure the correctness of the input data.
<img src="https://github.com/rodionmaulenov/TextExtractPdf/assets/109179333/69b843cb-4085-470e-913e-d7a2432c042e" width="300" alt="form to find father">
<img src="https://github.com/rodionmaulenov/TextExtractPdf/assets/109179333/06a697fe-2766-4547-b8d5-3510d7fb6b96" width="300" alt="form to find father">

<br>
<br>
<br>

## On Production stage

### Containerization and Deployment
- **Docker Containers**: Application and supporting services like Nginx and Certbot are containerized with Docker for consistency.
- **Digital Ocean Deployment**: The application is hosted on Digital Ocean, providing a robust and scalable environment.

### CI/CD with GitHub Actions
- **Automated Workflows**: Utilizes GitHub Actions for seamless CI/CD, streamlining testing, updates and deployment processes.

### Database and Storage
- **Digital Ocean Postgres**: Employs Digital Ocean's Postgres service for efficient database management.
- **DO Spaces**: Uses Digital Ocean Spaces for secure and accessible storage of PDF files.
<img src="https://github.com/rodionmaulenov/TextExtractPdf/assets/109179333/13a02527-1279-488b-8652-8959e3093507" width="300" alt="form to find father">

<br>
<br>
<br>

## How launch project on Linux local server 

### Step 1: Create a Directory

Open your terminal and create a new directory for your project:
  ```python
mkdir project-name
cd project-name
```
### Step 2: Create a Virtual Environment

Set up a virtual environment to manage your Python dependencies:
```python
virtualenv myenv
```
### Step 3: Activate the Virtual Environment

Activate the virtual environment:
```python
source myenv/bin/activate
``` 
### Step 4: Clone the Project from GitHub

Copy the project from GitHub:
```python
git clone git@github.com:rodionmaulenov/TextExtractPdf.git
cd TextExtractPdf
```
### Step 5: Create a requirements.txt File

Create a requirements.txt file with the following dependencies:
```python
django>=3.2,<4.0
psycopg2-binary==2.9.9 
gunicorn==21.2.0
django-admin-interface==0.26.1
boto3==1.28.64
textract-trp==0.1.3
python-decouple==3.8
django-storages==1.14.2
django-cleanup==8.0.0
PyMuPDF==1.23.5
requests==2.31.0
```

### Step 6: Install Dependencies

Install the required dependencies:
```python
pip isntall -r requirements.txt
```
### Step 7: Launching the Project with Docker

Launch your Django project using Docker:
```python
docker-compose up --build
```




