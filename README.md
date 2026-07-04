# Looqbox Data Challenge

This repository contains my solution for the Looqbox technical challenge.

The project was developed using Python, SQL, and Streamlit to query a MySQL database and present the results through an interactive web application.

## Technologies

- Python 3.14
- Streamlit
- Pandas
- PyMySQL
- Matplotlib
- MySQL

## Project Structure

```text
LOOQBOX_CHALLENGE/
│
├── streamlit_app/
│   ├── app.py
│   └── functions.py
│
├── README.md
├── requirements.txt
└── solutions.ipynb
```

## How to Run

1. Clone the repository:

```bash
git clone <repository-url>
```

2. Create a virtual environment:

```bash
python -m venv .venv
```

3. Activate the virtual environment.

On Windows:

```bash
.venv\Scripts\activate
```

On Linux or macOS:

```bash
source .venv/bin/activate
```

4. Install the dependencies:

```bash
pip install -r requirements.txt
```

5. Run the application:

```bash
streamlit run streamlit_app/app.py
```

## Project Files

- `app.py`: Streamlit application interface.
- `functions.py`: Helper functions for database queries and data processing.
- `solutions.ipynb`: Jupyter Notebook containing the SQL queries and challenge solutions.

## Notes

To run this project, you must have access to the MySQL database provided for the challenge and configure the database connection credentials before starting the application.