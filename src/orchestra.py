import os
from crewai import Agent, Task, Crew, Process
from crewai_tools import WebsiteSearchTool, ScrapeWebsiteTool
from langchain.agents import Tool
from langchain.tools import ShellTool
from textwrap import dedent
from langchain_openai import ChatOpenAI

import llms, agents, tasks

class SdlcCrew:
  def __init__(self, urls):
    self.urls = urls
  def run(self):
    llm_web = llms.openai_35_turbo_web
    llm_local = llms.codegemma

    sdlcCrew1 = Crew(
      agents=[agents.text_scraper(llm_web),
              agents.features_writer(llm_local),
              agents.test_cases_writer(llm_local),
              agents.api_request_agent(llm_local),
              agents.test_cases_implementer(llm_local)],
      tasks=[tasks.scrape_full_site_data(urls, llm_web),
             tasks.clean_text(llm_local),
             tasks.generate_features_task(llm_local),
             tasks.write_test_cases_task(llm_local),
             tasks.implement_test_cases_task(llm_local),
             tasks.api_request_task(llm_local)],
      verbose=2, # You can set it to 1 or 2 to different logging levels
    )

    sdlcCrew2 = Crew(
        agents=[agents.api_test_agent(llm_local)],
        tasks=[tasks.api_request_task_exact(llm_local)],
        verbose=2, # You can set it to 1 or 2 to different logging levels
    )

    sdlcCrew = sdlcCrew1

    sdlcCrew.kickoff()

if __name__ == "__main__":
  print("## Welcome to testcase writer")
  print('-------------------------------')
  urls = """http://localhost/display/MSP/Project+description,
            http://localhost/pages/viewpage.action?pageId=786443,
            http://localhost/display/MSP/Service+deployment"""

  # urls = "http://localhost/display/MSP"

  sdlc_crew = SdlcCrew(urls)
  result = sdlc_crew.run()
  print("\n\n########################")
  print("## Here is the Result")
  print("########################\n")
  print(result)