"""Search agents for different academic paper sources."""

import os
from tools import arxiv_search, semantic_scholar_search
from .state import ResearchState


def arxiv_agent(state: ResearchState) -> ResearchState:
    """Search arXiv for papers."""
    print(f"\n🔍 Searching arXiv for: {state['query']}")

    results = arxiv_search(state["query"], max_results=5)
    print(f"   Found {len(results)} papers on arXiv")

    return {
        "arxiv_results": results,
        "all_results": results
    }


def semantic_scholar_agent(state: ResearchState) -> ResearchState:
    """Search Semantic Scholar for papers."""
    print(f"\n🔍 Searching Semantic Scholar for: {state['query']}")

    results = semantic_scholar_search(state["query"], max_results=5)
    print(f"   Found {len(results)} papers on Semantic Scholar")

    return {
        "semantic_results": results,
        "all_results": results
    }


def google_scholar_agent(state: ResearchState) -> ResearchState:
    """Search Google Scholar using Gemini's Google Search grounding."""
    print(f"\n🔍 Searching Google Scholar (via Gemini grounding) for: {state['query']}")

    # Check if Google API key is available
    if not os.getenv("GOOGLE_API_KEY"):
        print("   ⚠️  GOOGLE_API_KEY not found, skipping Google Scholar search")
        return {
            "google_results": [],
            "all_results": []
        }

    try:
        import google.generativeai as genai

        # Configure Gemini
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

        # Create model with Google Search grounding tool
        model = genai.GenerativeModel(
            "gemini-2.5-flash-lite",
            tools="google_search_retrieval"
        )

        # Search query focused on academic papers
        search_prompt = f"Find recent academic research papers about: {state['query']}. Focus on peer-reviewed papers from Google Scholar, arXiv, or academic journals."

        # Generate with grounding
        response = model.generate_content(search_prompt)

        # Extract text from response
        generated_text = response.text if hasattr(response, 'text') else ""

        # Create result entry
        results = [{
            "title": f"Google Scholar research summary: {state['query']}",
            "authors": "Various (AI-curated from Google Search)",
            "abstract": generated_text[:500] if generated_text else "Academic papers found via Google Search grounding",
            "url": "https://scholar.google.com",
            "published": "Recent",
            "source": "Google Scholar (Gemini Grounded)"
        }]

        print(f"   Found {len(results)} grounded result from Google Scholar")

        return {
            "google_results": results,
            "all_results": results
        }

    except Exception as e:
        print(f"   ⚠️  Google Scholar search error: {e}")
        print("   Continuing with arXiv and Semantic Scholar results...")
        return {
            "google_results": [],
            "all_results": []
        }
