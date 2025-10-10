"""Config flow for Advanced Phone System."""
import logging
import voluptuous as vol
import aiohttp

from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.core import callback

from .const import DOMAIN, DEFAULT_PORT

_LOGGER = logging.getLogger(__name__)

class PhoneSystemConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Advanced Phone System."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            port = user_input[CONF_PORT]
            
            # Test connection
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"http://{host}:{port}/health") as response:
                        if response.status == 200:
                            await self.async_set_unique_id(f"{host}:{port}")
                            self._abort_if_unique_id_configured()
                            
                            return self.async_create_entry(
                                title=f"Phone System ({host})",
                                data=user_input
                            )
                        else:
                            errors["base"] = "cannot_connect"
            except Exception:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required(CONF_HOST, default="homeassistant.local"): str,
                vol.Required(CONF_PORT, default=DEFAULT_PORT): int,
            }),
            errors=errors,
        )
