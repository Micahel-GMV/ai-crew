import time
from crewai import Crew

from src.tasks import task_provider
from src.agents import agent_provider
from src.llms import llm_man
from src.utils import helper

@staticmethod
def test_llm_dtos(llm_dto_list, llm_functional, test_run_name, llm_temp, iteration_count):
    for llm_dto in llm_dto_list:
        start_cycle_time = time.time()
        if llm_temp is None:
            temp_str = "def"
        else:
            temp_str = f"{llm_temp:.1f}"
        base_path = "./out/" + test_run_name + "_" + llm_dto.get_name() + "_" + temp_str + "_" + helper.get_datetime_str()
        base_path = base_path.replace(":", "_")
        for run_id in range(1, iteration_count + 1):
            start_iteration_time = time.time()
            file_path = base_path + "_" + "{:02}".format(run_id)
            stat_path = file_path + "_stat.txt"
            content_path = file_path + ".txt"
            print("Starting run #" + str(run_id) + " with llm " + llm_dto.name + " at temperature " + str(llm_temp))
            print("======================================================================================================================")
            crew_result = single_test(llm_dto, llm_functional, llm_temp)
            elapsed_time = time.time() - start_iteration_time
            helper.write_content_file(content_path, crew_result)
            helper.write_stat_file(stat_path, llm_dto.get_name(), llm_temp, elapsed_time)
        elapsed_cycle_time = time.time() - start_cycle_time
        avg_path = (base_path + "_" + helper.get_datetime_str() + "_avg.txt").replace(":", "_")
        helper.write_avg_file(avg_path, llm_dto.get_name(), llm_temp, elapsed_cycle_time, iteration_count)

@staticmethod
def single_test(llm_dto, llm_functional, llm_temp):
    try:
        llm_current = llm_dto.get_llm()
        if llm_temp is not None:
            llm_current.temperature = llm_temp
        sdlc_crew = SdlcCrew(parameter)
        result = sdlc_crew.run(llm_current, llm_functional)
        print(result)
        print("======================================================================================================================")
        return result
    except Exception as e:
        print(f"an error occurred during processing {llm_dto.name}: {str(e)}")
        return str(e)

class SdlcCrew:
    def __init__(self, urls):
        self.urls = urls
    def run(self, llm_tested, llm_functional):

        # sdlcCrew = Crew(
        #     agents = [agent_provider.text_scraper(llm_functional), agent_provider.text_cleaner(llm_tested)],
        #     tasks = [task_provider.pass_urls_tothetool(urls, llm_functional), task_provider.clean_text(llm_tested)],
        #     verbose = 2,
        #     share_crew = True
        # )

        sdlcCrew = Crew(
            agents = [agent_provider.file_reader(llm_tested)],
            tasks = [task_provider.read_file(parameter, llm_tested)],
            verbose = 2,
            share_crew = True
        )

        return sdlcCrew.kickoff()

if __name__ == "__main__":
    print("## Welcome to CrewAI testbed")
    print('-------------------------------')
    # urls = """http://localhost/display/MSP/Project+description|http://localhost/pages/viewpage.action?pageId=786443|http://localhost/display/MSP/Service+deployment"""
    parameter = """./in/00_scraped_pages.txt"""

    llm_manager = llm_man.LlmMan()
    llm_dto_functional = llm_manager.get_model_byname("openhermes:latest")
    llm_functional = llm_manager.get_model_byname("openhermes:latest").get_llm()
    llm_functional.temperature = 0.0

    llm_dto_list = llm_manager.get_models_bymodeltype("pretrained")
    llm_dto_list = [model for model in llm_dto_list if model.is_local]

    print("pretrained local llms selected:" + str(len(llm_dto_list)))

    # HARDCODE PART ***********************************************************************************************
    # llm_dto_list = [llm_manager.get_model_byname("openhermes:latest"), llm_manager.get_model_byname("solar")]
    # *************************************************************************************************************

    test_run_name = "read_file"
    iteration_count = 100

    llm_dto_list = [llm_manager.get_model_byname("mixtral")]
    print("pretrained local llms selected:" + str(len(llm_dto_list)))
    test_llm_dtos(llm_dto_list, llm_functional, test_run_name, 0.0, iteration_count)

    llm_dto_list = [llm_manager.get_model_byname("openhermes:latest")]
    print("pretrained local llms selected:" + str(len(llm_dto_list)))
    test_llm_dtos(llm_dto_list, llm_functional, test_run_name, 0.0, iteration_count)

    llm_dto_list = [llm_manager.get_model_byname("solar")]
    print("pretrained local llms selected:" + str(len(llm_dto_list)))
    test_llm_dtos(llm_dto_list, llm_functional, test_run_name, 0.0, iteration_count)

    print("\n\n########################")
    print("## Finish #################")
    print("########################\n")