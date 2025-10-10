"""Advanced Phone System integration."""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.const import CONF_HOST, CONF_PORT

from .const import DOMAIN
from .coordinator import PhoneSystemCoordinator

_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, config: dict):
    """Set up the Advanced Phone System component."""
    hass.data.setdefault(DOMAIN, {})
    return True

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Set up Advanced Phone System from a config entry."""
    host = entry.data[CONF_HOST]
    port = entry.data[CONF_PORT]
    
    coordinator = PhoneSystemCoordinator(hass, host, port)
    await coordinator.async_config_entry_first_refresh()
    
    hass.data[DOMAIN][entry.entry_id] = coordinator
    
    # Register services
    await async_setup_services(hass, coordinator)
    
    # Forward to sensor platform
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])
    
    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, ["sensor"])
    
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    
    return unload_ok

async def async_setup_services(hass: HomeAssistant, coordinator):
    """Set up services for the phone system."""
    
    async def handle_call(call):
        """Handle the call service."""
        phone_number = call.data.get("phone_number")
        tts_text = call.data.get("tts_text")
        recording_file = call.data.get("recording_file")
        caller_id = call.data.get("caller_id")
        max_retries = call.data.get("max_retries", 3)
        pre_message_delay = call.data.get("pre_message_delay", 1)
        max_ring_time = call.data.get("max_ring_time", 45)
        
        result = await coordinator.make_call(
            phone_number=phone_number,
            tts_text=tts_text,
            recording_file=recording_file,
            caller_id=caller_id,
            max_retries=max_retries,
            pre_message_delay=pre_message_delay,
            max_ring_time=max_ring_time
        )
        
        if result:
            _LOGGER.info(f"Call initiated successfully: {result.get('call_id')}")
        else:
            _LOGGER.error("Failed to initiate call")
    
    async def handle_broadcast(call):
        """Handle the broadcast service."""
        name = call.data.get("name")
        group_name = call.data.get("group_name")
        phone_numbers = call.data.get("phone_numbers")
        tts_text = call.data.get("tts_text")
        recording_file = call.data.get("recording_file")
        caller_id = call.data.get("caller_id")
        concurrent_calls = call.data.get("concurrent_calls", 5)
        pre_message_delay = call.data.get("pre_message_delay", 1)
        max_ring_time = call.data.get("max_ring_time", 45)
        
        result = await coordinator.make_broadcast(
            name=name,
            group_name=group_name,
            phone_numbers=phone_numbers,
            tts_text=tts_text,
            recording_file=recording_file,
            caller_id=caller_id,
            concurrent_calls=concurrent_calls,
            pre_message_delay=pre_message_delay,
            max_ring_time=max_ring_time
        )
        
        if result:
            _LOGGER.info(f"Broadcast initiated successfully: {result.get('broadcast_id')}")
        else:
            _LOGGER.error("Failed to initiate broadcast")
    
    async def handle_hangup(call):
        """Handle the hangup service."""
        call_id = call.data.get("call_id")
        
        result = await coordinator.hangup_call(call_id)
        
        if result:
            _LOGGER.info(f"Call {call_id} hung up successfully")
        else:
            _LOGGER.error(f"Failed to hangup call {call_id}")
    
    # Register services
    hass.services.async_register(DOMAIN, "call", handle_call)
    hass.services.async_register(DOMAIN, "broadcast", handle_broadcast)
    hass.services.async_register(DOMAIN, "hangup", handle_hangup)
