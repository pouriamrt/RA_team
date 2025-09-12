from agno.team import Team
from all_agents import search_agent, crawler_agent, youtube_agent, email_agent, github_agent, hackernews_agent, general_agent, db

def initialize_team(model):
    """Initializes or re-initializes the research assistant team."""
    return Team(
        name="ResearchAssistantTeam",
        model=model,                  # The base model (same as agents) acts as the coordinator brain
        members=[
            search_agent,
            crawler_agent,
            youtube_agent,
            email_agent,
            github_agent,
            hackernews_agent,
            general_agent
        ],
        description="Coordinates a team of specialist agents to handle research tasks.",
        instructions=[
            "Analyze the user query and decide which specialist(s) should handle it.",
            "Delegate tasks based on query type:",
            "- Web searches -> InternetSearcher",
            "- Website content -> WebCrawler",
            "- YouTube videos -> YouTubeAnalyst",
            "- Emails -> EmailAssistant",
            "- GitHub queries -> GitHubResearcher",
            "- Hacker News -> HackerNewsMonitor",
            "- General or multi-step queries -> GeneralAssistant",
            "Gather all agents' findings and synthesize a coherent answer.",
            "Cite sources for any facts and maintain clarity in the final answer.",
            "Always check the conversation history (memory) for context or follow-up references.",
            "If the user asks something that was asked before, utilize remembered information instead of starting fresh.",
            "Continue delegating and researching until the query is fully answered.",
            "Avoid mentioning the function calls in the final response and make the final response beautifully formatted as well."
        ],
        db=db,
        expected_output="The user's query has been thoroughly answered with information from all relevant specialists.",
        enable_agentic_state=True,      # The coordinator retains its own context between turns
        share_member_interactions=True, # All agents see each other's outputs as context
        enable_agentic_memory=True,
        enable_user_memories=True,
        read_team_history=True,
        show_members_responses=False,   # Do not show raw individual agents' answers directly to the user
        markdown=True,
        add_member_tools_to_context=True,
        add_history_to_context=True,    # Maintain a shared history (memory) between coordinator and members
        num_history_runs=5              # Limit how much history is shared (to last 5 interactions)
    )