# InCite

A multi-agent system that searches academic papers across multiple sources (arXiv, Semantic Scholar, and Google Scholar) in parallel and generates comprehensive research summaries using AI.

## Problem Statement

Academic literature reviews are tedious and time-consuming. Researchers must manually query multiple databases (arXiv, Semantic Scholar, Google Scholar) one at a time, each with different interfaces and search syntax. A comprehensive search easily takes 30-60 minutes of switching tabs and copy-pasting results. After gathering papers, researchers must read through abstracts individually to identify themes and determine which papers matter most.

## Solution

InCite solves this with specialized agents that search multiple databases simultaneously in parallel. Once all searches complete, an AI analysis agent generates a structured report with key papers, research trends, and reading recommendations. This turns a 30-60 minute manual process into a 3-minute automated workflow.

## Features

- **Multi-Source Search**: Searches arXiv, Semantic Scholar, and Google Scholar simultaneously
- **Parallel Processing**: All searches run in parallel for maximum efficiency
- **AI-Powered Summaries**: Uses Google Gemini to generate comprehensive research reports
- **Custom Tools**: Integrates with arXiv and Semantic Scholar APIs
- **Google Search Grounding**: Leverages Gemini's Google Search grounding for scholarly content
- **Automatic Report Generation**: Saves research summaries to markdown files
- **Simple CLI**: Easy-to-use command-line interface

## Architecture

The system uses a multi-agent architecture built with LangGraph:

```
User Query
    │
    ▼
┌───────────────┐
│ Orchestrator  │  (coordinates workflow)
└───────┬───────┘
        │
        ├─────────────┬─────────────┐
        ▼             ▼             ▼
   [arXiv]    [Semantic Scholar] [Google Scholar]
   Search         Search            Search
   (parallel agents - run simultaneously)
        │             │             │
        └─────────────┴─────────────┘
                      │
                      ▼
              ┌──────────────┐
              │  Analysis    │  (processes results)
              │  Agent       │
              └──────┬───────┘
                     │
                     ▼
              Final Report
```

### Agent Descriptions

1. **Orchestrator Agent**: Coordinates the workflow and initiates parallel searches
2. **Search Agents** (3 parallel agents):
   - **arXiv Agent**: Searches arXiv for academic papers
   - **Semantic Scholar Agent**: Searches Semantic Scholar API
   - **Google Scholar Agent**: Uses Gemini's Google Search grounding
3. **Analysis Agent**: Synthesizes all results into a comprehensive report using Google Gemini

## Prerequisites

- Python 3.8+
- Google AI Studio API key (free at [aistudio.google.com](https://aistudio.google.com/app/apikey))

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up your environment variables:
```bash
cp .env.example .env
```

3. Edit `.env` and add your Google API key:
```
GOOGLE_API_KEY=your_api_key_here
```


## Usage

### Interactive Mode

Simply run the main script:
```bash
python main.py
```

You'll be prompted to enter a research query.

### Command-Line Mode

Provide your query as a command-line argument:
```bash
python main.py "vision language models for robotics"
```

### Example Queries

- "vision language models for robotics"
- "autonomous navigation multimodal"
- "exoplanet classification machine learning"
- "quantum computing error correction"
- "JEPA for world models"

## Example Output

When you run a query, the system will:

1. Search all three sources in parallel
2. Display progress for each search
3. Generate an AI-powered summary report
4. Save the report to `examples/report_<query>.md`

Sample output:
```
================================================================================
🚀 Starting Research Assistant
================================================================================

📋 Orchestrator received query: 'vision language models for robotics'
   Coordinating parallel searches across arXiv, Semantic Scholar, and Google Scholar...

🔍 Searching arXiv for: vision language models for robotics
   Found 5 papers on arXiv

🔍 Searching Semantic Scholar for: vision language models for robotics
   Found 5 papers on Semantic Scholar

🔍 Searching Google Scholar (via Gemini grounding) for: vision language models for robotics
   Found 1 grounded result from Google Scholar

📊 Analysis Agent processing 11 total papers...
   🤖 Using model: Google Gemini 2.5 Flash Lite
   ✅ Report generated successfully

================================================================================
✅ Research Complete!
================================================================================

📄 FINAL REPORT
================================================================================
[AI-generated comprehensive summary appears here]

💾 Report saved to: examples/report_vision_language_models_for_.md
```

## Project Structure

```
research-assistant-agent/
├── README.md                    # This file
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variable template
├── .env                         # Your API keys (gitignored)
├── main.py                      # Main entry point
├── agents/
│   ├── __init__.py             # Agent exports
│   ├── state.py                # Shared state definition
│   ├── orchestrator.py         # Orchestrator agent
│   ├── search_agents.py        # All three search agents
│   └── analysis_agent.py       # Analysis and report generation
├── tools/
│   ├── __init__.py             # Tool exports
│   ├── arxiv.py                # arXiv API integration
│   └── semantic.py             # Semantic Scholar API integration
└── examples/
    └── *.md                    # Saved research reports
```

## Technologies Used

### Core Framework
- **LangGraph**: Multi-agent orchestration framework
- **LangChain**: Agent framework and utilities

### APIs & Services
- **arXiv API**: Academic paper search (free, no authentication required)
- **Semantic Scholar API**: Academic graph search (free, no authentication required)
- **Google Gemini 2.5 Flash Lite**: AI-powered analysis and Google Search grounding

### Python Libraries
- `google-generativeai`: Google Gemini API client
- `requests`: HTTP library for API calls
- `python-dotenv`: Environment variable management
- `arxiv`: Official arXiv API Python wrapper

## How It Works

1. **User enters a research query** (e.g., "quantum computing error correction")

2. **Orchestrator agent** initializes the workflow and triggers parallel searches

3. **Search agents run in parallel**:
   - arXiv agent queries the arXiv API
   - Semantic Scholar agent queries Semantic Scholar API
   - Google Scholar agent uses Gemini's grounding to search scholarly content

4. **Results are aggregated** into a shared state

5. **Analysis agent**:
   - Receives all search results
   - Generates a comprehensive summary using Google Gemini
   - Structures the report with:
     - Overview of the research area
     - Highlights of key papers
     - Research trends
     - Reading recommendations

6. **Report is displayed and saved** to the `examples/` directory

## Limitations

- Google Scholar results are AI-curated summaries rather than direct paper links
- Each source is limited to 5 papers by default (configurable in code)
- Requires internet connection for all searches
- API rate limits apply (especially for free tier services)

## Future Enhancements

Potential improvements for future versions:

- Add more academic sources (IEEE Xplore, PubMed, etc.)
- Implement result filtering by date, citation count, or relevance
- Add citation export (BibTeX, RIS)
- Create a web interface
- Add vector database for caching and similarity search
- Implement user feedback loop for refining searches