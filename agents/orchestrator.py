"""Orchestrator agent that coordinates the search workflow."""

from .state import ResearchState


def orchestrator(state: ResearchState) -> ResearchState:
    """
    Orchestrator agent that receives the query and prepares state.
    The actual coordination happens via the graph structure.
    """
    print(f"\n📋 Orchestrator received query: '{state['query']}'")
    print("   Coordinating parallel searches across arXiv, Semantic Scholar, and Google Scholar...")

    # Initialize empty lists if not present
    return {
        "arxiv_results": state.get("arxiv_results", []),
        "semantic_results": state.get("semantic_results", []),
        "google_results": state.get("google_results", []),
        "all_results": []
    }
