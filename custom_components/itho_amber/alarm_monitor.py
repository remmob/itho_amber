"""Alarm monitoring for Itho Amber integration."""

import logging
from datetime import datetime, timedelta
from homeassistant.core import HomeAssistant, callback
from homeassistant.const import STATE_UNAVAILABLE, STATE_UNKNOWN
from homeassistant.components.persistent_notification import async_create as create_persistent_notification
from homeassistant.helpers.event import async_track_state_change_event

from .const import ALARM_SENSORS, DOMAIN

_LOGGER = logging.getLogger(__name__)


class AlarmMonitor:
    """Monitor alarm sensors and send notifications."""

    def __init__(self, hass: HomeAssistant, name: str, notify_alarms_mobile: bool = False, notify_alarms_persistent: bool = False, notify_services: str = "", notification_title: str = "Warmtepomp in storing!", alarm_delay: int = 60):
        """Initialize the alarm monitor."""
        self.hass = hass
        self.name = name
        self._notify_alarms_mobile = notify_alarms_mobile
        self._notify_alarms_persistent = notify_alarms_persistent
        self._notify_services = [s.strip() for s in notify_services.split(",") if s.strip()] if notify_services else []
        self._notification_title = notification_title
        self._alarm_delay = alarm_delay
        self._alarm_states = {}
        self._alarm_times = {}
        self._listeners = []

    def start_monitoring(self):
        """Start monitoring alarm sensors."""
        if not self._notify_alarms_mobile and not self._notify_alarms_persistent:
            _LOGGER.debug("Alarm notifications disabled, not starting monitor")
            return

        # Build list of entity IDs to monitor
        entity_ids = [f"sensor.{self.name}_{sensor}" for sensor in ALARM_SENSORS]
        
        # Track state changes
        self._listeners.append(
            async_track_state_change_event(
                self.hass,
                entity_ids,
                self._alarm_state_changed
            )
        )
        
        _LOGGER.info(f"Started monitoring {len(entity_ids)} alarm sensors for {self.name}")

    @callback
    def _alarm_state_changed(self, event):
        """Handle alarm sensor state changes."""
        entity_id = event.data.get("entity_id")
        old_state = event.data.get("old_state")
        new_state = event.data.get("new_state")

        if not old_state or not new_state:
            return

        # Skip if unavailable or unknown
        if new_state.state in [STATE_UNAVAILABLE, STATE_UNKNOWN]:
            return

        # Get sensor key from entity_id
        sensor_key = entity_id.replace(f"sensor.{self.name}_", "")
        
        # Check if this is a transition from "No Alarm" to "ALARM"
        if old_state.state == "No Alarm" and new_state.state == "ALARM":
            now = datetime.now()
            
            # Determine delay based on sensor type
            # S06 and S07 need minimum 5 minute delay, others use configured alarm_delay
            if sensor_key in ["s06_water_outlet_to_low_in_cooling", "s07_water_outlet_to_high_in_heating"]:
                # Ensure minimum 5 minutes for these sensors
                delay = timedelta(seconds=max(self._alarm_delay, 300))
            else:
                delay = timedelta(seconds=self._alarm_delay)
            
            # Store the alarm time
            self._alarm_times[entity_id] = now
            
            # Schedule notification check
            self.hass.loop.call_later(
                delay.total_seconds(),
                lambda: self.hass.async_create_task(
                    self._send_alarm_notification(entity_id, new_state, now)
                )
            )
            
            _LOGGER.debug(f"Alarm detected on {entity_id}, will notify after {delay}")
        
        # Clear alarm time if it goes back to "No Alarm"
        elif old_state.state == "ALARM" and new_state.state == "No Alarm":
            if entity_id in self._alarm_times:
                del self._alarm_times[entity_id]
                _LOGGER.debug(f"Alarm cleared on {entity_id}")

    async def _send_alarm_notification(self, entity_id, state, alarm_time):
        """Send notification if alarm is still active."""
        # Check if alarm is still active and hasn't been cleared
        if entity_id not in self._alarm_times or self._alarm_times[entity_id] != alarm_time:
            _LOGGER.debug(f"Alarm on {entity_id} was cleared before notification delay")
            return
        
        # Get current state
        current_state = self.hass.states.get(entity_id)
        if not current_state or current_state.state != "ALARM":
            _LOGGER.debug(f"Alarm on {entity_id} is no longer active")
            return
        
        # Send notification
        friendly_name = state.attributes.get("friendly_name", entity_id)
        title = self._notification_title
        message = f"{friendly_name} is in ALARM status"
        
        # Send persistent notification if enabled
        if self._notify_alarms_persistent:
            create_persistent_notification(
                self.hass,
                message,
                title
            )
        
        # Send mobile app notifications if configured
        if self._notify_alarms_mobile:
            for service_name in self._notify_services:
                try:
                    await self.hass.services.async_call(
                        "notify",
                        service_name,
                        {
                            "title": title,
                            "message": friendly_name,
                        },
                    )
                    _LOGGER.debug(f"Sent mobile notification to {service_name}")
                except Exception as e:
                    _LOGGER.error(f"Failed to send notification to {service_name}: {e}")
        
        _LOGGER.info(f"Sent alarm notification for {entity_id}")

    def stop_monitoring(self):
        """Stop monitoring alarm sensors."""
        for listener in self._listeners:
            listener()
        self._listeners.clear()
        _LOGGER.debug(f"Stopped alarm monitoring for {self.name}")

    def update_settings(self, notify_alarms_mobile: bool = False, notify_alarms_persistent: bool = False, notify_services: str = "", notification_title: str = "Warmtepomp in storing!", alarm_delay: int = 60):
        """Update notification settings."""
        notify_services_list = [s.strip() for s in notify_services.split(",") if s.strip()] if notify_services else []
        
        # Check if we need to start or stop monitoring
        was_enabled = self._notify_alarms_mobile or self._notify_alarms_persistent
        now_enabled = notify_alarms_mobile or notify_alarms_persistent
        
        if was_enabled != now_enabled:
            if now_enabled:
                self.start_monitoring()
            else:
                self.stop_monitoring()
        
        self._notify_alarms_mobile = notify_alarms_mobile
        self._notify_alarms_persistent = notify_alarms_persistent
        self._notify_services = notify_services_list
        self._notification_title = notification_title
        self._alarm_delay = alarm_delay
