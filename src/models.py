from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    version: str


class DatasetInfo(BaseModel):
    # TODO: id (int), filename (str), rows (int),
    id: int
    filename: str
    rows: int
    # columns (int), column_names (list[str])
    columns: int
    column_names: list[str]