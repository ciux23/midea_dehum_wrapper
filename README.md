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
1. Add this repository as a custom repository in HACS
2. Search for "Midea Dehumidifier Wrapper"
3. Install

### Manual
Copy `custom_components/midea_dehum_wrapper/` to your `config/custom_components` directory.

## Configuration

1. Restart Home Assistant
2. Go to Settings → Devices & Services → Add Integration
3. Search for "Midea Dehumidifier Wrapper"
4. Select your dehumidifier climate entity

## Usage

Your dehumidifier will appear as a native `humidifier` entity with:
- ON/OFF toggle
- Target humidity slider
- Mode selector containing:
  - Original preset modes (Setpoint, Continuous, Smart, ClothesDrying)
  - Fan speeds (Fan: low, Fan: medium, Fan: high)

[releases-shield]: https://img.shields.io/github/v/release/tuo-username/midea-dehum-wrapper.svg?style=for-the-badge
[releases]: https://github.com/tuo-username/midea-dehum-wrapper/releases
[commits-shield]: https://img.shields.io/github/commit-activity/y/tuo-username/midea-dehum-wrapper.svg?style=for-the-badge
[commits]: https://github.com/tuo-username/midea-dehum-wrapper/commits/main
[license-shield]: https://img.shields.io/github/license/tuo-username/midea-dehum-wrapper.svg?style=for-the-badge
