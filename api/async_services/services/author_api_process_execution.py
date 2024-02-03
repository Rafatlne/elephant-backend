# tasks.py
from datetime import datetime

from django_rq import job


@job('default', timeout='2m')
def process_author_details_task(page_data):
    try:
        from api.async_services.services.social_media_content_service import process_author_json
        # Process the API response data using the utility function
        result = process_author_json(page_data)

        # Log the result or handle it as needed
        print(f"Processing result: {result}")

    except Exception as e:
        # Handle exceptions
        print(f"An error occurred: {e}")

    # Log the completion time
    completion_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    print(f"Task completed at {completion_time}")
