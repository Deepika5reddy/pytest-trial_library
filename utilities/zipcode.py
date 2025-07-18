import random

def get_realistic_zip_codes(count=3):
    # Sample list of known valid metro-area ZIP codes
    zip_pool = [
        "60616",  # Chicago
        "10001",  # New York
        "94105",  # San Francisco
        "30301",  # Atlanta
        "80202",  # Denver
        "90001",  # Los Angeles
        "75201",  # Dallas
        "33101",  # Miami
        "98101",  # Seattle
        "19103",  # Philadelphia
    ]
    return random.sample(zip_pool, count)
