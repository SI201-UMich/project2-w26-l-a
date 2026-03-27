# SI 201 Project 2 - Airbnb Data Scraping and Analysis
# Your name: Loryn Canty 
# Your student id: 31004224
# Your email: lorync@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT):
# Your name: Ailyn Moreno
# Your student id: 49537383
# Your email: ailynm@umich.edu
# If you worked with generative AI also add a statement for how you used it.
# e.g.:
# Asked ChatGPT for hints on debugging and for suggestions on overall code structure
#Used ChatGPT to help with debugging and strucural issues
# Did your use of GenAI on this assignment align with your goals and guidelines in your Gen AI contract? If not, why?
#Yes as I didn't have time to go to office hours
# --- ARGUMENTS & EXPECTED RETURN VALUES PROVIDED --- #
# --- SEE INSTRUCTIONS FOR FULL DETAILS ON METHOD IMPLEMENTATION --- #

from turtle import title

from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import requests  # kept for extra credit parity


# IMPORTANT NOTE:
"""
If you are getting "encoding errors" while trying to open, read, or write from a file, add the following argument to any of your open() functions:
    encoding="utf-8-sig"
"""


def load_listing_results(html_path) -> list[tuple]:
    """
    Load file data from html_path and parse through it to find listing titles and listing ids.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples containing (listing_title, listing_id)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    results = []

    with open(html_path, "r", encoding="utf-8-sig") as f:
        soup = BeautifulSoup(f, "html.parser")

    title_tags = soup.find_all("div", {"data-testid": "listing-card-title"})

    for title_tag in title_tags:
        title = title_tag.get_text(strip=True)
        listing_id = title_tag.get("id").replace("title_", "")
        results.append((title, listing_id))

    return results
    # pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def get_listing_details(listing_id) -> dict:
    """
    Parse through listing_<id>.html to extract listing details.

    Args:
        listing_id (str): The listing id of the Airbnb listing

    Returns:
        dict: Nested dictionary in the format:
        {
            "<listing_id>": {
                "policy_number": str,
                "host_type": str,
                "host_name": str,
                "room_type": str,
                "location_rating": float
            }
        }
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    file_path = os.path.join("html_files", f"listing_{listing_id}.html")
    with open(file_path, "r", encoding="utf-8-sig") as f:
        soup = BeautifulSoup(f, "html.parser")
    text = soup.text

    policy_number = "Exempt"
    match = re.search(r"(20\d{2}-00\d{4}STR|STR-000\d{4})", text)
    if match:
        policy_number = match.group()
    elif "pending" in text.lower():
        policy_number = "Pending"
    elif "exempt" in text.lower():
        policy_number = "Exempt"

    if "Superhost" in text:
        host_type = "Superhost"
    else:
        host_type = "regular"
    
    host_name = ""
    host_tag = soup.find("h2", string=re.compile(r"Hosted by", re.I))
    if host_tag:
        full_text = host_tag.text.replace("\xa0", " ")
    parts = re.split(r"hosted by", full_text, flags=re.I)
    if len(parts) > 1:
        host_name = parts[-1].strip()
    else:
        host_name = full_text.replace("Hosted by", "").strip()
    room_type = "Entire Room"
    subtitle_tag = soup.find("h2")
    if subtitle_tag:
        subtitle = subtitle_tag.text
        if "Private" in subtitle:
            room_type = "Private Room"
        elif "Shared" in subtitle:
            room_type = "Shared Room"

    location_rating = 0.0
    location_label_div = soup.find('div', class_='_y1ba89', string='Location')
    if location_label_div:
        outer_container = location_label_div.find_parent('div', class_='_a3qxec')
        if outer_container:
            rating_span = outer_container.find('span', class_='_4oybiu')
            if rating_span:
                location_rating = float(rating_span.text.strip())

    return {
        "policy_number": policy_number,
        "host_type": host_type,
        "host_name": host_name,
        "room_type": room_type,
        "location_rating": location_rating
    }
    # pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def create_listing_database(html_path) -> list[tuple]:
    """
    Use prior functions to gather all necessary information and create a database of listings.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples. Each tuple contains:
        (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
  
    results = []
    listings = load_listing_results(html_path)
    for listing_title, listing_id in listings:
        details = get_listing_details(listing_id)
        policy_number = details.get("policy_number")
        host_type = details.get("host_type")
        host_name = details.get("host_name")
        room_type = details.get("room_type")
        location_rating = details.get("location_rating")

        listing_tuple = (
            listing_title,
            listing_id,
            policy_number,
            host_type,
            host_name,
            room_type,
            location_rating,
        )

        results.append(listing_tuple)
    return results

    # pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def output_csv(data, filename) -> None:
    """
    Write data to a CSV file with the provided filename.

    Sort by Location Rating (descending).

    Args:
        data (list[tuple]): A list of tuples containing listing information
        filename (str): The name of the CSV file to be created and saved to

    Returns:
        None
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    
    sorted_data = sorted(data, key=lambda x: x[-1] or 0, reverse=True)
    file = open(filename, 'w', newline='')
    writer = csv.writer(file)
    writer.writerow([
        "Listing Title",
        "Listing ID",
        "Policy Number",
        "Host Type",
        "Host Name",
        "Room Type",
        "Location Rating"
    ])
    for row in sorted_data:
        writer.writerow(row)
    file.close()

    # pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def avg_location_rating_by_room_type(data) -> dict:
    """
    Calculate the average location_rating for each room_type.

    Excludes rows where location_rating == 0.0 (meaning the rating
    could not be found in the HTML).

    Args:
        data (list[tuple]): The list returned by create_listing_database()

    Returns:
        dict: {room_type: average_location_rating}
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    ratings = {}
    counts = {}
    for row in data:
        room_type = row[5]
        location_rating = row[6]
        if location_rating == 0.0:
            continue
        if room_type not in ratings:
            ratings[room_type] = 0.0
            counts[room_type] = 0
        ratings[room_type] += location_rating
        counts[room_type] += 1
    for room_type in ratings:
        ratings[room_type] /= counts[room_type]
    return ratings
    #pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def validate_policy_numbers(data) -> list[str]:
    """
    Validate policy_number format for each listing in data.
    Ignore "Pending" and "Exempt" listings.

    Args:
        data (list[tuple]): A list of tuples returned by create_listing_database()

    Returns:
        list[str]: A list of listing_id values whose policy numbers do NOT match the valid format
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    misformatted_listings = []
    pattern = r"^(20\d{2}-00\d{4}STR|STR-\d{7})$"
    for row in data:
        listing_id = row[1]
        policy_number = str(row[2]).strip()
        room_type = row[5]

        if policy_number == "Exempt":
            continue

        if policy_number == "Pending":
            if room_type == "Entire Room":
                continue
            misformatted_listings.append(listing_id)
            continue

        if not re.match(pattern, policy_number):
            misformatted_listings.append(listing_id)
    return misformatted_listings

    #pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


