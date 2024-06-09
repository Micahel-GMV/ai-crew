import datetime
import psycopg2
import json

# Database connection setup
def connect_to_db():
    conn = psycopg2.connect(
        dbname="resthello",
        user="postgres",
        password="jellyfish",
        host="localhost",
        port="5432"
    )
    return conn

def report_test_run_db(test_name, llm_name, temperature, start_timestamp, end_timestamp, iter_num, iter_count):
    conn = connect_to_db()
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO test_runs (start_timestamp, end_timestamp, test_run_name, llm_name, temperature, iter_num, iter_count)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """

    cursor.execute(insert_query, (start_timestamp, end_timestamp, test_name, llm_name, temperature, iter_num, iter_count))
    conn.commit()

    cursor.close()
    conn.close()

def get_requests_between_times(start_time, end_time):
    conn = connect_to_db()
    cursor = conn.cursor()

    query = """
    SELECT * FROM incoming_requests
    WHERE timestamp >= %s AND timestamp <= %s
    """

    cursor.execute(query, (start_time, end_time))
    rows = cursor.fetchall()

    # Get column names from the cursor
    column_names = [desc[0] for desc in cursor.description]

    # Convert each row to a dictionary
    requests = [dict(zip(column_names, row)) for row in rows]

    cursor.close()
    conn.close()

    return requests

def count_requests_between_times(start_time, end_time):
    conn = connect_to_db()
    cursor = conn.cursor()

    query = """
    SELECT COUNT(*) FROM incoming_requests
    WHERE timestamp >= %s AND timestamp <= %s
    """

    cursor.execute(query, (start_time, end_time))
    requests_count = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return requests_count

def get_datetime_str(dt=None, fmt='%y%m%d%H%M%S'):
    if dt is None:
        dt = datetime.datetime.now()
    return dt.strftime('%y%m%d%H%M%S')

def write_stat(file_path, test_name, llm_name, temperature, start_time, end_time, iter_num, iter_count):
    report_test_run_db(test_name, llm_name, temperature, start_time, end_time, iter_num, iter_count)

    elapsed_time = end_time - start_time
    elapsed_seconds = elapsed_time.total_seconds()

    requests = get_requests_between_times(start_time, end_time)
    requests_count = len(requests)

    detailed_requests = [
        {
            "id": req.get("id"),
            "loglevel": req.get("loglevel"),
            "timestamp": req.get("timestamp"),
            "method": req.get("method"),
            "request_url": req.get("request_url"),
            "query_string": req.get("query_string"),
            "parameters_json": req.get("parameters_json"),
            "endpoint": req.get("endpoint"),
            "body": req.get("body"),
            "response_code": req.get("response_code"),
            "response_body": req.get("response_body")
        } for req in requests
    ]

    content = {
        "model_name": llm_name,
        "temperature": temperature,
        "start_time": start_time,
        "end_time": end_time,
        "elapsed_time": elapsed_seconds,
        "average_time_per_iteration": int(elapsed_seconds / iter_count),
        "iteration_count": iter_count,
        "requests_count": requests_count,
        "requests": detailed_requests
    }

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(content, file, indent=4, default=str)

def write_avg_file(file_path, llm_name, temperature, start_time, end_time, iter_count):
    elapsed_time = end_time - start_time
    elapsed_seconds = elapsed_time.total_seconds()
    avg_time = int(elapsed_seconds / iter_count)
    request_count = count_requests_between_times(start_time,end_time)

    content = {
        "model_name": llm_name,
        "temperature": temperature,
        "elapsed_time": elapsed_seconds,
        "request_count": request_count,
        "average_time_per_iteration": avg_time,
        "iteration_count": iter_count
    }

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(content, file, indent=4, default=str)

def write_content_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def write_content_file_fortask(content, file_path) -> str:
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
    return content

def read_file_to_string(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return None
    except IOError as e:
        print(f"An error occurred while reading the file: {e}")
        return None

def add_file_to_context(context: str, file_path: str) -> str:
    result =  context + "\n" + read_file_to_string(file_path)
    print(f"\nContext+file:{result}")
    return result

def remove_comments(json_text):
    lines = json_text.split('\n')
    cleaned_lines = [line for line in lines if not line.strip().startswith('//')]
    return '\n'.join(cleaned_lines)

def extract_json(text):
    start_index_obj = text.find('{')
    end_index_obj = text.rfind('}')

    start_index_arr = text.find('[')
    end_index_arr = text.rfind(']')

    if start_index_obj != -1 and (start_index_arr == -1 or start_index_obj < start_index_arr):
        if end_index_obj != -1:
            return text[start_index_obj:end_index_obj + 1]
    elif start_index_arr != -1:
        if end_index_arr != -1:
            return text[start_index_arr:end_index_arr + 1]

    return None