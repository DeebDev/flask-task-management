from repository.TaskRepository import get_tasks, get_task_by_id, create_task, update_task, delete_task, get_tasks_by_user_id, complete_task, incomplete_task, get_completed_tasks, get_incomplete_tasks

def get_tasks_service():
    return get_tasks()

def get_all_task_service():
    return get_tasks()

def get_task_by_id_service(id):
    return get_task_by_id(id)

def create_task_service(name, description, due_date, priority_id, user_id):
    return create_task(name, description, due_date, priority_id, user_id)

def update_task_service(id, name, description, due_date, priority_id, user_id):
    return update_task(id, name, description, due_date, priority_id, user_id)

def delete_task_service(id):
    return delete_task(id)

def get_tasks_by_user_id_service(user_id):
    return get_tasks_by_user_id(user_id)

def complete_task_service(id):
    return complete_task(id)

def incomplete_task_service(id):
    return incomplete_task(id)

def get_completed_tasks_service():
    return get_completed_tasks()

def get_incomplete_tasks_service():
    return get_incomplete_tasks()