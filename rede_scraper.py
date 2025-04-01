import requests
from bs4 import BeautifulSoup
import re
import time
from urllib.parse import urljoin

# Base URL of the search results page
base_url = "https://www.bundespraesident.de"

# URL of the search results for speeches by Frank-Walter Steinmeier
search_url = f"{base_url}/SiteGlobals/Forms/Suche/Aktuellessuche/Aktuellessuche_Formular.html"

# Headers to mimic a browser visit
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_speech_links(search_url):
    """
    Retrieve all speech links from the search results page.
    """
    speech_links = []
    page_number = 1

    while page_number <= 100:  # Limit to 100 pages
        # Append the page number parameter for pagination
        paginated_url = f"{search_url}?pageLocale=de&gtp=220620_list%253D{page_number}&documentType_=speech&person_str=frankwaltersteinmeier"
        print(f"Retrieving page {page_number}: {paginated_url}")
        response = requests.get(paginated_url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to retrieve page {page_number + 1}. Status code: {response.status_code}")
            break

        soup = BeautifulSoup(response.content, "html.parser")

        # Find all links to speeches
        for link in soup.find_all("a", href=True):
            href = link["href"]
            print(f"Checking link: {href}")
            if "SharedDocs/Reden/DE/" in href and href not in speech_links:
                speech_links.append(href)
                print (f"Found speech link: {href}")

        page_number += 1
        time.sleep(1)  # Pause to avoid overwhelming the server

    return speech_links

def clean_text(text):
    """
    Clean and format the extracted text.
    """
    # Remove multiple newlines and excessive spaces
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def get_speech_content(speech_url):
    """
    Retrieve the content of a speech from its URL.
    """
    response = requests.get(speech_url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve speech from {speech_url}. Status code: {response.status_code}")
        return ""

    soup = BeautifulSoup(response.content, "html.parser")

    # Find the main content area
    content_div = soup.find("div", class_="column small-12 large-7")
    if not content_div:
        print(f"No content found at {speech_url}")
        return ""

    # Extract text and clean it
    paragraphs = content_div.find_all("p", recursive=False)
    speech_text = "\n".join([clean_text(p.get_text()) for p in paragraphs])
    return speech_text

def save_speeches_to_file(speech_texts, filename="Steinmeier_Speeches.txt"):
    """
    Save all speeches to a single text file.
    """
    with open(filename, "w", encoding="utf-8") as file:
        for i, speech in enumerate(speech_texts, 1):
            file.write(f"S{i}:\n")
            file.write(speech)
            file.write("\n\n" + "="*80 + "\n\n")
    print(f"All speeches have been saved to {filename}")

def main():
    print("Retrieving speech links...")
    speech_links = get_speech_links(search_url)
    print(f"Found {len(speech_links)} speeches.")

    speech_texts = []
    for idx, relative_link in enumerate(speech_links, 1):
        full_url = urljoin(base_url, relative_link)
        print(f"Retrieving speech {idx}/{len(speech_links)}: {full_url}")
        speech_content = get_speech_content(full_url)
        if speech_content:
            speech_texts.append(speech_content)
        time.sleep(1)  # Pause between requests

    save_speeches_to_file(speech_texts)

if __name__ == "__main__":
    
    main()