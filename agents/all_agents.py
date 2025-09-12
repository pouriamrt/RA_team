from agno.models.openai import OpenAIChat
from agno.agent import Agent
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.crawl4ai import Crawl4aiTools
from agno.tools.youtube import YouTubeTools
from agno.tools.resend import ResendTools
from agno.tools.github import GithubTools
from agno.tools.hackernews import HackerNewsTools
from agno.db.in_memory import InMemoryDb

import os
from dotenv import load_dotenv
load_dotenv(override=True)

RESEND_API_KEY = os.getenv("RESEND_API_KEY")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME")

model = OpenAIChat(id=MODEL_NAME, api_key=OPENAI_API_KEY)
db = InMemoryDb()

# Search Agent
search_agent = Agent(
    name="InternetSearcher",
    model=model,
    db=db,
    tools=[DuckDuckGoTools(all=True)],
    add_history_to_context=True,
    num_history_runs=3,  # limit history passed to this agent
    description="Expert at finding information online.",
    instructions=[
        "Use duckduckgo_search for web queries.",
        "Cite sources with URLs in responses.",
        "Focus on recent, reliable information."
    ],
    add_datetime_to_context=True,  # adds current date/time context
    markdown=True,
    exponential_backoff=True  # retry strategy to handle rate limits
)

# Crawler Agent
crawler_agent = Agent(
    name="WebCrawler",
    model=model,
    db=db,
    tools=[Crawl4aiTools(max_length=None)],  # no content length limit
    add_history_to_context=True,
    num_history_runs=3,
    description="Extracts content from specific websites.",
    instructions=[
        "Use web_crawler to extract content from provided URLs.",
        "Summarize key points and include the source URL."
    ],
    markdown=True,
    exponential_backoff=True
)


# YouTube Agent
youtube_agent = Agent(
    name="YouTubeAnalyst",
    model=model,
    db=db,
    tools=[YouTubeTools()],
    add_history_to_context=True,
    num_history_runs=3,
    description="Analyzes YouTube videos.",
    instructions=[
        "Extract captions and metadata for provided YouTube URLs.",
        "Summarize key points and include the video URL."
    ],
    markdown=True,
    exponential_backoff=True
)


# Email Agent
email_agent = Agent(
    name="EmailAssistant",
    model=model,
    db=db,
    tools=[ResendTools(from_email=EMAIL_FROM, api_key=RESEND_API_KEY)],
    add_history_to_context=True,
    num_history_runs=3,
    description="Sends emails professionally.",
    instructions=[
        "Send professional emails based on context or user request.",
        f"Default recipient is {EMAIL_TO}, but use the recipient specified in the query if provided.",
        "Include any relevant links or references in the email.",
        "Maintain a courteous and professional tone."
    ],
    markdown=True,
    exponential_backoff=True
)

# GitHub Agent
github_agent = Agent(
    name="GitHubResearcher",
    model=model,
    db=db,
    tools=[GithubTools(access_token=GITHUB_ACCESS_TOKEN)],
    add_history_to_context=True,
    num_history_runs=3,
    description="Explores GitHub repositories and issues.",
    instructions=[
        "Search repositories or list pull requests based on the user query.",
        "Provide repository links and summarize findings."
    ],
    markdown=True,
    exponential_backoff=True,
    add_datetime_to_context=True  # include time for up-to-date queries
)

# HackerNews Agent
hackernews_agent = Agent(
    name="HackerNewsMonitor",
    model=model,
    db=db,
    tools=[HackerNewsTools()],
    add_history_to_context=True,
    num_history_runs=3,
    description="Tracks Hacker News trends.",
    instructions=[
        "Fetch top stories using get_top_hackernews_stories.",
        "Summarize the story discussions and include URLs."
    ],
    markdown=True,
    exponential_backoff=True,
    add_datetime_to_context=True
)

# General Agent
general_agent = Agent(
    name="GeneralAssistant",
    model=model,
    db=db,
    add_history_to_context=True,
    num_history_runs=5,  # give it a bit more history for broader context
    description="Handles general queries and synthesizes info from specialists.",
    instructions=[
        "Answer general questions or combine inputs from specialist agents.",
        "If specialists provide info, synthesize it into a clear answer.",
        "If a query doesn't fit other specialists, attempt to answer directly.",
        "Maintain a professional and clear tone.",
        "Make the response beautifully formatted as well."
    ],
    markdown=True,
    exponential_backoff=True
)

