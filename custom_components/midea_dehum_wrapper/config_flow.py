"""Config flow for Midea Dehumidifier Wrapper."""
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.helpers import selector
import voluptuous as vol

DOMAIN = "midea_dehum_wrapper"

class MideaDehumConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Midea Dehumidifier Wrapper."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Verifica che l'entità esista
            climate_entity = user_input.get("climate_entity")
            state = self.hass.states.get(climate_entity)
            
            if not state:
                errors["climate_entity"] = "entity_not_found"
            elif state.domain != "climate":
                errors["climate_entity"] = "not_climate_entity"
            else:
                return self.async_create_entry(
                    title=f"Midea Dehumidifier ({state.name})",
                    data=user_input,
                )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("climate_entity"): selector.EntitySelector(
                    selector.EntitySelectorConfig(domain="climate"),
                ),
            }),
            errors=errors,
        )