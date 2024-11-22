def get_entity(entity_id):
    entity = hass.states.get(entity_id)
    if entity is None:
        raise ValueError(f"Cannot find entity '{entity_id}'.")
    return entity

def execute_action(action, data):
    entity_id = data.get("entity_id", "").strip()
    if not entity_id:
        raise ValueError("Required parameter 'entity_id' is missing.")
    
    entity = get_entity(entity_id)
    attributes = {key: entity.attributes[key] for key in entity.attributes}
    state = entity.state

    if action == "set_state":
        new_state = data.get("state", "").strip()
        if not new_state:
            raise ValueError("Required parameter 'state' is missing.")
        hass.states.set(entity_id, new_state, attributes)

    elif action == "set_attributes":
        new_attributes = data.get("attributes", {})
        if not isinstance(new_attributes, dict):
            raise ValueError("Required parameter 'attributes' must be a dictionary.")
        attributes.update(new_attributes)
        hass.states.set(entity_id, state, attributes)

    elif action == "set_state_attributes":
        new_state = data.get("state", "").strip()
        new_attributes = data.get("attributes", {})
        if not new_state:
            raise ValueError("Required parameter 'state' is missing.")
        if not isinstance(new_attributes, dict):
            raise ValueError("Required parameter 'attributes' must be a dictionary.")
        attributes.update(new_attributes)
        hass.states.set(entity_id, new_state, attributes)

    elif action == "delete_attribute":
        del_attr = data.get("attribute", "").strip()
        if not del_attr:
            raise ValueError("Required parameter 'attribute' is missing.")
        attributes.pop(del_attr, None)
        hass.states.set(entity_id, state, attributes)

    else:
        raise ValueError(f"Invalid action '{action}'. Expected: 'set_state', 'set_attributes', 'set_state_attributes', 'delete_attribute'.")

try:
    action = data.get("action", "").lower()
    if not action:
        raise ValueError("Required parameter 'action' is missing.")
    execute_action(action, data)
except Exception as e:
    hass.services.call(
        "persistent_notification",
        "create",
        {
            "notification_id": "Entity Wizard Error",
            "title": "Entity Wizard Error",
            "message": f"**Error log:** {e}",
        },
        False,
    )
