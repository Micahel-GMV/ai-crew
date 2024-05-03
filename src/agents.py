from crewai import Agent
from crewai_tools import WebsiteSearchTool, ScrapeWebsiteTool
from langchain.tools import ShellTool

import api_request_tool

scrape_tool = ScrapeWebsiteTool()
shell_tool = ShellTool()
request_tool = api_request_tool.ApiRequestTool()

def text_scraper(llm):
    return Agent(
        role='Full Site Content Scraper',
        goal="""Surf the entire specified site and extract all available text and data without discrimination. This includes 
            text from all reachable pages under the specified domain, ensuring comprehensive data capture.""",
        backstory="""Developed for an outsourcing software development company, this agent is engineered to perform 
            extensive data extraction from entire websites. It navigates through multiple pages, systematically collecting 
            all forms of data presented, aiming to provide a complete dataset of the site's content for exhaustive analysis 
            and archival purposes.""",
        verbose=True,
        memory = True,
        allow_delegation=False,
        tools=[scrape_tool],
        llm=llm
    )

def text_cleaner(llm):
    return Agent(
        role='Senior Technical Writer',
        goal="""Analyze the provided raw text from project documentation, and clean it from the technical text from 
                buttons, links, headers etc.""",
        backstory="""In an outsourcing software development company, your role involves dissecting raw text to gather
                    information about the product.""",
        verbose=True,
        memory = True,
        allow_delegation=False,
        llm = llm
    )
def features_writer(llm):
    return Agent(
        role='Senior Business Analyst',
        goal="""Analyze the provided text from project documentation, accurately summarize all the RESTful API features, 
                ensuring only to include features explicitly described in the Confluence documentation, and prepare a detailed
                list of these features for the test_writer agent.""",
        backstory="""In an outsourcing software development company, your role involves dissecting complex product documentation 
                     to identify and clearly define RESTful service features. Your analytical skills ensure that only precise 
                     and explicitly mentioned features are captured.""",
        verbose=True,
        memory = True,
        allow_delegation=False,
        llm = llm
    )

def test_cases_writer(llm):
    return Agent(
        role='Test Cases Writer',
        goal='Write comprehensive test cases for given requirements, including various test scenarios',
        backstory="""As an experienced QA Engineer in an outsourcing software development company, you specialize in translating
                     detailed requirements into clear, structured test cases that cover all necessary scenarios, including positive,
                     negative, and corner cases.""",
        verbose=True,
        memory = True,
        allow_delegation=False,
        llm = llm
    )

def test_cases_implementer(llm):
    return Agent(
        role='Test Cases Implementer',
        goal='Get testcases written by previous agents, the URL of the deployed service to test API endpoints.',
        backstory="""As an experienced QA Engineer in an outsourcing software development company, you specialize in 
                    compiling provided testcases and URL of the deployed service in completed list of URLS to test 
                    endpoint and additional information like request body and HTTP verb to perform the API call.""",
        verbose=True,
        memory = True,
        allow_delegation=False,
        llm = llm
    )
def api_request_agent(llm):
    return Agent(
        role='API Caller',
        goal="""Make and test API calls based on previous agent outputs to evaluate service functionality.""",
        backstory="""This agent is designed to automate and validate API interactions by utilizing data provided by 
                    preceding agents in the chain, thereby enhancing integration and testing workflows.""",
        tools=[request_tool],
        memory=True,
        verbose=True,
        allow_delegation=False,
        llm = llm
    )

def api_test_agent(llm):
    return Agent(
        role='API Tester',
        goal="""Make single API call and return the exact response, including errors, to validate endpoint behavior 
            under specified conditions.""",
        backstory="""This agent is designed for testing API interactions by making exact calls with predefined 
                parameters and capturing all aspects of the response for analysis.""",
        tools=[request_tool],
        memory=True,
        verbose=True,
        allow_delegation=False,
        llm = llm
    )