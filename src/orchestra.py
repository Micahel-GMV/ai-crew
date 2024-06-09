from datetime import datetime
from crewai import Crew

from src.agents.agent_wrapper import AgentWrapper
from src.tasks import task_provider
from src.agents import agent_provider
from src.llms import llm_provider
from src.tasks.task_wrapper import TaskWrapper
from src.utils import helper
from src.utils.helper import read_file_to_string


@staticmethod
def test_llm_dtos(llm_dto_list, llm_functional, test_name, llm_temp, iter_count):
    for llm_dto in llm_dto_list:
        start_cycle_time = datetime.now()
        if llm_temp is None:
            temp_str = "def"
        else:
            temp_str = f"{llm_temp:.1f}"
        base_path = "./out/" + test_name + "_" + llm_dto.get_name() + "_" + temp_str + "_" + helper.get_datetime_str()
        base_path = base_path.replace(":", "_")
        for iter_num in range(1, iter_count + 1):
            start_iteration_time = datetime.now()
            file_path = base_path + "_" + "{:02}".format(iter_num)
            stat_path = file_path + "_stat.txt"
            content_path = file_path + ".txt"
            print("Starting run #" + str(iter_num) + " with llm " + llm_dto.name + " at temperature " + str(llm_temp))
            print("====================================================== START ================================================================")
            crew_result = single_test(llm_dto, llm_functional, llm_temp)
            print("====================================================== FINISH ===============================================================")
            end_iteration_time = datetime.now()
            helper.write_content_file(content_path, crew_result)
            helper.write_stat(stat_path, test_name, llm_dto.get_name(), llm_temp, start_iteration_time, end_iteration_time, iter_num, iter_count)
        end_cycle_time = datetime.now()
        avg_path = (base_path + "_" + helper.get_datetime_str() + "_avg.txt").replace(":", "_")
        helper.write_avg_file(avg_path, llm_dto.get_name(), llm_temp, start_cycle_time, end_cycle_time, iter_count)

@staticmethod
def single_test(llm_dto, llm_functional, llm_temp):
    def run_sdlc_crew():
        llm_current = llm_dto.get_llm()
        if llm_temp is not None:
            llm_current.temperature = llm_temp
        sdlc_crew = SdlcCrew("")
        return sdlc_crew.run(llm_current, llm_functional)
    result = run_sdlc_crew()
    print(result)
    print("======================================================================================================================")
    return result


class SdlcCrew:
    def __init__(self, urls):
        self.urls = urls

    def run(self, llm_tested, llm_functional):
        run_time_str = str(datetime.now()).replace(":","-")
        urls = """http://localhost/display/MSP/Project+description|http://localhost/pages/viewpage.action?pageId=786443|http://localhost/display/MSP/Service+deployment"""

        testcases_schema = read_file_to_string("./in/04_test_cases_schema.txt")
        features_file_path = f"./out/_features_{run_time_str}.txt"
        testcase_file_path = f"./out/_current_testcases_{run_time_str}.txt"
        testassert_file_path = f"./out/_testassert_{run_time_str}.txt"

        llm_scraper = llm_provider.get_model_byname("openhermes:latest").get_llm()
        llm_scraper.temperature = 0.0

        llm_cleaner = llm_provider.get_model_byname("phind-codellama").get_llm()
        llm_cleaner.temperature = 0.0

        llm_featurer = llm_provider.get_model_byname("codeqwen").get_llm()
        llm_featurer.temperature = 0.0

        llm_testcaser = llm_provider.get_model_byname("codebooga").get_llm()
        llm_testcaser.temperature = 0.1

        llm_normalizer = llm_provider.get_model_byname("solar").get_llm()
        llm_normalizer.temperature = 0.0

        llm_reporter = llm_provider.get_model_byname("solar").get_llm()
        llm_reporter.temperature = 0.0

        sdlc_crew = Crew(
            agents=[
                agent_provider.text_scraper(llm_scraper),
                agent_provider.text_cleaner(llm_cleaner),
                agent_provider.features_writer(llm_featurer),
                agent_provider.test_cases_writer(llm_testcaser),
                agent_provider.test_cases_normalizer(llm_normalizer),
                agent_provider.injector(llm_functional),
                agent_provider.test_report_writer(llm_tested)
            ],
            tasks=[task_provider.scrape_pages(urls, llm_scraper),
                   task_provider.clean_text(llm_cleaner),
                   task_provider.write_features(llm_featurer),
                   task_provider.write_pass_content(features_file_path, llm_functional),
                   task_provider.write_test_cases(testcases_schema, llm_testcaser),
                   task_provider.write_pass_content(testcase_file_path, llm_functional),
                   task_provider.run_tests(llm_functional),
                   task_provider.assert_test_results(testcase_file_path, llm_functional),
                   task_provider.write_pass_content(testassert_file_path, llm_functional),
                   task_provider.inject_file(testcase_file_path, llm_functional),
                   task_provider.evaluate_testrun(llm_reporter)],
            verbose=2,
            share_crew=True
        )

        return sdlc_crew.kickoff()

if __name__ == "__main__":
    print("## Welcome to CrewAI testbed")
    print('-------------------------------')

    llm_provider = llm_provider.LlmProvider()
    llm_dto_functional = llm_provider.get_model_byname("solar")
    llm_functional = llm_dto_functional.get_llm()
    llm_functional.temperature = 0.0

    llm_dto_list = llm_provider.get_models_bymodeltype("pretrained")
    llm_dto_list = [model for model in llm_dto_list if model.is_local]

    print("pretrained local llms selected:" + str(len(llm_dto_list)))

    iteration_count = 30

    test_name = "full_run"
    llm_dto_list = [llm_provider.get_model_byname("solar")]
    test_llm_dtos(llm_dto_list, llm_functional, test_name, 0.0, iteration_count)

    print("\n\n########################")
    print("## Finish #################")
    print("########################\n")
