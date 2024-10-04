import requests
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re
from urllib.parse import urlparse, urljoin

def get_text_from_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text(separator=' ')
    text = re.sub(r'\W+', ' ', text)
    text = ' '.join(text.split())
    return text

def get_css_from_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    relevant_css_properties = []

    # Extract CSS from <style> tags
    for style in soup.find_all('style'):
        css_text = style.get_text()
        relevant_css_properties.extend(css_text.split('\n'))

    # Extract CSS from external CSS files linked using <link> tag
    for link in soup.find_all('link', rel='stylesheet'):
        css_url = link.get('href')
        if css_url:
            # Handle relative URLs
            if not bool(urlparse(css_url).netloc):
                css_url = urljoin(url, css_url)
            css_response = requests.get(css_url)
            css_text = css_response.text
            relevant_css_properties.extend(css_text.split('\n'))

    return relevant_css_properties

def calculate_cosine_similarity(tokens1, tokens2):
    vectorizer = CountVectorizer().fit_transform([tokens1, tokens2])
    cosine_sim = cosine_similarity(vectorizer)
    return cosine_sim[0, 1]

website1_url = 'http://localhost/spotify/84_Spotify_Clone/'
website2_url = 'https://open.spotify.com/'

text1 = get_text_from_website(website1_url)
text2 = get_text_from_website(website2_url)

css1 = get_css_from_website(website1_url)
css2 = get_css_from_website(website2_url)

text_similarity = calculate_cosine_similarity(text1, text2)

# Combine CSS into strings for comparison
css1_str = '\n'.join(css1)
css2_str = '\n'.join(css2)
css_similarity = calculate_cosine_similarity(css1_str, css2_str)

overall_similarity = (text_similarity + css_similarity) / 2 * 100

print("Text Similarity Score:", text_similarity)
print("CSS Similarity Score:", css_similarity)
print("\nOverall Similarity Percentage:", overall_similarity, "%")
