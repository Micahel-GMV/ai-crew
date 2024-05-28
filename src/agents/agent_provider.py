from crewai import Agent
from crewai_tools import FileReadTool

from src.tools import api_request_tool, file_write_tool, scrape_pages_tool

scrape_tool = scrape_pages_tool.ScrapePagesTool()
request_tool = api_request_tool.ApiRequestTool()
read_tool = FileReadTool()
write_tool = file_write_tool.FileWriteTool()

# ******************************************************* Finalized agents ******************************************
def text_scraper(llm):
    return Agent(
        role='Full Site Content Scraper',
        goal="""Surf the all the provided URLs and extract all available text and data without discrimination. This 
            includes text from all reachable pages under the specified domain, ensuring comprehensive data capture. 
            Don`t change the scrapped text in any way.""",
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

#

def text_cleaner(llm):
    return Agent(
        role='Senior Technical Writer',
        goal="""Efficiently clean raw project documentation text, removing all extraneous technical elements like 
                button labels, navigation links, and non-essential headers. Ensure that the core message and wording 
                of the essential content are preserved, avoiding unnecessary rephrasing or rewording.""",
        backstory="""In your role at a software development outsourcing company, you specialize in refining and 
                    structuring raw text to highlight clear, informative content about software products, ensuring 
                    high-quality documentation. Your task is to extract the essence without altering the original 
                    text's intent or style.""",
        verbose=True,
        memory=True,
        allow_delegation=False,
        llm=llm
    )

def file_reader(llm):
    return Agent(
        role="File Reader",
        goal="""Read the content from a file and pass the content further unchanged without adding any text, comments or 
                thoughts. Don`t change the content read from the file in any way.""",
        backstory="""This agent reads content from a specified file and passes the content unchanged.""",
        tools = [read_tool],
        memory = True,
        verbose = True,
        allow_delegation = False,
        llm = llm
    )

def features_writer(llm):
    return Agent(
        role='Senior Business Analyst',
        goal="""Analyze the provided text from project documentation. Accurately summarize all the RESTful API features, 
                ensuring only to include features explicitly described in the Confluence documentation. Prepare a detailed
                list of these features for the test_writer agent.""",
        backstory="""In an outsourcing software development company, your role involves dissecting complex product documentation 
                     to identify and clearly define RESTful service features. Your analytical skills ensure that only precise 
                     and explicitly mentioned features are captured.""",
        verbose=True,
        memory = True,
        allow_delegation=False,
        llm = llm
    )

# ***************************************************** **************************************************************

def test_cases_writer(llm):
    return Agent(
        role='API Test Case Engineer',
        goal="""Develop detailed and comprehensive test cases for API services, strictly based on provided requirements, 
             without assumptions. These test cases must cover a wide range of scenarios including positive, negative, 
             edge, and corner cases.""",
        backstory="""With extensive experience as a QA Engineer at an outsourcing software development company, 
                     you excel at converting detailed API requirements into well-structured, thorough test cases 
                     that ensure robust testing across various scenarios. You are meticulous about adhering to given 
                     specifications and avoiding any assumptions that are not explicitly stated in the requirements. 
                     Your expertise includes considering edge cases and unusual scenarios to ensure thorough coverage.""",
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

def api_test_agent(llm): # TODO: implement handling the situation when service connection is impossible - e.g. service is not running
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

def file_writer(llm):
    return Agent(
        role="File Writer",
        goal="""Write the specified content to a file and pass the content further unchanged. Don`t change the input 
                content in any way.""",
        backstory="""This agent writes results to a single file between steps in a task chain and passes the input 
                    content unchanged.""",
        tools = [write_tool],
        memory = True,
        verbose = True,
        allow_delegation = False,
        llm = llm
    )
