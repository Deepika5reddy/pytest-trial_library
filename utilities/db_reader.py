# utilities/db_reader.py
import mysql.connector

def get_trial_data_from_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="$ervices1",
        database="trial_library"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, location, zip_code, radius, conditions, status FROM trial_search_results")
    rows = cursor.fetchall()
    conn.close()

    # Format to match API-like structure
    data = [
        {
            "sponsored_trial_acronym": row[0],
            "sponsored_trial_name": row[1],
            "closest_sponsored_trial_location_name": row[2],
            "zip5_code": row[3],
            "radius_in_miles": row[4],
            "sponsored_trial_conditions": row[5],
            "status": row[6]
        }
        for row in rows
    ]
    return data
