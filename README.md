# Django Plotting App

## Overview
This Django web application allows users to generate and view plots of the function y = x^p. Users can input a value for 'p' and see the corresponding plot.

## Prerequisites
Before running this project, make sure you have the following installed:

- Python (3.8 or later)
- Django (3.2 or later)
- Matplotlib
- Numpy

These can be installed via pip if not already present on your system.

## Installation

### Clone the Repository
First, clone the repository to your local machine using:

```bash
git clone [https://github.com/your-username/your-repository-name.git](https://github.com/Chesta0703/function_plotter.git)
cd your-repository-name
cd your-repository-name
```

### Set Up a Virtual Environment (Optional but Recommended)

It's a good practice to create a virtual environment for Python projects. Use the following commands:

```
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
### Install Dependencies

Install the required Python modules with pip:
 ```
pip install -r requirements.txt

```
This command assumes you have a requirements.txt file in your repo with all the necessary packages listed.

### Initialize the Database

Run the following commands to set up the database:
```
python manage.py makemigrations
python manage.py migrate
```

### Run the Server

#### Start the Django development server:



```
python manage.py runserver
```

## Access the Application

Open your web browser and go to http://localhost:8000/ to use the application.

## Usage
Enter a value for 'p' in the provided text box and click the "Plot" button. The plot for y = x^p will be displayed below the form.
