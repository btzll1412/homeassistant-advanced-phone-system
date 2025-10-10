"""Sensor platform for Advanced Phone System."""
from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the sensor platform."""
    coordinator = hass.data[DOMAIN][entry.entry_id]
    
    sensors = [
        PhoneSystemActiveCallsSensor(coordinator, entry),
        PhoneSystemTotalCallsSensor(coordinator, entry),
        PhoneSystemGroupsSensor(coordinator, entry),
        PhoneSystemBroadcastsSensor(coordinator, entry),
    ]
    
    async_add_entities(sensors)

class PhoneSystemActiveCallsSensor(CoordinatorEntity, SensorEntity):
    """Sensor for active calls."""

    def __init__(self, coordinator, entry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "Phone System Active Calls"
        self._attr_unique_id = f"{entry.entry_id}_active_calls"
        self._attr_icon = "mdi:phone-in-talk"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return len(self.coordinator.data.get("active_calls", []))

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        calls = self.coordinator.data.get("active_calls", [])
        return {
            "calls": [
                {
                    "call_id": call.get("call_id"),
                    "phone_number": call.get("phone_number"),
                    "status": call.get("status"),
                    "duration": call.get("duration"),
                }
                for call in calls
            ]
        }

class PhoneSystemTotalCallsSensor(CoordinatorEntity, SensorEntity):
    """Sensor for total calls today."""

    def __init__(self, coordinator, entry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "Phone System Total Calls"
        self._attr_unique_id = f"{entry.entry_id}_total_calls"
        self._attr_icon = "mdi:phone-log"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return len(self.coordinator.data.get("call_history", []))

class PhoneSystemGroupsSensor(CoordinatorEntity, SensorEntity):
    """Sensor for contact groups."""

    def __init__(self, coordinator, entry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "Phone System Groups"
        self._attr_unique_id = f"{entry.entry_id}_groups"
        self._attr_icon = "mdi:account-group"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return len(self.coordinator.data.get("groups", []))

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        groups = self.coordinator.data.get("groups", [])
        return {
            "groups": [
                {
                    "name": group.get("name"),
                    "member_count": group.get("member_count"),
                }
                for group in groups
            ]
        }

class PhoneSystemBroadcastsSensor(CoordinatorEntity, SensorEntity):
    """Sensor for broadcasts."""

    def __init__(self, coordinator, entry):
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._attr_name = "Phone System Broadcasts"
        self._attr_unique_id = f"{entry.entry_id}_broadcasts"
        self._attr_icon = "mdi:bullhorn"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        broadcasts = self.coordinator.data.get("broadcasts", [])
        active = [b for b in broadcasts if b.get("status") == "processing"]
        return len(active)

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        broadcasts = self.coordinator.data.get("broadcasts", [])
        return {
            "total_broadcasts": len(broadcasts),
            "recent_broadcasts": [
                {
                    "name": b.get("name"),
                    "status": b.get("status"),
                    "total": b.get("total_numbers"),
                    "completed": b.get("completed"),
                }
                for b in broadcasts[:5]
            ]
        }
