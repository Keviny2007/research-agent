"""Analysis agent that summarizes search results using an LLM."""

import os
from dotenv import load_dotenv
from .state import ResearchState

load_dotenv()


def get_llm_response(prompt: str) -> str:
    """Get LLM response using Google Gemini."""

    if not os.getenv("GOOGLE_API_KEY"):
        raise ValueError("GOOGLE_API_KEY not found in .env file. Please add your Google AI Studio API key.")

    try:
        import google.generativeai as genai
        print("   🤖 Using model: Google Gemini 2.5 Flash Lite")

        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        model = genai.GenerativeModel("gemini-2.5-flash-lite")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        raise Exception(f"Error calling Google Gemini API: {e}")


def analysis_agent(state: ResearchState) -> ResearchState:
    """Analyze all search results and generate a summary report."""
    print(f"\n📊 Analysis Agent processing {len(state['all_results'])} total papers...")

    all_results = state["all_results"]

    if not all_results:
        return {
            "report": "No papers found for the given query."
        }

    # Prepare paper summaries for the LLM
    papers_text = ""
    for i, paper in enumerate(all_results, 1):
        papers_text += f"\n{i}. **{paper['title']}**\n"
        papers_text += f"   - Authors: {paper['authors']}\n"
        papers_text += f"   - Source: {paper['source']}\n"
        papers_text += f"   - Published: {paper['published']}\n"
        papers_text += f"   - URL: {paper['url']}\n"
        papers_text += f"   - Abstract: {paper['abstract'][:300]}...\n"

    # Create prompt for the LLM
    prompt = f"""You are a research assistant that helps summarize academic papers.
Given a list of papers, create a clear, well-organized summary report that includes:

1. Overview: A brief summary of the research area and common themes
2. Key Papers: Highlight 3-5 most relevant papers with their main contributions
3. Research Trends: What patterns or trends do you see in this research?
4. Recommendations: Which papers would be most valuable to read first?

Be concise but informative. Use bullet points and clear sections.

Query: {state["query"]}

Papers found:
{papers_text}

Please create a comprehensive research summary report."""

    # Generate the report using LLM
    try:
        report = get_llm_response(prompt)
        print("   ✅ Report generated successfully")

        return {"report": report}

    except Exception as e:
        print(f"   ❌ Error generating report: {e}")
        # Fallback to simple summary without LLM
        report = f"# Research Summary for: {state['query']}\n\n"
        report += f"Found {len(all_results)} papers across multiple sources.\n\n"

        for source in ["arXiv", "Semantic Scholar", "Google Scholar"]:
            source_papers = [p for p in all_results if p['source'] == source]
            report += f"\n## {source} ({len(source_papers)} papers)\n"
            for paper in source_papers[:3]:
                report += f"- {paper['title']}\n"
                report += f"  {paper['url']}\n"

        return {"report": report}
