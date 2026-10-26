import io
import json
import logging
from pathlib import Path
import pandas as pd
from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from src import DatasetInfo, DatasetStorage, HealthResponse, setup_logging

setup_logging(verbose=True)
logger = logging.getLogger(__name__)

app = FastAPI(title="Data Processing API", version="1.0.0")
storage = DatasetStorage()

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Return the application status and version."""
    return HealthResponse(status='ok', version='1.0.0')

@app.post("/upload", response_model=DatasetInfo)
async def upload_dataset(file: UploadFile = File(...)):
    """Read and store a CSV upload."""
    suffix = Path(file.filename or "").suffix.lower()
    if suffix != '.csv':
        logger.error(f'Unsupported file format: {suffix}')
        raise HTTPException(400)

    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
    except pd.errors.EmptyDataError or pd.errors.ParserError or UnicodeDecodeError:
        logger.error("Empty upload file")
        raise HTTPException(400)


    dataset_id = storage.save(df, file.filename)
    metadata = storage.get_metadata(dataset_id)

    filename = metadata['filename']
    rows = metadata['rows']
    columns = metadata['columns']
    column_names = metadata['column_names']

    logger.info(f'Dataset ID: {dataset_id} | Filename: {filename} | Rows: {rows}')

    return DatasetInfo(id=dataset_id, filename=filename, rows=rows, columns=columns, column_names=column_names)

@app.get("/datasets/{dataset_id}")
def get_dataset(dataset_id: int, limit: int = Query(default=100, ge=1)):
    """Return up to limit rows from a stored dataset."""
    df = storage.get(dataset_id)
    if df is None:
        logger.warning("Dataset not found")
        raise HTTPException(404)

    records = json.loads(df.head(limit).to_json(orient="records"))
    logger.info(f'Returned dataset id: {dataset_id} | Returned Rows {len(df.head(limit))}')
    return {
        'id': dataset_id,
        'data': records,
        "total_rows": len(df),
    }
