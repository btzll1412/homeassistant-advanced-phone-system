"""Data coordinator for Advanced Phone System."""
import logging
from datetime import timedelta
import aiohttp
import async_timeout

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

class PhoneSystemCoordinator(DataUpdateCoordinator):
    """Coordinator to manage fetching phone system data."""

    def __init__(self, hass: HomeAssistant, host: str, port: int):
        """Initialize coordinator."""
        self.host = host
        self.port = port
        self.base_url = f"http://{host}:{port}"
        
        super().__init__(
            hass,
            _LOGGER,
            name="Advanced Phone System",
            update_interval=timedelta(seconds=30),
        )

    async def _async_update_data(self):
        """Fetch data from API."""
        try:
            async with async_timeout.timeout(10):
                async with aiohttp.ClientSession() as session:
                    # Get active calls
                    async with session.get(f"{self.base_url}/api/calls/active") as response:
                        active_calls = await response.json()
                    
                    # Get recent call history
                    async with session.get(f"{self.base_url}/api/call_history?limit=10") as response:
                        call_history = await response.json()
                    
                    # Get groups
                    async with session.get(f"{self.base_url}/api/groups") as response:
                        groups = await response.json()
                    
                    # Get broadcasts
                    async with session.get(f"{self.base_url}/api/broadcasts") as response:
                        broadcasts = await response.json()
                    
                    return {
                        "active_calls": active_calls.get("active_calls", []),
                        "call_history": call_history.get("calls", []),
                        "groups": groups.get("groups", []),
                        "broadcasts": broadcasts.get("broadcasts", []),
                    }
        except Exception as err:
            raise UpdateFailed(f"Error communicating with API: {err}")

    async def make_call(self, phone_number, tts_text=None, recording_file=None, 
                       caller_id=None, max_retries=3, pre_message_delay=1, max_ring_time=45):
        """Make a phone call."""
        data = {
            "phone_number": phone_number,
            "max_retries": max_retries,
            "pre_message_delay": pre_message_delay,
            "max_ring_time": max_ring_time
        }
        
        if caller_id:
            data["caller_id"] = caller_id
        
        if tts_text:
            data["tts_text"] = tts_text
        elif recording_file:
            data["recording_file"] = recording_file
        else:
            _LOGGER.error("Either tts_text or recording_file must be provided")
            return None
        
        try:
            async with async_timeout.timeout(10):
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f"{self.base_url}/api/call",
                        json=data
                    ) as response:
                        if response.status == 200:
                            result = await response.json()
                            await self.async_request_refresh()
                            return result
                        else:
                            _LOGGER.error(f"Call failed: {response.status}")
                            return None
        except Exception as err:
            _LOGGER.error(f"Error making call: {err}")
            return None

    async def make_broadcast(self, name, group_name=None, phone_numbers=None,
                           tts_text=None, recording_file=None, caller_id=None,
                           concurrent_calls=5, pre_message_delay=1, max_ring_time=45):
        """Make a broadcast call."""
        data = {
            "name": name,
            "concurrent_calls": concurrent_calls,
            "pre_message_delay": pre_message_delay,
            "max_ring_time": max_ring_time
        }
        
        if caller_id:
            data["caller_id"] = caller_id
        
        if group_name:
            data["group_name"] = group_name
        elif phone_numbers:
            data["phone_numbers"] = phone_numbers
        else:
            _LOGGER.error("Either group_name or phone_numbers must be provided")
            return None
        
        if tts_text:
            data["tts_text"] = tts_text
        elif recording_file:
            data["recording_file"] = recording_file
        else:
            _LOGGER.error("Either tts_text or recording_file must be provided")
            return None
        
        try:
            async with async_timeout.timeout(10):
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f"{self.base_url}/api/broadcast",
                        json=data
                    ) as response:
                        if response.status == 200:
                            result = await response.json()
                            await self.async_request_refresh()
                            return result
                        else:
                            _LOGGER.error(f"Broadcast failed: {response.status}")
                            return None
        except Exception as err:
            _LOGGER.error(f"Error making broadcast: {err}")
            return None

    async def hangup_call(self, call_id):
        """Hangup an active call."""
        try:
            async with async_timeout.timeout(10):
                async with aiohttp.ClientSession() as session:
                    async with session.post(
                        f"{self.base_url}/api/calls/{call_id}/hangup"
                    ) as response:
                        if response.status == 200:
                            await self.async_request_refresh()
                            return True
                        else:
                            _LOGGER.error(f"Hangup failed: {response.status}")
                            return False
        except Exception as err:
            _LOGGER.error(f"Error hanging up call: {err}")
            return False
