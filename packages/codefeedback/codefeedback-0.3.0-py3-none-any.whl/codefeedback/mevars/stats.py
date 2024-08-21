WRONG_TASK_COUNT = {}


def set_wrong_task(task_name):
    try:
        WRONG_TASK_COUNT[task_name] += 1
    except KeyError:
        WRONG_TASK_COUNT[task_name] = 1


def get_wrong_task_count(task_name):
    try:
        count = WRONG_TASK_COUNT[task_name]
    except KeyError:
        return -1
    return count
