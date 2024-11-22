# Entity-Wizard
Services to replace entity's states and attributes with anything you want.

# Services Schemas
### Replace State
```
action: python_script.entity_wizard
metadata: {}
data:
    action: set_state
    entity_id: person.mine
    state: home
```
### Replace Attribute
```
action: python_script.entity_wizard
metadata: {}
data:
    action: set_attributes
    entity_id: media_player.salon_tv
    attributes:
        volume_level: 0.5
```
### Replace State & Attribute
```
action: python_script.entity_wizard
metadata: {}
data:
  action: set_state_attributes
  entity_id: light.salon_lambasi
  state: 'on'
  attributes:
    color_name: red
```
### Delete Attribute
```    
action: python_script.entity_wizard
metadata: {}
data:
  action: delete_attribute
  entity_id: light.salon_lambasi
  attribute: color_temp
```
