from repository.PriorityRepository import get_priorities, get_priority_by_id, create_priority, update_priority, delete_priority
def get_priorities_service():
    return get_priorities()

def get_priority_by_id_service(id):
    return get_priority_by_id(id)

def create_priority_service(name, due_date_within):
    return create_priority(name, due_date_within)

def update_priority_service(id, name, due_date_within):
    return update_priority(id, name, due_date_within)

def delete_priority_service(id):
    return delete_priority(id)

