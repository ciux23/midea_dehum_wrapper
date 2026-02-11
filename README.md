# Midea Dehumidifier Wrapper

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

Home Assistant custom integration that wraps a Midea dehumidifier climate entity into a native humidifier with unified preset and fan control.

## Features

- Exposes a `climate` entity as a `humidifier`
- Full ON/OFF and target humidity control
- **Unified mode selector**: original preset modes + fan speeds in one dropdown
- Compatible with Matter (via RiDDiX/ha-matter-hub) and Alexa
- Config flow UI - no YAML required

## Installation

### HACS (recommended)
1. Add this custom repository to HACS: https://github.com/ciux23/midea_dehum_wrapper/tree/main
2. Search for "Midea Dehumidifier Wrapper" in HACS
3. Install the integration
4. Restart Home Assistant

### Manual
1. Download the [latest release](https://github.com/ciux23/midea_dehum_wrapper/releases)
2. Copy `custom_components/midea_dehum_wrapper/` to your `config/custom_components` directory
3. Restart Home Assistant

## Configuration

1. Go to Settings → Devices & Services → Add Integration
2. Search for "Midea Dehumidifier Wrapper"
3. Select your dehumidifier climate entity

## Usage

Your dehumidifier will appear as a native `humidifier` entity with:
- ON/OFF toggle
- Target humidity slider
- Mode selector containing:
- Original preset modes (Setpoint, Continuous, Smart, ClothesDrying)
- Fan speeds (Fan: low, Fan: medium, Fan: high)

## Support

- [GitHub Issues](https://github.com/ciux23/midea_dehum_wrapper/issues)

## License

MIT

[releases-shield]: https://img.shields.io/github/v/release/ciux23/midea_dehum_wrapper.svg?style=for-the-badge
[releases]: https://github.com/ciux23/midea_dehum_wrapper/releases
[commits-shield]: https://img.shields.io/github/commit-activity/y/ciux23/midea_dehum_wrapper.svg?style=for-the-badge
[commits]: https://github.com/ciux23/midea_dehum_wrapper/commits/main
[license-shield]: https://img.shields.io/github/license/ciux23/midea_dehum_wrapper.svg?style=for-the-badge
