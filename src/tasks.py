from crewai import Task

import llms, agents

def scrape_full_site_data(urls, llm):
    return Task(
        description=f"""Navigate through and extract all textual and associated data from the specified site, ensuring 
            comprehensive data capture. This task involves accessing all available content across the entire site, not 
            limited to a single page or section. URLs are:[{urls}]""",
        expected_output="""A complete dataset containing all raw data from the entire site, including text, metadata, 
            and any other content, without exclusions or structural modifications. This output aims to provide a 
            thorough representation of the site's current state.""",
        agent=agents.text_scraper(llm),
        llm=llm
    )

def clean_text(llm):
    return Task(
        description="""Analyze the text received from the text_scrapper to extract information about the product being 
                    developed.""",
        expected_output="""Readable text that contains all the product-relative information.""",
        agent=agents.text_cleaner(llm),
        llm = llm
    )
def generate_features_task(llm):
    return Task(
        description="""Analyze the text received from the text_scrapper to extract and summarize RESTful API features, 
                       including endpoints, HTTP methods, and expected parameters, as described in the Confluence documentation.""",
        expected_output="""Structured list (e.g., JSON) of RESTful API features, including endpoint descriptions, supported HTTP methods,
                          and parameters.""",
        agent=agents.features_writer(llm),
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
        agent=agents.test_cases_writer(llm),
        llm = llm
    )

def implement_test_cases_task(llm):
    return Task(
        description="""Using the test cases and the service URL provided, write down JSON with API calls to test the 
                    service functionality. Each call comprises the HTTP verb, URL and request payload so these fields 
                    must be in resulting JSON.""",
        expected_output="""Structured list of API calls in JSON format, where each call includes fields for 
                            HTTP verb, URL and request payload.""",
        agent=agents.test_cases_writer(llm),
        llm = llm
    )

def api_request_task(llm):
    return Task(
        description="""Retrieve the URL of the deployed service from previous agents, make API requests to that URL, and 
                    return response codes and bodies for further analysis. Any response codes or body are acceptable
                    due to testing purposes so the case might be negative to test the wrong input handling.""",
        expected_output="""A JSON object containing the API requests made, along with their response codes and bodies.""",
        tools=agents.api_request_agent(llm).tools,
        agent=agents.api_request_agent(llm),
        llm = llm
    )

def api_request_task_exact(llm):
    return Task(                                #'http://localhost:8085/greet?name=Mike
        description="""Make an API request to ''http://localhost:8085/greet?name=Mike' using specific parameters and return the response 
                    code and body exactly as received, even in case of errors.""",
        expected_output="""A JSON object containing the exact API request made, along with the response code and body, 
                    including any errors.""",
        tools=agents.api_request_agent(llm).tools,
        agent=agents.api_request_agent(llm),
        llm = llm
    )