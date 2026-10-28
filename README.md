## Cleaning Data API Description:

This API lets users upload CSV datasets, configure validation and
cleaning, and retrieve the processed rows. Cleaning options include removing
duplicates, handling missing values, and removing outliers. The API returns a JSON
report summarizing the changes. Reusable processing functions live in
`data_pipeline/`, and `main.py` connects them to the API.

## Data Movement:

1. Upload a CSV file with `POST /upload` and receive an ID
2. Submit validation and cleaning settings to `POST /datasets/{dataset_id}/process`
3. The API validates and cleans the dataset based on your config, then updates its stored data
4. The API returns a cleaning report as JSON
5. Retrieve the stored rows with `GET /datasets/{dataset_id}`

## Run the API:

From the `mp2-rest-api/` folder:

```bash
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Run pytest file:

```bash
python -m pytest tests -v
```

## Data Organization:


```text
mp2-rest-api/
├── .gitignore
├── README.md
├── main.py
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── middleware.py
│   ├── models.py
│   ├── storage.py
│   └── utils.py
├── data_pipeline/
│   ├── __init__.py
│   ├── data_loaders.py
│   ├── data_output.py
│   ├── data_processor.py
│   ├── data_validator.py
│   └── utils.py
├── fixtures/
│   ├── fake.txt
│   └── sample_data.csv
└── tests/
    ├── conftest.py
    └── test_api.py
```
