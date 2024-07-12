from dotenv import load_dotenv
import os
from crewai import Agent, Task, Crew
from duckduckgo_search import DDGS
from langchain.tools import tool

class Ai_Logic():
    # Get OPENAI_API_KEY and OPENAI_ORGANIZATION from .env file
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")

    def start_process(self, topic):
        @tool("Internet Search Tool")
        def internet_search_tool(query: str) -> list:
            """Search Internet for relevant information based on a query."""
            ddgs = DDGS()
            results = ddgs.text(keywords=query, region='wt-wt', safesearch='moderate', max_results=3)
            return results
        # Define agents
        researcher = Agent(
            role='Researcher',
            goal='Gather and analyze information on specific topics',
            verbose=True,
            backstory=(
                "You are an expert researcher that can identify reputable websites that contain important information "
                "relating to a given specified topic. You can easily sift through information and pick out relevant  "
                "paragraphs, and accurate data."
            ),
            tools=[internet_search_tool],
            allow_delegation=True
        )

        writer = Agent(
            role='Writer',
            goal='Compose informative and engaging articles based on research findings',
            verbose=True,
            backstory=(
                "You are an expert research writer, you have the capability to write "
                "clear, concise, and  informative essays. Your articles are well-researched, "
                "accurate, accessible and easily understood by a wide-range audience."
            ),
            tools=[internet_search_tool],
            allow_delegation=False
        )

        # Define tasks
        research_task = Task(
            description=(
                f"Investigate the following: {topic}. "
                "Identify relevant information and cite the sources."
            ),
            expected_output='A detailed and easy to understand report summarizing the findings.',
            tools=[internet_search_tool],
            agent=researcher,
        )

        writing_task = Task(
            description=(
                "Based on the research findings of the topic. Create a brief outline on what it is about."
            ),
            expected_output='An accurate and informative report on the topic with citations.',
            tools=[internet_search_tool],
            agent=writer,
        )

        # Create and kick off the crew
        crew = Crew(
            agents=[researcher, writer],
            tasks=[research_task, writing_task]
        )

        result = crew.kickoff(inputs={'topic': 'Renewable Energy'})
        return result

    @property
    def api_key(self):
        return self._api_Key

    @api_key.setter
    def api_key(self, api_key):
        self._api_Key = api_key
