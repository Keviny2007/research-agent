"""arXiv search tool for finding academic papers."""

import arxiv
from typing import List, Dict


def arxiv_search(query: str, max_results: int = 5) -> List[Dict[str, str]]:
    """
    Search arXiv for academic papers.

    Args:
        query: Search query string
        max_results: Maximum number of results to return

    Returns:
        List of paper dictionaries with title, authors, abstract, url, published date
    """
    try:
        search = arxiv.Search(
            query=query,
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance
        )

        results = []
        for paper in search.results():
            results.append({
                "title": paper.title,
                "authors": ", ".join([author.name for author in paper.authors]),
                "abstract": paper.summary,
                "url": paper.entry_id,
                "published": paper.published.strftime("%Y-%m-%d"),
                "source": "arXiv"
            })

        return results

    except Exception as e:
        print(f"Error searching arXiv: {e}")
        return []


if __name__ == "__main__":
    # Test the function
    results = arxiv_search("vision language models robotics", max_results=3)
    for i, paper in enumerate(results, 1):
        print(f"\n{i}. {paper['title']}")
        print(f"   Authors: {paper['authors']}")
        print(f"   URL: {paper['url']}")
