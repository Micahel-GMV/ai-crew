from crewai import Task
from langchain_openai import ChatOpenAI

from src.agents import agent_provider

# ******************************************************* Finalized agents ******************************************

def pass_urls_tothetool(urls, llm):
    return Task(
        description=f"""Just pass URLs provided in the form provided to the scrape tool and the tool will return all the 
                    needed content scraped from pages. URLs are:[{urls}]""",
        expected_output="""All the text the agent scraped from the list of pages.""",
        agent=agent_provider.text_scraper(llm),
        tools=agent_provider.text_scraper(llm).tools,
        llm=llm
    )

def clean_text(llm):
    return Task(
        description="""Analyze and refine the text received from the text_scrapper agent to clearly outline different
                    aspects of the software product being developed. The task involves structuring the information 
                    to improve readability and coherency, while preserving the original phrasing and terminology as 
                    much as possible.""",
        expected_output="""A structured and coherent text document that comprehensively presents all relevant 
                    information about the product, devoid of any extraneous technical details, with the original 
                    wording and style maintained.""",
        agent=agent_provider.text_cleaner(llm),  # Assuming `text_cleaner` is directly callable here
        llm=llm
    )

# ***************************************************** **************************************************************

def read_file(file_path, llm):
    return Task(
        description=f"""Just pass file path to the file read tool and the tool will return all the needed content read 
                        from the file. The file may be empty. Don`t add any comments or thoughts to the output. 
                        File path is:{file_path}""",
        expected_output="""Exact text the agent read from the file.""",
        agent=agent_provider.file_reader(llm),
        tools=agent_provider.file_reader(llm).tools,
        llm=llm
    )


def scrape_full_site_data(urls, llm):
    return Task(
        description=f"""Navigate through and extract all textual and associated data from all the provided links, 
            ensuring comprehensive data capture. This task involves accessing all available content across the entire 
            site, not limited to a single page or section. Don`t go out of the domain provided by URLs. Combine all the 
            information scraped from all the URLs into the single text entity dividing parts with "\n" URLs are:{urls}""",
        expected_output="""All the text the agent scraped from the website.""",
        agent=agent_provider.text_scraper(llm),
        llm=llm
    )


def generate_features_task(llm):
    return Task(
        description="""Analyze the text received from the text_scrapper to extract and summarize RESTful API features, 
                       including endpoints, HTTP methods, and expected parameters, as described in the Confluence documentation.""",
        expected_output="""Structured list (e.g., JSON) of RESTful API features, including endpoint descriptions, supported HTTP methods,
                          and parameters.""",
        agent=agent_provider.features_writer(llm),
        llm = llm
    )

def write_test_cases_task(llm):
    return Task(
        description="""Using the requirements provided, develop structured, comprehensive, and repeatable test cases that 
                       can be understood and executed manually or automated by test execution tools. Focus on creating test cases
                       that cover a full range of scenarios derived from the requirements.""",
        expected_output="""Structured list of test cases in JSON format, where each test case includes fields for 
                            precondition, action, and expected result. Each action may correspond to multiple intermediate 
                            results.""",
        agent=agent_provider.test_cases_writer(llm),
        llm = llm
    )

def implement_test_cases_task(llm):
    return Task(
        description="""Using the test cases and the service URL provided, write down JSON with API calls to test the 
                    service functionality. Each call comprises the HTTP verb, URL and request payload so these fields 
                    must be in resulting JSON.""",
        expected_output="""Structured list of API calls in JSON format, where each call includes fields for 
                            HTTP verb, URL and request payload.""",
        agent=agent_provider.test_cases_writer(llm),
        llm = llm
    )

def api_request_task(llm):
    return Task(
        description="""Retrieve the URL of the deployed service from previous agent_provider, make API requests to that URL, and 
                    return response codes and bodies for further analysis. Any response codes or body are acceptable
                    due to testing purposes so the case might be negative to test the wrong input handling.""",
        expected_output="""A JSON object containing the API requests made, along with their response codes and bodies.""",
        tools=agent_provider.api_request_agent(llm).tools,
        agent=agent_provider.api_request_agent(llm),
        llm = llm
    )

def api_request_task_exact(llm):
    return Task(                                #'http://localhost:8085/greet?name=Mike
        description="""Make an API request to ''http://localhost:8085/greet?name=Mike' using specific parameters and return the response 
                    code and body exactly as received, even in case of errors.""",
        expected_output="""A JSON object containing the exact API request made, along with the response code and body, 
                    including any errors.""",
        tools=agent_provider.api_request_agent(llm).tools,
        agent=agent_provider.api_request_agent(llm),
        llm = llm
    )

def file_writer_task(file_path, llm):
    return Task(
        description=f"""Store the received information into a single file at {file_path} and pass the input content 
                    unchanged. Don`t alter , filter or remove the input content in any way not before writing it to the 
                    file nor before passing it further by the chain.""",
        expected_output="""The output will include a single file stored at the specified location with the provided 
                    content unchanged, and the task's return will be an exact copy of the inpunt content provided.""",
        agent=agent_provider.file_writer(llm),
        tools=agent_provider.file_writer(llm).tools,
        llm=llm,
        file_path=file_path
    )


