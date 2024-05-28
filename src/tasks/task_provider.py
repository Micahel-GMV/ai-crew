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

def write_features(llm):
    return Task(
        description="""Analyze the text received from the text_scrapper to extract and summarize RESTful API features, 
                       including endpoints, HTTP methods, expected parameters, and deployment information as 
                       described in the Confluence documentation. The result must be formatted as JSON that can be 
                       parsed without further transformation. Similar entities must be arranged in lists. Prettify the 
                       JSON representation at the end to make it more readable.""",
        expected_output="""Structured list (e.g., JSON) of RESTful API features, including endpoint descriptions, supported HTTP methods,
                          parameters, and deployment information.""",
        agent=agent_provider.features_writer(llm),
        llm = llm
    )
# ***************************************************** **************************************************************

def write_test_cases(llm):
    return Task(
        description="""Using the provided API features and requirements, generate structured, comprehensive, 
                       and repeatable test cases. These test cases should cover a wide range of scenarios including 
                       positive, negative, edge, and corner cases.

                       Important:
                       - Strictly adhere to the provided requirements without introducing any additional restrictions or assumptions.
                       - Ensure the test cases are detailed, specifying parameters and expected results accurately.
                       - Avoid redundancy by combining similar test scenarios.
                       - Include edge cases and scenarios involving special characters and unusual inputs.
                       - Format the result as JSON that is directly usable for manual execution or automation tools.
                       - Ensure the JSON is prettified for readability and include comments as additional JSON values where necessary.""",
        expected_output="""A structured list of test cases in JSON format, each with fields for precondition, 
                           action, and expected result. The JSON should be organized to allow for easy parsing 
                           and execution. Similar test cases should be grouped together in lists, and the JSON 
                           should be formatted for readability. Edge cases and special character scenarios should 
                           be explicitly included.""",
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



