import requests
import pytest
from itertools import product
from utilities.configuration import get_trial_search_base_url
from utilities.zipcode import get_realistic_zip_codes
from utilities.schema_validator import REQUIRED_FIELDS
from utilities.chicago_expected_trials import expected_pairs

ZIP_CODES = get_realistic_zip_codes(count=2)
RADIUS_VALUES = [50, 100, 150, 250, 6000]
BASE_URL = get_trial_search_base_url()

# Create combinations of zip and radius
test_cases = list(product(ZIP_CODES, RADIUS_VALUES))

@pytest.mark.positive
@pytest.mark.parametrize("zip_code,radius", test_cases)
def test_trial_search_by_zip_and_radius(zip_code, radius):
    """Validate API response for combination of zipcode and radius"""
    params = {
        "zip5_code": zip_code,
        "radius_in_miles": radius
    }
    response = requests.get(BASE_URL, params=params)

    assert response.status_code == 200, f"Status code {response.status_code} for zip {zip_code} radius {radius}"

    data = response.json()
    assert isinstance(data, list), f"Response is not a list for zip {zip_code} radius {radius}"

@pytest.mark.negative
@pytest.mark.parametrize("radius", [0, -1, -100,])
def test_trial_search_invalid_radius(radius):
    zip_code = "60616"
    response = requests.get(BASE_URL, params={"zip5_code": zip_code, "radius_in_miles": radius})
    assert response.status_code == 400

@pytest.mark.negative
def test_trial_search_empty_zipcode():
    """Verify that API returns an error for empty ZIP code"""
    params = {
        "zip5_code": "",  # empty ZIP code
        "radius_in_miles": 100
    }
    response = requests.get(BASE_URL, params=params)

    # You can adjust expected status code if API returns 400, 422, etc.
    assert response.status_code == 400, (
        f"Expected failure for empty ZIP code, but got {response.status_code}"
    )

@pytest.mark.schema
@pytest.mark.parametrize("zip_code,radius", test_cases)
def test_trial_search_response_schema(zip_code, radius):
    """Test if the response schema matches the expected structure fromm schema validator"""
    params = {"zip5_code": zip_code, "radius_in_miles": radius}
    response = requests.get(BASE_URL, params=params)

    assert response.status_code == 200, f"Expected 200, got {response.status_code} for {zip_code=} {radius=}"

    data = response.json()
    assert isinstance(data, list), f"Response should be a list for {zip_code=} {radius=}"

    for trial in data:
        assert isinstance(trial, dict), "Each trial must be a dictionary"
        for field, expected_type in REQUIRED_FIELDS.items():
            assert field in trial, f"Missing field: {field}"
            assert isinstance(trial[field], expected_type), (
                f"Field '{field}' has type {type(trial[field])}, expected {expected_type}"
            )

@pytest.mark.schema
@pytest.mark.positive
@pytest.mark.parametrize("zip_code,radius", test_cases)
def test_required_field_values_are_valid(zip_code, radius):
    params = {
        "zip5_code": zip_code,
        "radius_in_miles": radius
    }
    response = requests.get(BASE_URL, params=params)
    assert response.status_code == 200, f"Status {response.status_code} for {zip_code=} {radius=}"

    data = response.json()
    assert isinstance(data, list), f"Expected list, got {type(data)}"

    for trial in data:
        # Trial name must not be empty
        assert trial.get("sponsored_trial_name"), f"Missing name for {zip_code=} {radius=}"

        # URL must start with http/https
        url = trial.get("sponsored_trial_study_url", "")
        assert url.startswith("http"), f"Invalid URL '{url}' for {zip_code=} {radius=}"

        # Phase must be a valid value
        assert trial.get("sponsored_trial_phase") in ["1", "1/2", "2", "2b", "3", "N/A"], \
            f"Unexpected trial phase for {zip_code=} {radius=}"

        # Distance should not exceed radius
        distance = trial.get("distance_to_closest_location_in_miles")
        assert distance is not None and distance <= radius, \
            f"Distance {distance} > radius {radius} for {zip_code=}"

        # Investigator name checks
        assert trial.get("closest_principal_investigator_first_name"), "Missing PI first name"
        assert trial.get("closest_principal_investigator_last_name"), "Missing PI last name"

        # Location name must exist
        assert trial.get("closest_sponsored_trial_location_name"), "Missing trial location name"


@pytest.mark.schema
@pytest.mark.positive
def test_trial_search_chicago_trail():
    zip_code = "60616"
    radius = 6000

    response = requests.get(BASE_URL, params={"zip5_code": zip_code, "radius_in_miles": radius})
    assert response.status_code == 200

    data = response.json()  # <- define `data` here
    found_pairs = [(trial.get("sponsored_trial_acronym", ""), trial.get("sponsored_trial_conditions", "")) for trial in data]

    for expected in expected_pairs:
        assert expected in found_pairs, f"Expected pair {expected} not found in the response."