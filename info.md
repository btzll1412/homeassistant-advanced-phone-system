# Advanced Phone System Integration

Integration for the Advanced Phone System Home Assistant add-on with Asterisk PBX.

## Features

- 📞 Make phone calls with TTS or pre-recorded audio
- 📢 Broadcast messages to multiple contacts or groups
- 👥 Manage contact groups with names and phone numbers
- 📊 Real-time sensors for active calls, call history, groups, and broadcasts
- 🔔 Full automation support with Home Assistant
- ⚡ Hangup active calls programmatically

## Requirements

- Home Assistant Add-on: **Advanced Phone System** must be installed and running
- The add-on must be accessible on port 8088

## Installation

### Via HACS (Recommended)

1. Open HACS
2. Go to "Integrations"
3. Click the three dots in the top right
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/btzll1412/homeassistant-advanced-phone-system`
6. Category: Integration
7. Click "Add"
8. Find "Advanced Phone System" in HACS and click "Download"
9. Restart Home Assistant

### Manual Installation

1. Download the `custom_components/advanced_phone_system` folder
2. Copy it to your Home Assistant `custom_components` directory
3. Restart Home Assistant

## Configuration

1. Go to **Settings** → **Devices & Services**
2. Click **"+ Add Integration"**
3. Search for **"Advanced Phone System"**
4. Enter your configuration:
   - **Host**: `homeassistant.local` (or your HA IP address)
   - **Port**: `8088` (default add-on port)
5. Click **Submit**

## Usage

### Services

#### `advanced_phone_system.call`
Make a phone call with TTS or a recording.

**Example - Call with TTS:**
```yaml
service: advanced_phone_system.call
data:
  phone_number: "+1234567890"
  tts_text: "The garage door has been open for 30 minutes"
  caller_id: "Home Security"

## Example - Call with Recording
service: advanced_phone_system.call
data:
  phone_number: "+1234567890"
  recording_file: "fire_alarm.wav"
  caller_id: "Fire Alert"
advanced_phone_system.broadcast
Broadcast a message to multiple numbers or a contact group.


## Example - Broadcast to Group:
service: advanced_phone_system.broadcast
data:
  name: "Family Alert"
  group_name: "Family"
  tts_text: "Dinner is ready! Please come home."
  caller_id: "Home"
Example - Broadcast to Multiple Numbers:
yamlservice: advanced_phone_system.broadcast
data:
  name: "Emergency Alert"
  phone_numbers:
    - "+1234567890"
    - "+0987654321"
  tts_text: "Emergency situation detected"
  caller_id: "Emergency System"
advanced_phone_system.hangup
Hangup an active call.
yamlservice: advanced_phone_system.hangup
data:
  call_id: "call_123456"
Sensors
The integration provides these sensors:

sensor.phone_system_active_calls - Number of currently active calls
sensor.phone_system_total_calls - Total calls made today
sensor.phone_system_groups - Number of contact groups
sensor.phone_system_broadcasts - Number of active broadcasts

Automation Examples
Alert on door open:
yamlautomation:
  - alias: "Front Door Alert"
    trigger:
      - platform: state
        entity_id: binary_sensor.front_door
        to: "on"
    action:
      - service: advanced_phone_system.call
        data:
          phone_number: "+1234567890"
          tts_text: "Alert! The front door has been opened."
          caller_id: "Security System"
Fire alarm notification to family group:
yamlautomation:
  - alias: "Fire Alarm Alert"
    trigger:
      - platform: state
        entity_id: binary_sensor.smoke_detector
        to: "on"
    action:
      - service: advanced_phone_system.broadcast
        data:
          name: "Fire Emergency"
          group_name: "Family"
          recording_file: "fire_alarm.wav"
          caller_id: "Emergency Alert"
Support
For issues and feature requests, please use the GitHub Issues page.
License
MIT License - see LICENSE file for details.
