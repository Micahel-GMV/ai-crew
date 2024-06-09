import json
from src.utils import helper

def normalize_string(json_str):
    json_str = str(json_str)
    json_str = json_str.lower()
    json_str = json_str.replace("'", "").replace('"', "")
    json_str = json_str.replace("{", "").replace("}", "").strip()
    return json_str

def jsonstring_equal(json_str1, json_str2):
    norm_str1 = normalize_string(json_str1)
    norm_str2 = normalize_string(json_str2)
    return norm_str1 == norm_str2

def validate_test_cases_file(test_report, test_cases_file_path) -> str:
    test_cases = helper.read_file_to_string(test_cases_file_path)
    return validate_test_cases(test_report, test_cases)
def validate_test_cases(test_report, test_cases) -> str:
    test_cases = helper.extract_json(test_cases)
    test_cases = helper.remove_comments(test_cases)
    test_report = helper.extract_json(test_report)
    test_report_dict = json.loads(test_report)
    test_case_dict = json.loads(test_cases)

    test_case_array = test_case_dict["test_cases"]
    test_case_map = {test_case['testcase_id']: test_case for test_case in test_case_array}

    failed_tests = []
    for test_report in test_report_dict:
        test_case = test_case_map.get(test_report['testcase_id'])
        expected_result = {
            'http_status_code': test_case['expected_result']['http_status_code'],
            'body': test_case['expected_result']['body']
        }
        actual_result = {
            'http_status_code': test_report['http_status_code'],
            'body': test_report['body']
        }
        print(f"""id:{test_report['testcase_id']} - *************************************\n{normalize_string(expected_result['body'])}\n{normalize_string(actual_result['body'])}""")
        if (expected_result['http_status_code'] != actual_result['http_status_code']
                or not jsonstring_equal(expected_result['body'], actual_result['body'])):
            cause = {}
            if expected_result['http_status_code'] != actual_result['http_status_code']:
                cause['status_code'] = {
                    'expected': expected_result['http_status_code'],
                    'actual': actual_result['http_status_code']
                }
            if expected_result['body'] != actual_result['body']:
                cause['response_body'] = {
                    'expected': expected_result['body'],
                    'actual': actual_result['body']
                }
            failed_test = {
                'testcase_id': test_case['testcase_id'],
                'cause': cause
            }
            failed_tests.append(failed_test)

    return json.dumps(failed_tests, indent=4, ensure_ascii=False)