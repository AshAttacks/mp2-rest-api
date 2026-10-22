import logging

logger = logging.getLogger(__name__)


class DatasetStorage:
    def __init__(self):
        self._store = {}
        self._counter = 0

    def save(self, df, filename):
        """Store a copy of the data and return a new integer ID."""
        # not sure how to do this one
        self._store[filename] = df
        self._counter = self._counter + 1


    def get(self, dataset_id):
        """Return a copy of the stored DataFrame, or None."""
        return self._store.get(dataset_id, None)

    def get_metadata(self, dataset_id):
        """Return the dataset metadata, or None."""
        metadata = self._store.get(dataset_id, None)['DatasetInfo'] # field is DatasetInfo

    def update(self, dataset_id, df):
        """Replace an existing dataset; return True, or False if missing."""
        self._store[dataset_id] = df
        pass

    def clear(self):
        """Clear all data and reset the ID counter."""
        self._store.clear()
        self._counter = 0