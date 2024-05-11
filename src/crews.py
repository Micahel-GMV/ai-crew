from crewai import Crew

from src.tasks import task_provider
from src.agents import agent_provider
from src.llms import llm_man

# sdlcCrew1 = Crew(
#     agents=[agent_provider.text_scraper(llm_web),
#             agent_provider.features_writer(llm_local),
#             agent_provider.test_cases_writer(llm_local),
#             agent_provider.api_request_agent(llm_local),
#             agent_provider.test_cases_implementer(llm_local)],
#     tasks=[task_provider.scrape_full_site_data(urls, llm_web),
#            task_provider.clean_text(llm_local),
#            task_provider.generate_features_task(llm_local),
#            task_provider.write_test_cases_task(llm_local),
#            task_provider.implement_test_cases_task(llm_local),
#            task_provider.api_request_task(llm_local)],
#     verbose=2,
#     share_crew = True
# )
#
# sdlcCrew2 = Crew(
#     agents=[agent_provider.api_test_agent(llm_local)],
#     tasks=[task_provider.api_request_task_exact(llm_local)],
#     verbose=2,
#     share_crew = True
# )
#
# sdlcCrew3 = Crew(
#     agents = [agent_provider.text_scraper(llm_web),
#               agent_provider.file_writer(llm_web)],
#     tasks = [task_provider.scrape_full_site_data(urls, llm_web),
#              task_provider.file_writer_task("./out/text_scrap.txt", llm_web)],
#     verbose = 2,
#     share_crew = True
#)
