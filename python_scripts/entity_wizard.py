import homeassistant.helpers.config_validation as cv
import voluptuous as vol

DOMAIN = 'entity_wizard'

# Servis tanımları için şema
SET_STATE_SCHEMA = vol.Schema({
    vol.Required('entity_id'): cv.entity_id,
    vol.Required('state'): cv.string,
})

SET_ATTRIBUTES_SCHEMA = vol.Schema({
    vol.Required('entity_id'): cv.entity_id,
    vol.Required('attributes'): dict,
})

SET_STATE_ATTRIBUTES_SCHEMA = vol.Schema({
    vol.Required('entity_id'): cv.entity_id,
    vol.Required('state'): cv.string,
    vol.Required('attributes'): dict,
})

DELETE_ATTRIBUTE_SCHEMA = vol.Schema({
    vol.Required('entity_id'): cv.entity_id,
    vol.Required('attribute'): cv.string,
})


def get_entity(entity_id):
    """Varlığı alır."""
    entity = hass.states.get(entity_id)
    if entity is None:
        raise ValueError(f"Varlık '{entity_id}' bulunamadı.")
    return entity

def execute_action(action, data):
    """Belirtilen eylemi gerçekleştirir."""
    entity_id = data.get("entity_id", "").strip()
    if not entity_id:
        raise ValueError("Gerekli parametre 'entity_id' eksik.")
    
    entity = get_entity(entity_id)
    attributes = {key: entity.attributes[key] for key in entity.attributes}
    state = entity.state

    if action == "set_state":
        new_state = data.get("state", "").strip()
        if not new_state:
            raise ValueError("Gerekli parametre 'state' eksik.")
        hass.states.set(entity_id, new_state, attributes)

    elif action == "set_attributes":
        new_attributes = data.get("attributes", {})
        if not isinstance(new_attributes, dict):
            raise ValueError("Gerekli parametre 'attributes' bir sözlük olmalıdır.")
        attributes.update(new_attributes)
        hass.states.set(entity_id, state, attributes)

    elif action == "set_state_attributes":
        new_state = data.get("state", "").strip()
        new_attributes = data.get("attributes", {})
        if not new_state:
            raise ValueError("Gerekli parametre 'state' eksik.")
        if not isinstance(new_attributes, dict):
            raise ValueError("Gerekli parametre 'attributes' bir sözlük olmalıdır.")
        attributes.update(new_attributes)
        hass.states.set(entity_id, new_state, attributes)

    elif action == "delete_attribute":
        del_attr = data.get("attribute", "").strip()
        if not del_attr:
            raise ValueError("Gerekli parametre 'attribute' eksik.")
        attributes.pop(del_attr, None)
        hass.states.set(entity_id, state, attributes)

    else:
        raise ValueError(f"Geçersiz eylem '{action}'. Beklenen: 'set_state', 'set_attributes', 'set_state_attributes', 'delete_attribute'.")


async def async_setup(hass, config):
    """Entity Wizard bileşenini kurar."""

    async def handle_set_state(call):
        """set_state servisi için çağrı işleyicisi."""
        await hass.async_add_executor_job(
            execute_action, "set_state", call.data
        )

    async def handle_set_attributes(call):
        """set_attributes servisi için çağrı işleyicisi."""
        await hass.async_add_executor_job(
            execute_action, "set_attributes", call.data
        )

    async def handle_set_state_attributes(call):
        """set_state_attributes servisi için çağrı işleyicisi."""
        await hass.async_add_executor_job(
            execute_action, "set_state_attributes", call.data
        )

    async def handle_delete_attribute(call):
        """delete_attribute servisi için çağrı işleyicisi."""
        await hass.async_add_executor_job(
            execute_action, "delete_attribute", call.data
        )

    # Servisleri kaydet
    hass.services.async_register(
        DOMAIN, 'set_state', handle_set_state, schema=SET_STATE_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, 'set_attributes', handle_set_attributes, schema=SET_ATTRIBUTES_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, 'set_state_attributes', handle_set_state_attributes, schema=SET_STATE_ATTRIBUTES_SCHEMA
    )
    hass.services.async_register(
        DOMAIN, 'delete_attribute', handle_delete_attribute, schema=DELETE_ATTRIBUTE_SCHEMA
    )

    return True
