"""
Script to fetch and parse the 1000 most common Spanish words from Wiktionary.
This creates a Python list that can be used in seed_high_frequency_words.py
"""
import requests
from bs4 import BeautifulSoup
import re

def fetch_wiktionary_words():
    """Fetch the 1000 most common Spanish words from Wiktionary"""
    url = "https://en.wiktionary.org/wiki/Wiktionary:Frequency_lists/Spanish1000"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find the table with word frequencies
        table = soup.find('table', {'class': 'wikitable'})
        if not table:
            print("Could not find frequency table")
            return []
        
        words = []
        rows = table.find_all('tr')[1:]  # Skip header row
        
        for row in rows:
            cells = row.find_all('td')
            if len(cells) >= 2:
                rank_text = cells[0].get_text(strip=True).rstrip('.')
                word_link = cells[1].find('a')
                if word_link:
                    spanish_word = word_link.get_text(strip=True)
                    # Get English translation from the link title or next cell
                    english = "word"  # Default, will need manual translation
                    
                    try:
                        rank = int(rank_text)
                        words.append((rank, spanish_word, english))
                    except ValueError:
                        continue
        
        return words
    
    except Exception as e:
        print(f"Error fetching words: {e}")
        return []

if __name__ == "__main__":
    words = fetch_wiktionary_words()
    print(f"Fetched {len(words)} words")
    for rank, spanish, english in words[:10]:
        print(f"{rank}: {spanish} - {english}")

