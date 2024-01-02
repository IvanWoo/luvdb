def get_parent_locations(location):
    parents = []
    current = location.parent
    while current is not None:
        parents.insert(0, current)
        current = current.parent
    return parents


def get_location_hierarchy_ids(location):
    hierarchy_ids = []
    if location.historical and location.current_identity:
        hierarchy_ids.append(str(location.id))
        current = location.current_identity
    else:
        current = location
    while current:
        hierarchy_ids.append(str(current.id))
        current = current.parent
    return hierarchy_ids
