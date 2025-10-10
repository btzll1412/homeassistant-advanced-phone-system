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