# EXTRA CREDIT
def google_scholar_searcher(query):
    """
    EXTRA CREDIT

    Args:
        query (str): The search query to be used on Google Scholar
    Returns:
        List of titles on the first page (list)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================

    url = "https://scholar.google.com/scholar"
    params = {
        "q": query
    }
    r = requests.get(url, params=params,)
    
    soup = BeautifulSoup(r.text, "html.parser")
    titles = []
    for tag in soup.find_all("h3", class_="gs_rt"):
        titles.append(tag.get_text(strip=True))
    return titles

    # pass
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


class TestCases(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.search_results_path = os.path.join(self.base_dir, "html_files", "search_results.html")

        self.listings = load_listing_results(self.search_results_path)
        self.detailed_data = create_listing_database(self.search_results_path)

    def test_load_listing_results(self):
        # TODO: Check that the number of listings extracted is 18.
        self.assertEqual(len(self.listings), 18)
        # TODO: Check that the FIRST (title, id) tuple is  ("Loft in Mission District", "1944564").
        self.assertEqual(self.listings[0], ("Loft in Mission District", "1944564"))
        # pass

    def test_get_listing_details(self):
        html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]

        # TODO: Call get_listing_details() on each listing id above and save results in a list.
        results = [get_listing_details(i) for i in html_list]
        # TODO: Spot-check a few known values by opening the corresponding listing_<id>.html files.
        # 1) Check that listing 467507 has the correct policy number "STR-0005349".
        # 2) Check that listing 1944564 has the correct host type "Superhost" and room type "Entire Room".
        # 3) Check that listing 1944564 has the correct location rating 4.9.
        self.assertEqual(results[0]["policy_number"], "STR-0005349")
        self.assertEqual(results[2]["host_type"], "Superhost")
        self.assertEqual(results[2]["room_type"], "Entire Room")
        self.assertEqual(results[2]["location_rating"], 4.9)
        # pass

    def test_create_listing_database(self):
        # TODO: Check that each tuple in detailed_data has exactly 7 elements:
        # (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
        for item in self.detailed_data:
            self.assertEqual(len(item), 7)
        # TODO: Spot-check the LAST tuple is ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8).
        self.assertEqual(
        self.detailed_data[-1],
            ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8)
        ) 
        # pass

    def test_output_csv(self):
        out_path = os.path.join(self.base_dir, "test.csv")

        # TODO: Call output_csv() to write the detailed_data to a CSV file.
        output_csv(self.detailed_data, out_path)
        # TODO: Read the CSV back in and store rows in a list.
        rows = []
        with open(out_path, "r", encoding="utf-8-sig") as f:
            reader = csv.reader(f)
            next(reader)  # skip header
            for row in reader:
                rows.append(row)
        # TODO: Check that the first data row matches ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"].
        expected_first_row = ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"]
        self.assertEqual(rows[0], expected_first_row)

        os.remove(out_path)
        #pass

    def test_avg_location_rating_by_room_type(self):
        # TODO: Call avg_location_rating_by_room_type() and save the output.
        avg_ratings = avg_location_rating_by_room_type(self.detailed_data)
        # TODO: Check that the average for "Private Room" is 4.9.
        self.assertEqual(avg_ratings.get("Private Room"), 4.9)
       # pass

    def test_validate_policy_numbers(self):
        # TODO: Call validate_policy_numbers() on detailed_data and save the result into a variable invalid_listings.
        invalid_listings = validate_policy_numbers(self.detailed_data)
        # TODO: Check that the list contains exactly "16204265" for this dataset.
        self.assertEqual(invalid_listings, ["16204265"])
      #  pass


def main():
    detailed_data = create_listing_database(os.path.join("html_files", "search_results.html"))
    output_csv(detailed_data, "airbnb_dataset.csv")

if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)