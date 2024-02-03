# tasks.py
import time
from datetime import datetime, timedelta
from rq import get_current_job
from django_rq import job, get_queue
import requests

from api.async_services.services.author_api_process_execution import process_author_details_task


@job('default', timeout='2m')
def execute_author_api(author_id):
    api_url = f"https://hackapi.hellozelf.com/backend/api/v1/authors/{author_id}?page={{}}"
    api_key = "1fb5d9bfsk_3666sk_436ask_9bdcsk_e4b5ba99e9ba1706932443"
    headers = {'x-api-key': api_key}

    api_calls_per_minute = 2
    seconds_per_minute = 60
    wait_time_5min = 5 * 60
    # Get the current job
    job_instance = get_current_job()
    default_queue = get_queue("default")

    try:
        # Make the initial API call to get total_contents and page_size
        response = requests.get(api_url.format(1), headers=headers)
        response.raise_for_status()
        data = response.json()
        from api.async_services.services.contents_api_process_execution import process_author_social_content_task
        process_author_details_task(data["data"])

        total_contents = data.get("total_contents", 0)
        page_size = data.get("page_size", 30)

        # Calculate the number of pages
        num_pages = (total_contents + page_size - 1) // page_size

        # Calculate the delay between API calls to stay within the rate limit
        delay_between_calls = seconds_per_minute / api_calls_per_minute

        # Loop through the calculated number of pages
        for page_number in range(1, num_pages + 1):
            # Make API call for each page
            response = requests.get(api_url.format(page_number), headers=headers)
            response.raise_for_status()
            page_data = response.json()
            from api.async_services.services.contents_api_process_execution import process_author_social_content_task
            process_author_details_task(page_data["data"])
            # time.sleep(delay_between_calls)

        # time.sleep(delay_between_calls)
    except requests.exceptions.HTTPError as err:
        if response.status_code == 429:  # HTTP status code for rate limit exceeded
            # Retry the job after waiting for 5 minutes
             # 5 minutes in seconds
            job_instance.meta['delay'] = wait_time_5min
            job_instance.save()

    except Exception as e:
        # Handle other exceptions
        print(f"An error occurred: {e}")

    # Log the completion time
    completion_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    print(f"Job completed at {completion_time}")
