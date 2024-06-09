from crewai import Task

from src.agents import agent_provider
from src.utils import api_tools, test_cases_tools, helper
from src.tasks.task_wrapper import TaskWrapper

# ******************************************************* Finalized agents ******************************************
def scrape_pages(urls, llm):
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
        agent=agent_provider.text_cleaner(llm),
        llm=llm
    )

def read_file(file_path, llm):
        return Task(
            description=f"""Read the content of the file located at the specified file path using the file read tool. 
                        The file may be empty. Do not add any comments or thoughts to the output. Do not try to 
                        comprehend, fix, or improve any content, including characters, special symbols, escape 
                        characters, or any potential misspellings. Simply return the exact text as read from the file.
                        File path is: {file_path}""",
            expected_output="""Exact text read from the file, with no modifications.""",
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

def write_test_cases(schema, llm):
    return Task(
        description=f"""Using the provided API features and requirements, generate structured, comprehensive, 
                       and repeatable test cases. These test cases should cover a wide range of scenarios including 
                       positive, negative, edge, and corner cases. Include the deployment information into the resulting
                       JSON as separate field.

                       Important:
                       - Strictly adhere to the provided requirements without introducing any additional restrictions or assumptions.
                       - Ensure the test cases are detailed, specifying parameters and expected results accurately.
                       - Avoid redundancy by combining similar test scenarios.
                       - Include edge cases and scenarios involving special characters and unusual inputs.
                       - Format the result as JSON that is directly usable for manual execution or automation tools.
                       - Ensure the JSON is prettified for readability and include comments as additional JSON values where necessary.
                       - Don`t use any comments that are not provided as JSON fields. Especially comment strings that are indented by "//"
                       The schema to use during the process:
                        {schema}""",
        expected_output="""A structured list of test cases in JSON format, each with fields for precondition, 
                           action, and expected result. The JSON should be organized to allow for easy parsing 
                           and execution. The JSON should adhere the JSON schema provided below. Similar test cases 
                           should be grouped together in lists, and the JSON should be formatted for readability. 
                           Edge cases and special character scenarios should be explicitly included.""",
        agent=agent_provider.test_cases_writer(llm),
        llm = llm
    )
def normalize_test_cases(schema, llm):
    return Task(
        description=f"""Transform incoming JSONs to conform to a specified JSON schema, ensuring all relevant information 
                    is preserved and structured correctly.

                    Important:
                    - Validate incoming JSONs against the provided schema and make necessary adjustments for compliance.
                    - Maintain the integrity of the original information while ensuring it matches the schema.
                    - Format the output JSON for readability, adhering to the schema's structure.
                    - Ensure the transformed JSON is usable for manual execution or automation tools.
                    - Do not attempt to improve, correct, or alter any values, including special characters, even if 
                    they appear misspelled.
                    - Secure the content - don`t reduce the number of test cases and don`t try to shorten the output in any way.
                    - Do not add any forewords or afterwords. Just formatted JSON as output.

                    The schema to use during the process:
                    {schema}
            """,
        expected_output="""A structured JSON document that conforms to the specified schema, retaining all original 
                    information while ensuring it is correctly formatted and validated. The output should be prettified 
                    for readability and ready for use in various testing tools.""",
        agent=agent_provider.test_cases_writer(llm),
        llm = llm
    )
def inject_text(text, llm):
    return TaskWrapper(
        description=text,
        expected_output="",
        agent=agent_provider.injector(llm)
    )

def inject_file(file_name, llm):
    return TaskWrapper(
        description=file_name,
        expected_output="",
        agent=agent_provider.injector(llm),
        string_function=helper.add_file_to_context
    )

def run_tests(llm):
    return TaskWrapper(
        description="",
        expected_output="",
        agent=agent_provider.injector(llm),
        string_function=api_tools.run_test_cases_strings
    )

def assert_test_results(test_cases_file, llm):
    return TaskWrapper(
        description=test_cases_file,
        expected_output="",
        agent=agent_provider.injector(llm),
        string_function=test_cases_tools.validate_test_cases_file
    )

def write_pass_content(file_path, llm):
    return TaskWrapper(
        description=file_path,
        expected_output="",
        agent=agent_provider.injector(llm),
        string_function=helper.write_content_file_fortask
    )
# ***************************************************** **************************************************************

def evaluate_testrun(llm):
    return Task(
        description=f"""Receive two JSONs. In the first one test run results and test cases expected outputs are 
                    compared and the second is testcases description. Write a brief but comprehensive structured test 
                    run report.""",
        expected_output="""A structured test report based on the provided test run results comparison with test cases' expected 
                    results. Each test case should include the ID, description, expected result, actual result, 
                    and feedback on whether the test passed or failed, including any discrepancies. If a test case is 
                    described in the test cases list and not present in the comparison report, it means the response code and 
                    response body are equal to the expected result. Mention passed test cases as well.""",
        agent=agent_provider.test_report_writer(llm),
        llm=llm
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





