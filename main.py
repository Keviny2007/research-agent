"""Main entry point for the Research Assistant Agent."""

import os
import sys
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END
from agents import (
    ResearchState,
    orchestrator,
    arxiv_agent,
    semantic_scholar_agent,
    google_scholar_agent,
    analysis_agent
)

# Load environment variables
load_dotenv()


def create_workflow():
    """Create the LangGraph workflow for the research assistant."""

    # Create the graph
    workflow = StateGraph(ResearchState)

    # Add nodes
    workflow.add_node("orchestrator", orchestrator)
    workflow.add_node("arxiv", arxiv_agent)
    workflow.add_node("semantic", semantic_scholar_agent)
    workflow.add_node("google", google_scholar_agent)
    workflow.add_node("analysis", analysis_agent)

    # Set entry point
    workflow.set_entry_point("orchestrator")

    # Parallel search: orchestrator -> all three search agents
    workflow.add_edge("orchestrator", "arxiv")
    workflow.add_edge("orchestrator", "semantic")
    workflow.add_edge("orchestrator", "google")

    # Sequential analysis: all search agents -> analysis
    workflow.add_edge("arxiv", "analysis")
    workflow.add_edge("semantic", "analysis")
    workflow.add_edge("google", "analysis")

    # End after analysis
    workflow.add_edge("analysis", END)

    return workflow.compile()


def run_research_query(query: str):
    """
    Run a research query through the multi-agent system.

    Args:
        query: The research query to search for

    Returns:
        The final report from the analysis agent
    """
    print("=" * 80)
    print(f"🚀 Starting Research Assistant")
    print("=" * 80)

    # Create and run the workflow
    app = create_workflow()

    # Initial state
    initial_state = {
        "query": query,
        "arxiv_results": [],
        "semantic_results": [],
        "google_results": [],
        "all_results": [],
        "report": ""
    }

    # Run the workflow
    result = app.invoke(initial_state)

    print("\n" + "=" * 80)
    print("✅ Research Complete!")
    print("=" * 80)

    return result


def main():
    """Main function to run research queries."""

    # Check for Google API key
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found!")
        print("Please create a .env file with your Google AI Studio API key:")
        print("  GOOGLE_API_KEY=your-api-key-here")
        print("\nGet your free API key at: https://aistudio.google.com/app/apikey")
        print("See .env.example for template")
        return

    # Check if query provided as command line argument
    if len(sys.argv) > 1:
        # Use command line argument as query
        query = " ".join(sys.argv[1:])
        queries = [query]
    else:
        # Interactive mode - prompt user for query
        print("\n" + "=" * 80)
        print("🔬 Research Assistant Agent")
        print("=" * 80)
        print("\nWelcome! I can help you find and summarize academic papers.")
        print("\nExample queries:")
        print("  • vision language models for robotics")
        print("  • autonomous navigation multimodal")
        print("  • exoplanet classification machine learning")
        print("  • quantum computing error correction")
        print("\n" + "=" * 80)

        query = input("\n🔍 Enter your research query: ").strip()

        if not query:
            print("\n❌ No query provided. Exiting...")
            return

        queries = [query]

    for query in queries:
        result = run_research_query(query)

        print("\n" + "=" * 80)
        print("📄 FINAL REPORT")
        print("=" * 80)
        print(result["report"])
        print("\n")

        # Save the report
        filename = f"examples/report_{query.replace(' ', '_')[:30]}.md"
        os.makedirs("examples", exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# Research Report: {query}\n\n")
            f.write(result["report"])
        print(f"💾 Report saved to: {filename}\n")


if __name__ == "__main__":
    main()
