"""Semantic Scholar search tool for finding academic papers."""

import requests
from typing import List, Dict


def semantic_scholar_search(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Search Semantic Scholar for academic papers.

    Args:
        query: Search query string
        max_results: Maximum number of results to return

    Returns:
        List of paper dictionaries with title, authors, abstract, url, published date
    """
    try:
        url = "https://api.semanticscholar.org/graph/v1/paper/search"
        params = {
            "query": query,
            "limit": max_results,
            "fields": "title,authors,abstract,url,year,publicationDate"
        }

        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        results = []

        for paper in data.get("data", []):
            # Extract author names
            authors = paper.get("authors", [])
            author_names = ", ".join([author.get("name", "Unknown") for author in authors])

            results.append({
                "title": paper.get("title", "No title"),
                "authors": author_names if author_names else "Unknown",
                "abstract": paper.get("abstract", "No abstract available"),
                "url": paper.get("url", ""),
                "published": paper.get("publicationDate", paper.get("year", "Unknown")),
                "source": "Semantic Scholar"
            })

        return results

    except Exception as e:
        print(f"Error searching Semantic Scholar: {e}")
        return []


if __name__ == "__main__":
    # Test the function
    results = semantic_scholar_search("vision language models robotics", max_results=3)
    for i, paper in enumerate(results, 1):
        print(f"\n{i}. {paper['title']}")
        print(f"   Authors: {paper['authors']}")
        print(f"   URL: {paper['url']}")
