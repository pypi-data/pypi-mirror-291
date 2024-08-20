import asyncio
import logging
import os
import time

import httpx
import polars as pl
from dotenv import load_dotenv
from rich import print
from utils import ConvertSeconds, create_directory

create_directory("logs")
create_directory("_outputs")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/geoquest.log"),
        logging.StreamHandler()
        ]
    )


# Load environment variables from .env file
load_dotenv('./config/.env')

# Get the OpenCage API key from environment variables
api_key = os.environ['OPEN_CAGE_API_KEY']

async def process_request(request):
    """
    Process a geocode request to the OpenCage API.

    Args:
        request (dict): A dictionary containing 'City' and 'State'.

    Returns:
        dict: A dictionary with the extracted state, city, and county information.
    """
    base_url = "https://api.opencagedata.com/geocode/v1/json"

    # Construct the API query parameters
    params = {'key': api_key, 'q': f"{request['City']}, {request['State']}", 'pretty': 1, 'no_annotations': 1}  # Use an f-string for more readable formatting

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(base_url, params=params)

            if response.status_code == 200:
                result = response.json()

                # Extract the required components from the API response
                components = result['results'][0].get('components', {})
                entered_city = request['City']
                entered_state = request['State']
                if components.get('city') is None:
                    city = entered_city
                else:
                    city = components.get('city')
                state = components.get('state')
                county_with_suffix = components.get('county')
                if county_with_suffix is None:
                    county = county_with_suffix
                else:
                    # Remove the 'County' suffix if present
                    county = county_with_suffix.replace(" County", "")

                return {'Entered City': entered_city, 'Entered State': entered_state, 'City': city, 'State': state, 'County': county, 'County with Suffix': county_with_suffix}
            # Handle API errors with a more informative message
            print(f"API Error: {response.status_code} - Unable to process request")
            return None

        except Exception as e:
            print(f"Error occurred while processing request: {e}")
            return None

async def get_county_for_user_inputs():
    city = input("Enter the city name: ")
    state = input("Enter the state name: ")
    request = {"City": city, "State": state}
    result = await process_request(request)
    if result is not None:
        logging.info("\nGeocoded Result:")
        for key, value in result.items():
            logging.info(f"{key}: {value}")


file_name = "city_state_input_data.csv"
data_input_folder_path = os.path.join(os.getcwd(), "data", "raw")

file_path = os.path.join(data_input_folder_path, file_name)


async def get_county_for_user_inputs_via_csv(file_path=os.path.join(data_input_folder_path, file_name)):

    start_time = time.time()

    # Read the CSV file into a Polars DataFrame
    df = pl.read_csv(file_path, has_header=True)

    results = []

    for row in df.iter_rows(named=True):
        result = await process_request(row)
        # Append the result to a list
        if result is not None:
            results.append(result)
            logging.info("\nGeocoded Result:")
            for key, value in result.items():
                logging.info(f"{key}: {value}")


    df_results = pl.from_dicts(results)

    # Convert the DataFrame to a CSV file
    output_file_name = "mapped_county_to_city_state.csv"
    output_folder = "_outputs"
    output_file_path = os.path.join(output_folder, output_file_name)

    df_results.write_csv(output_file_path)
    logging.info(f"\nData has been saved to {output_file_path}")

    end_time = time.time()
    elapsed_time_in_seconds = end_time - start_time

    logging.info(f"\nElapsed time to run complete code: {ConvertSeconds(elapsed_time_in_seconds)}")



async def main():
    print("GeoQuest Geocoder")
    print("----------------------")

    while True:
        print("\nMenu:")
        print("1. Get County Details by manually entering city and state")
        print("2. Get County Details by loading CSV file that contains city and state")
        print("3. Exit the program")

        choice = input("Enter your choice: ")

        if choice == "1":
            await get_county_for_user_inputs()

        elif choice == "2":
            await get_county_for_user_inputs_via_csv()
        elif choice == "3":
            print("Goodbye! Exiting the program.")
            break
        else:
            print("\nInvalid choice. Please try again.")


asyncio.run(main())
