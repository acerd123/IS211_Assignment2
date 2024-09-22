import argparse
import urllib.request
import logging
import datetime

def downloadData(url):
    """Downloads the data"""
    with urllib.request.urlopen(url) as response:
        return response.read().decode('utf-8')

def processData(file_content):
    logger = logging.getLogger('assignment2')
    logger.setLevel(logging.ERROR)

    data_dict = {}
    lines = file_content.strip().split('\n')

    for i, line in enumerate(lines, start=1):
        parts = line.split(',')
        try:
            person_id = int(parts[0].strip())
            name = parts[1].strip()
            birthday_str = parts[2].strip()
            birthday = datetime.datetime.strptime(birthday_str, '%d/%m/%Y')
            data_dict[person_id] = (name, birthday)

        except (ValueError, IndexError):
            # Log errors if there's a problem with the date or line structure
            logger.error(f"Error processing line #{i} for ID #{parts[0] if len(parts) > 0 else 'N/A'}")
             
    return data_dict


def displayPerson(id, personData):
    if id in personData:
        name, birthday = personData[id]
        print(f"Person #{id} is {name} with a birthday of {birthday.strftime('%Y-%m-%d')}")
    else:
        print(f"No user found with that id")

def main(url):
    print(f"Running main with URL = {url}...")
    logging.basicConfig(filename='errors.log', level=logging.ERROR)

    try:
        # Download the data
        csvData = downloadData(url)
    except Exception as e:
        print(f"Failed to download data: {e}")
        return
    personData = processData(csvData)
    while True:
        try:
            person_id = int(input("Enter ID to lookup, or a negative number to quit: "))
            if person_id <= 0:
                break
            displayPerson(person_id, personData)
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
        


if __name__ == "__main__":
    """Main entry point"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", help="URL to the datafile", type=str, required=True)
    args = parser.parse_args()
    main(args.url)
