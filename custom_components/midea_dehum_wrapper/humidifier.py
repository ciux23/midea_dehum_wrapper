"""Humidifier platform for Midea Dehumidifier Wrapper - Selettore unificato."""
from homeassistant.components.humidifier import (
    HumidifierEntity,
    HumidifierDeviceClass,
    HumidifierEntityFeature,
)
from homeassistant.core import HomeAssistant, callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import STATE_UNAVAILABLE, STATE_OFF
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.event import async_track_state_change_event
import logging

_LOGGER = logging.getLogger(__name__)

DOMAIN = "midea_dehum_wrapper"
FAN_PREFIX = "Fan: "
SEPARATOR = "---"

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the humidifier entities."""
    climate_entity_id = entry.data.get("climate_entity")
    _LOGGER.debug("Setting up Midea Dehumidifier Wrapper with climate entity: %s", climate_entity_id)
    entity = MideaDehumWrapper(hass, climate_entity_id, entry)
    async_add_entities([entity], update_before_add=True)


class MideaDehumWrapper(HumidifierEntity):
    """Wrapper che espone un climate come deumidificatore con preset unificato (preset originali + fan mode)."""

    def __init__(self, hass: HomeAssistant, climate_entity_id: str, entry: ConfigEntry):
        self.hass = hass
        self._climate_entity_id = climate_entity_id
        self._entry = entry
        self._attr_should_poll = False
        self._attr_unique_id = f"{entry.entry_id}_dehumidifier"
        self._attr_device_class = HumidifierDeviceClass.DEHUMIDIFIER
        self._attr_icon = "mdi:dehumidifier"
        self._attr_supported_features = HumidifierEntityFeature.MODES

        # Nome
        climate_state = self.hass.states.get(climate_entity_id)
        if climate_state:
            self._attr_name = climate_state.name
        else:
            entity_name = climate_entity_id.split('.')[-1].replace('_', ' ').title()
            self._attr_name = entity_name

        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, self._climate_entity_id)},
            name=self._attr_name,
            manufacturer="Midea",
            model="Dehumidifier Wrapper",
        )

    # --- Disponibilità e stato ON/OFF ---
    @property
    def available(self) -> bool:
        state = self.hass.states.get(self._climate_entity_id)
        return state is not None and state.state != STATE_UNAVAILABLE

    @property
    def is_on(self) -> bool:
        state = self.hass.states.get(self._climate_entity_id)
        if not state:
            return False
        hvac_mode = state.attributes.get("hvac_mode") or state.state
        return hvac_mode in ["dry", "cool", "fan_only", "heat", "heat_cool", "auto"] and state.state != "off"

    # --- Umidità ---
    @property
    def target_humidity(self) -> int | None:
        state = self.hass.states.get(self._climate_entity_id)
        return state.attributes.get("humidity") if state else None

    @property
    def current_humidity(self) -> int | None:
        state = self.hass.states.get(self._climate_entity_id)
        return state.attributes.get("current_humidity") if state else None

    @property
    def min_humidity(self) -> int:
        state = self.hass.states.get(self._climate_entity_id)
        return state.attributes.get("min_humidity", 30) if state else 30

    @property
    def max_humidity(self) -> int:
        state = self.hass.states.get(self._climate_entity_id)
        return state.attributes.get("max_humidity", 80) if state else 80

    # --- MODE (preset_mode per HA) ---
    @property
    def mode(self) -> str | None:
        """Restituisce il preset attuale (originale o fan mode con prefisso)."""
        state = self.hass.states.get(self._climate_entity_id)
        if not state:
            return None

        # Priorità: preset_mode originale (se impostato e non None)
        orig_preset = state.attributes.get("preset_mode")
        if orig_preset:
            return orig_preset

        # Altrimenti fan_mode (con prefisso)
        fan_mode = state.attributes.get("fan_mode")
        if fan_mode:
            return f"{FAN_PREFIX}{fan_mode}"

        return None

    @property
    def available_modes(self) -> list[str] | None:
        """Restituisce l'elenco di tutte le modalità disponibili: preset originali, separatore, fan modes."""
        state = self.hass.states.get(self._climate_entity_id)
        if not state:
            return None

        modes = []

        # 1. Preset originali
        orig_presets = state.attributes.get("preset_modes", [])
        modes.extend(orig_presets)

        # 2. Separatore visivo (non selezionabile)
        if orig_presets:
            modes.append(SEPARATOR)

        # 3. Fan modes con prefisso
        fan_modes = state.attributes.get("fan_modes", [])
        for fan_mode in fan_modes:
            modes.append(f"{FAN_PREFIX}{fan_mode}")

        return modes if modes else None

    async def async_set_mode(self, mode: str):
        """Imposta una modalità: se è il separatore, ignora; altrimenti distingue tra fan mode e preset originale."""
        if mode == SEPARATOR:
            _LOGGER.debug("Separatore selezionato, nessuna azione")
            return

        if mode.startswith(FAN_PREFIX):
            # Modalità ventola
            fan_mode = mode[len(FAN_PREFIX):]
            _LOGGER.debug("Impostazione ventola %s su %s", fan_mode, self._climate_entity_id)
            await self.hass.services.async_call(
                "climate",
                "set_fan_mode",
                {"entity_id": self._climate_entity_id, "fan_mode": fan_mode},
                blocking=True,
                context=self._context,
            )
        else:
            # Preset originale
            _LOGGER.debug("Impostazione preset %s su %s", mode, self._climate_entity_id)
            await self.hass.services.async_call(
                "climate",
                "set_preset_mode",
                {"entity_id": self._climate_entity_id, "preset_mode": mode},
                blocking=True,
                context=self._context,
            )

        self.async_write_ha_state()

    # --- Azioni di base ---
    async def async_turn_on(self, **kwargs):
        try:
            await self.hass.services.async_call(
                "climate",
                "set_hvac_mode",
                {"entity_id": self._climate_entity_id, "hvac_mode": "dry"},
                blocking=True,
                context=self._context,
            )
        except Exception as e:
            _LOGGER.error("Impossibile impostare dry mode: %s", e)
            await self.hass.services.async_call(
                "climate",
                "turn_on",
                {"entity_id": self._climate_entity_id},
                blocking=True,
                context=self._context,
            )
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        await self.hass.services.async_call(
            "climate",
            "turn_off",
            {"entity_id": self._climate_entity_id},
            blocking=True,
            context=self._context,
        )
        self.async_write_ha_state()

    async def async_set_humidity(self, humidity: int):
        await self.hass.services.async_call(
            "climate",
            "set_humidity",
            {"entity_id": self._climate_entity_id, "humidity": humidity},
            blocking=True,
            context=self._context,
        )
        self.async_write_ha_state()

    # --- Aggiornamento automatico via eventi ---
    async def async_added_to_hass(self):
        await super().async_added_to_hass()

        @callback
        def async_state_changed(event):
            self.async_write_ha_state()

        self.async_on_remove(
            async_track_state_change_event(
                self.hass,
                [self._climate_entity_id],
                async_state_changed
            )
        )
        _LOGGER.debug("Entità humidifier unificata aggiunta, tracking %s", self._climate_entity_id)