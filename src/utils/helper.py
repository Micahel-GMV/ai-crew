import datetime
def get_datetime_str(dt=None, fmt='%y%m%d%H%M%S'):
    if dt is None:
        dt = datetime.datetime.now()
    return dt.strftime('%y%m%d%H%M%S')

def write_stat_file(file_path, temperature, elapsed_time):
    content = "temperature: " + str(temperature) + "\nelapsed time: " + str(elapsed_time)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def write_avg_file(file_path, temperature, elapsed_time, iteration_count):
    content = ("temperature: " + str(temperature) + "\nelapsed time: " + str(elapsed_time)
               + "\naverage time per iteration:" + str(elapsed_time / iteration_count) + "\niteration count:" + str(iteration_count))
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

def write_content_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)
