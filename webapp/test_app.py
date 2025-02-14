from main import app
import pytest
from fastapi.testclient import TestClient

def test_length_of_ratings():
    client = TestClient(app)
    response = client.get("/api/ratings")
    assert response.status_code == 200
    assert len(response.json()['results']) == 50


def test_request_time():
    client = TestClient(app)
    response = client.get("/api/ratings")
    assert response.elapsed.total_seconds() < 3


# Test Database output directly
import sqlite3
from main import db_file, sql_file

@pytest.fixture(scope="session")
def db_fixture(request):
    with open(sql_file, "r") as file:
        query = file.read()
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()

    # Convert results to a list of dictionaries
    keys = ["name", "region", "variety", "wine_year", "rating", "rolling_avg_rating", "performance_ratio", "performance_trend", "rating_category"]
    results_dict = [dict(zip(keys, row)) for row in results]
    return results_dict

def test_db_length(db_fixture):
    assert len(db_fixture) == 50

def test_region_is_not_empty(db_fixture):
    assert all([result['region'] for result in db_fixture])

def test_rating_is_not_empty(db_fixture):
    assert all([result['rating'] for result in db_fixture])

def test_rolling_avg_rating_is_not_empty(db_fixture):
    assert all([result['rolling_avg_rating'] for result in db_fixture])

def test_performance_ratio_is_not_empty(db_fixture):
    assert all([result['performance_ratio'] for result in db_fixture])

def test_performance_trend_is_not_empty(db_fixture):
    assert all([result['performance_trend'] for result in db_fixture])

def test_rating_category_is_not_empty(db_fixture):
    assert all([result['rating_category'] for result in db_fixture])

def test_rating_category_is_valid(db_fixture):
    valid_categories = ['Low Rating', 'Medium Rating', 'High Rating']
    assert all([result['rating_category'] in valid_categories for result in db_fixture])
