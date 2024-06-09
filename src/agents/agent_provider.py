from crewai import Agent
from crewai_tools import FileReadTool

from src.tools import api_request_tool, file_write_tool, scrape_pages_tool
from src.agents.agent_wrapper import AgentWrapper
from src.tasks.task_wrapper import TaskWrapper

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
        memory = False,
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
        memory=False,
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

def test_cases_normalizer(llm):
    return Agent(
        role='API Test Cases Normalizer',
        goal="""Transform incoming JSONs into a format that matches the given JSON schema, ensuring that all relevant 
            information is retained and correctly structured. The agent should validate the JSON against the schema, 
            make necessary adjustments to comply with the schema, and produce output that meets the defined standards
            and preserves all the information comprised in the given JSON.""",
        backstory="""With extensive experience as a QA Engineer at a leading software development company, you have a 
            proven track record of ensuring the quality and robustness of API services. Your expertise lies in 
            meticulously analyzing API documentation and translating it into well-structured, comprehensive test cases. 
            You are skilled at identifying edge cases and ensuring thorough coverage, adhering strictly to 
            specifications without making assumptions. Your background includes working with various teams to ensure the 
            highest standards of software quality.""",
        verbose=True,
        memory = True,
        allow_delegation=False,
        llm = llm
    )

def injector(llm):
    return AgentWrapper(
        role="",
        goal="",
        backstory="",
        memory = False,
        verbose = True,
        allow_delegation = False,
        llm = llm
    )
# ***************************************************** **************************************************************

def test_report_writer(llm):
    return Agent(
        role='Senior Test Case Engineer',
        goal="""Analyze the test run comparison to test cases output and give feedback on each test case.""",
        backstory="""With extensive experience as a QA Engineer at an outsourcing software development company, 
                     you excel at analyzing test run outputs and providing detailed feedback.""",
        verbose=True,
        memory = True,
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


