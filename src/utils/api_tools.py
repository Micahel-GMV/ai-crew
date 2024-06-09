import json
import requests
from src.utils import helper

def read_test_cases(file_path):
    with open(file_path, 'r') as file:
        test_cases = json.load(file)
    return test_cases['test_cases']

def make_api_call(test_case):
    print(f"Running test case:\n{str(test_case)}")
    method = test_case.get('http_method')
    url = test_case.get('action').get('url')
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    headers = {
        'Content-Type': 'application/json'
    }

    print(f"Making {method} request to URL: {url}")
    # TODO: handle the service is down
    response = None
    if method == 'GET':
        response = requests.get(url, headers=headers)
    elif method == 'POST':
        response = requests.post(url, headers=headers, json=test_case.get('action').get('parameters'))
    elif method == 'PUT':
        response = requests.put(url, headers=headers, json=test_case.get('action').get('parameters'))
    elif method == 'DELETE':
        response = requests.delete(url, headers=headers)
    else:
        return {'error': f'Unsupported HTTP method: {method}'}

    return {
        'testcase_id': test_case.get('testcase_id'),
        'http_status_code': response.status_code,
        'body': response.text
    }

def run_test_cases_file(file_path) -> str:
    test_cases: json
    with open(file_path, 'r') as file:
        test_cases = json.load(file)
    return run_test_cases(test_cases['test_cases'])

def run_test_cases_string(test_cases_jsonstring: str) -> str:
    test_cases_jsonstring = helper.extract_json(test_cases_jsonstring)
    test_cases_jsonstring = helper.remove_comments(test_cases_jsonstring)
    test_cases = json.loads(test_cases_jsonstring)
    return run_test_cases(test_cases['test_cases'])

def run_test_cases_strings(str1: str, str2: str) -> str:
    if str1 and str2:
        raise ValueError("Both strings cannot be non-null")
    if not str1 and not str2:
        raise ValueError("Both strings cannot be null")
    if str1:
        return run_test_cases_string(str1)
    return run_test_cases_string(str2)

def run_test_cases_description(dummy: str, test_cases_jsonstring: str) -> str:
    return run_test_cases_string(test_cases_jsonstring)

def run_test_cases(test_cases: list) -> str:
    results = []

    for test_case in test_cases:
        result = make_api_call(test_case)
        results.append(result)

    return json.dumps(results, indent=4, ensure_ascii=False)

