"""State definition for the research assistant workflow."""

from typing import TypedDict, List, Dict, Annotated
import operator


class ResearchState(TypedDict):
    """State that gets passed between agents."""

    # Input
    query: str

    # Search results from each source
    arxiv_results: List[Dict[str, str]]
    semantic_results: List[Dict[str, str]]
    google_results: List[Dict[str, str]]

    # Combined results
    all_results: Annotated[List[Dict[str, str]], operator.add]

    # Final output
    report: str
