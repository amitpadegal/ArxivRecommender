import requests
import xml.etree.ElementTree as ET

def fetch_arxiv_papers(category="cs.LG", max_results=5):
    url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": f"cat:{category}",
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }

    response = requests.get(url, params=params)
    if response.status_code != 200:
        raise Exception("API request failed")

    root = ET.fromstring(response.text)
    ns = {'atom': 'http://www.w3.org/2005/Atom'}

    papers = []
    for entry in root.findall('atom:entry', ns):
        paper = {
            "title": entry.find('atom:title', ns).text.strip(),
            "summary": entry.find('atom:summary', ns).text.strip(),
            "authors": [author.find('atom:name', ns).text for author in entry.findall('atom:author', ns)],
            "published": entry.find('atom:published', ns).text,
            "url": entry.find('atom:id', ns).text
        }
        papers.append(paper)

    return papers

# # Example usage:
# papers = fetch_arxiv_papers("cs.LG", max_results=3)
# for p in papers:
#     print(p["title"], "-", p["url"])
