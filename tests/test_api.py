def test_upload_csv(client, sample_csv_bytes):
    # TODO: Upload the sample CSV to POST /upload.
    # Assert status 200, six rows, two columns,
    response = client.post(
        '/upload',
        files={'file': ('sample_data.csv', sample_csv_bytes, 'text/csv')},
    )
    assert response.status_code == 200
    # and a positive integer dataset ID.
    result = response.json()
    assert result['rows'] == 6
    assert result['columns'] == 2
    assert isinstance(result['id'], int)
    assert result['id'] > 0


def test_process_and_retrieve(
    client, uploaded_dataset_id, processing_body
):
    # TODO 1: Send a POST request to
    # /datasets/{uploaded_dataset_id}/process
    response = client.post(
        f'/datasets/{uploaded_dataset_id}/process',
        json=processing_body,
    )
    assert response.status_code == 200

    # using json=processing_body.
    # Assert status 200, one validation removal,
    result = response.json()
    assert result['validation_rows_removed'] == 1

    # and a cleaning report showing 5 → 3 rows.
    report = result['cleaning_report']
    assert report['rows_before'] == 5
    assert report['rows_after'] == 3
    assert report['rows_removed'] == 2

    # TODO 2: GET /datasets/{uploaded_dataset_id}.
    response = client.get(f'/datasets/{uploaded_dataset_id}')

    # Assert status 200 and total_rows == 3.
    assert response.status_code == 200
    result = response.json()

    # Check that the returned records contain student IDs
    # 1, 2, and 5 with scores 80, 90, and 85.
    # Read the response as a dictionary.
    assert result['total_rows'] == 3
    assert result['data'] == [
        {'student_id': 1, 'score': 80},
        {'student_id': 2, 'score': 90},
        {'student_id': 5, 'score': 85},
    ]


def test_retrieve_missing_dataset(client):
    # TODO: Retrieve a dataset ID that does not exist.
    response = client.get(f'/datasets/{13013}')
    # Assert status 404.
    assert response.status_code == 404