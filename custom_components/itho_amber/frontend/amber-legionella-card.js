/**
 * Amber legionella card
 *
 * Shows the anti-legionella schedule of an Itho Amber heat pump as one line and
 * opens a dialog to change it. Nothing is written while the dialog is open: the
 * day chips and the time only change local state, and Save sends them to the
 * heat pump in a single action call.
 *
 * Deliberately free of dependencies. No card-mod, no browser_mod, no build
 * step. The dialog is our own overlay, themed with Home Assistant's own CSS
 * variables so it follows the active theme in light and dark mode.
 *
 * Reads sensor.amber_legionella_schedule (its attributes carry the separate
 * fields) and calls itho_amber.set_legionella_schedule.
 *
 * (c)2026 Mischa Bommer
 */

const SERVICE_DOMAIN = "itho_amber";
const SERVICE_NAME = "set_legionella_schedule";
const DEFAULT_ENTITY = "sensor.amber_legionella_schedule";

// Bit order of register 48 starts at Sunday; the display order starts at
// Monday because that is what people expect on a week schedule.
const DAY_KEYS = [
  "monday",
  "tuesday",
  "wednesday",
  "thursday",
  "friday",
  "saturday",
  "sunday",
];

// 2024-01-01 was a Monday, so this gives one date per weekday in display order.
const DAY_DATES = DAY_KEYS.map((_, index) => new Date(Date.UTC(2024, 0, 1 + index)));

const STYLES = `
  :host { display: block; }

  .summary {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 12px 16px;
    cursor: pointer;
    color: var(--primary-text-color);
  }
  .summary:focus-visible {
    outline: 2px solid var(--primary-color);
    outline-offset: -2px;
  }
  .summary:hover { background: rgba(var(--rgb-primary-text-color, 0, 0, 0), 0.04); }

  .icon {
    flex: 0 0 auto;
    width: 24px;
    height: 24px;
    color: var(--state-icon-color, var(--paper-item-icon-color, #44739e));
  }
  .icon svg { width: 100%; height: 100%; fill: currentColor; }

  .label { flex: 1 1 auto; min-width: 0; }
  .label .name {
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .label .hint {
    font-size: 0.85em;
    color: var(--secondary-text-color);
  }

  .value {
    flex: 0 0 auto;
    color: var(--secondary-text-color);
    text-align: right;
  }

  .chevron { flex: 0 0 auto; width: 20px; height: 20px; color: var(--secondary-text-color); }
  .chevron svg { width: 100%; height: 100%; fill: currentColor; }

  .backdrop {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.45);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9;
    padding: 16px;
    box-sizing: border-box;
  }

  .dialog {
    background: var(--ha-card-background, var(--card-background-color, #fff));
    color: var(--primary-text-color);
    border-radius: var(--ha-card-border-radius, 12px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.35);
    width: 100%;
    max-width: 420px;
    max-height: 100%;
    overflow: auto;
    padding: 24px;
    box-sizing: border-box;
  }

  .dialog h2 {
    margin: 0 0 4px;
    font-size: 1.25em;
    font-weight: 500;
  }
  .dialog .subtitle {
    margin: 0 0 20px;
    color: var(--secondary-text-color);
    font-size: 0.9em;
  }

  .days {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-bottom: 20px;
  }
  .chip {
    flex: 1 1 40px;
    min-width: 40px;
    padding: 10px 0;
    text-align: center;
    border: 1px solid var(--divider-color, #e0e0e0);
    border-radius: 18px;
    background: transparent;
    color: var(--primary-text-color);
    font: inherit;
    font-size: 0.9em;
    cursor: pointer;
    user-select: none;
  }
  .chip[aria-pressed="true"] {
    background: var(--primary-color, #03a9f4);
    border-color: var(--primary-color, #03a9f4);
    color: var(--text-primary-color, #fff);
  }
  .chip:focus-visible { outline: 2px solid var(--primary-color); outline-offset: 2px; }

  .field {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    margin-bottom: 8px;
  }
  .field label { color: var(--secondary-text-color); }
  .field input[type="time"] {
    font: inherit;
    font-size: 1.1em;
    padding: 8px 10px;
    color: var(--primary-text-color);
    background: var(--secondary-background-color, transparent);
    border: 1px solid var(--divider-color, #e0e0e0);
    border-radius: 8px;
    color-scheme: light dark;
  }

  .note {
    min-height: 20px;
    font-size: 0.85em;
    color: var(--secondary-text-color);
    margin-bottom: 16px;
  }
  .note.error { color: var(--error-color, #db4437); }

  .actions {
    display: flex;
    justify-content: flex-end;
    gap: 8px;
  }
  .actions button {
    font: inherit;
    text-transform: uppercase;
    font-size: 0.875em;
    font-weight: 500;
    letter-spacing: 0.05em;
    padding: 10px 16px;
    border: none;
    border-radius: 8px;
    background: transparent;
    color: var(--primary-color, #03a9f4);
    cursor: pointer;
  }
  .actions button:hover { background: rgba(var(--rgb-primary-color, 3, 169, 244), 0.08); }
  .actions button[disabled] { opacity: 0.5; cursor: default; }
`;

const ICON_CALENDAR =
  "M19 3h-1V1h-2v2H8V1H6v2H5a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V5a2 2 0 0 0-2-2m0 " +
  "18H5V9h14zM5 7V5h14v2zm7 3.5a5 5 0 1 0 5 5 5 5 0 0 0-5-5m1.75 7.4L11.5 16.5V13h1v3l1.9 1.1z";
const ICON_CHEVRON = "M8.6 16.6 13.2 12 8.6 7.4 10 6l6 6-6 6z";

class AmberLegionellaCard extends HTMLElement {
  constructor() {
    super();
    this.attachShadow({ mode: "open" });
    this._open = false;
    this._pendingDays = null;
    this._pendingTime = null;
    this._busy = false;
    this._note = "";
    this._error = false;
    this._onKeyDown = this._onKeyDown.bind(this);
  }

  static getStubConfig() {
    return { entity: DEFAULT_ENTITY };
  }

  setConfig(config) {
    this._config = {
      entity: DEFAULT_ENTITY,
      name: null,
      row: false,
      ...(config || {}),
    };
    this._render();
  }

  set hass(hass) {
    this._hass = hass;
    // While the dialog is open the local edits win, otherwise a poll halfway
    // through would move the chips under the user's fingers.
    if (!this._open) this._render();
    else this._renderSummary();
  }

  getCardSize() {
    return 1;
  }

  disconnectedCallback() {
    window.removeEventListener("keydown", this._onKeyDown);
  }

  // --- state helpers -------------------------------------------------------

  get _stateObj() {
    if (!this._hass || !this._config) return null;
    return this._hass.states[this._config.entity] || null;
  }

  get _dayLabels() {
    const language = (this._hass && this._hass.locale && this._hass.locale.language) || "en";
    const formatter = new Intl.DateTimeFormat(language, { weekday: "short", timeZone: "UTC" });
    return DAY_DATES.map((date) => {
      const label = formatter.format(date).replace(".", "");
      return label.charAt(0).toUpperCase() + label.slice(1);
    });
  }

  _currentDays() {
    const stateObj = this._stateObj;
    const days = (stateObj && stateObj.attributes.days) || [];
    return DAY_KEYS.filter((day) => days.includes(day));
  }

  _currentTime() {
    const stateObj = this._stateObj;
    const time = stateObj && stateObj.attributes.time;
    return typeof time === "string" && time.length >= 4 ? time : "00:00";
  }

  _summaryText() {
    const stateObj = this._stateObj;
    if (!stateObj) return "-";
    if (stateObj.state === "unavailable" || stateObj.state === "unknown") return "-";

    const days = this._currentDays();
    if (days.length === 0) return "-";

    const labels = this._dayLabels;
    const chosen = days.map((day) => labels[DAY_KEYS.indexOf(day)]).join(", ");
    return `${chosen}  ${this._currentTime()}`;
  }

  // --- dialog --------------------------------------------------------------

  _openDialog() {
    if (!this._stateObj) return;
    this._pendingDays = this._currentDays();
    this._pendingTime = this._currentTime();
    this._note = "";
    this._error = false;
    this._busy = false;
    this._open = true;
    window.addEventListener("keydown", this._onKeyDown);
    this._render();
  }

  _closeDialog() {
    this._open = false;
    window.removeEventListener("keydown", this._onKeyDown);
    this._render();
  }

  _onKeyDown(event) {
    if (event.key === "Escape" && this._open && !this._busy) {
      event.stopPropagation();
      this._closeDialog();
    }
  }

  _toggleDay(day) {
    const days = new Set(this._pendingDays);
    if (days.has(day)) days.delete(day);
    else days.add(day);
    this._pendingDays = DAY_KEYS.filter((key) => days.has(key));
    this._render();
  }

  _defaultName() {
    // Every entity of this integration carries the full device name in its
    // friendly name, which is far too long for a card. Strip that prefix so
    // the card shows "Amber Legionella schedule" instead.
    const stateObj = this._stateObj;
    const friendly = (stateObj && stateObj.attributes.friendly_name) || "Legionella schedule";
    const device = this._device();
    const deviceName = device && (device.name_by_user || device.name);
    if (deviceName && friendly.startsWith(`${deviceName} `)) {
      return friendly.slice(deviceName.length + 1);
    }
    return friendly;
  }

  _device() {
    const deviceId = this._deviceId();
    const devices = this._hass && this._hass.devices;
    return (deviceId && devices && devices[deviceId]) || null;
  }

  _deviceId() {
    // Passing the device makes the action unambiguous when someone runs more
    // than one Amber. Older frontends do not expose the entity registry here,
    // and then the action falls back to the only hub there is.
    const entities = this._hass && this._hass.entities;
    const entry = entities && entities[this._config.entity];
    return (entry && entry.device_id) || undefined;
  }

  async _save() {
    this._busy = true;
    this._note = "";
    this._error = false;
    this._render();

    const data = {
      days: this._pendingDays,
      time: `${this._pendingTime}:00`.slice(0, 8),
    };
    const deviceId = this._deviceId();
    if (deviceId) data.device_id = deviceId;

    try {
      await this._hass.callService(SERVICE_DOMAIN, SERVICE_NAME, data);
      this._closeDialog();
    } catch (err) {
      this._busy = false;
      this._error = true;
      this._note = (err && (err.message || err.error)) || "Writing to the heat pump failed";
      this._render();
    }
  }

  // --- rendering -----------------------------------------------------------

  _render() {
    if (!this._config) return;
    const root = this.shadowRoot;

    if (!this._built) {
      root.innerHTML = `<style>${STYLES}</style><div id="root"></div>`;
      this._built = true;
    }

    const stateObj = this._stateObj;
    const name = this._config.name || this._defaultName();

    const summary = `
      <div class="summary" tabindex="0" role="button">
        <div class="icon"><svg viewBox="0 0 24 24"><path d="${ICON_CALENDAR}"></path></svg></div>
        <div class="label">
          <div class="name">${name}</div>
          ${stateObj ? "" : `<div class="hint">${this._config.entity} not found</div>`}
        </div>
        <div class="value">${this._summaryText()}</div>
        <div class="chevron"><svg viewBox="0 0 24 24"><path d="${ICON_CHEVRON}"></path></svg></div>
      </div>`;

    const body = this._config.row ? summary : `<ha-card>${summary}</ha-card>`;
    root.querySelector("#root").innerHTML = body + (this._open ? this._dialogHtml(name) : "");

    const summaryEl = root.querySelector(".summary");
    summaryEl.addEventListener("click", () => this._openDialog());
    summaryEl.addEventListener("keydown", (event) => {
      if (event.key === "Enter" || event.key === " ") {
        event.preventDefault();
        this._openDialog();
      }
    });

    if (this._open) this._wireDialog();
  }

  _renderSummary() {
    const value = this.shadowRoot.querySelector(".value");
    if (value) value.textContent = this._summaryText();
  }

  _dialogHtml(name) {
    const labels = this._dayLabels;
    const chips = DAY_KEYS.map(
      (day, index) =>
        `<button class="chip" type="button" data-day="${day}" aria-pressed="${
          this._pendingDays.includes(day) ? "true" : "false"
        }">${labels[index]}</button>`
    ).join("");

    const subtitle =
      this._pendingDays.length === 0
        ? "No days selected, the programme will not run"
        : "Runs on the selected days at the time below";

    return `
      <div class="backdrop">
        <div class="dialog" role="dialog" aria-modal="true" aria-label="${name}">
          <h2>${name}</h2>
          <p class="subtitle">${subtitle}</p>
          <div class="days">${chips}</div>
          <div class="field">
            <label for="time">Start time</label>
            <input id="time" type="time" value="${this._pendingTime}" ${
      this._busy ? "disabled" : ""
    }>
          </div>
          <div class="note ${this._error ? "error" : ""}">${this._note}</div>
          <div class="actions">
            <button class="cancel" type="button" ${this._busy ? "disabled" : ""}>Cancel</button>
            <button class="save" type="button" ${this._busy ? "disabled" : ""}>${
      this._busy ? "Saving" : "Save"
    }</button>
          </div>
        </div>
      </div>`;
  }

  _wireDialog() {
    const root = this.shadowRoot;

    root.querySelectorAll(".chip").forEach((chip) => {
      chip.addEventListener("click", () => {
        if (!this._busy) this._toggleDay(chip.dataset.day);
      });
    });

    const time = root.querySelector("#time");
    time.addEventListener("change", () => {
      this._pendingTime = time.value || "00:00";
    });

    root.querySelector(".cancel").addEventListener("click", () => {
      if (!this._busy) this._closeDialog();
    });
    root.querySelector(".save").addEventListener("click", () => {
      if (!this._busy) this._save();
    });
    root.querySelector(".backdrop").addEventListener("click", (event) => {
      if (event.target.classList.contains("backdrop") && !this._busy) this._closeDialog();
    });

    const firstChip = root.querySelector(".chip");
    if (firstChip) firstChip.focus();
  }
}

if (!customElements.get("amber-legionella-card")) {
  customElements.define("amber-legionella-card", AmberLegionellaCard);
}

window.customCards = window.customCards || [];
if (!window.customCards.some((card) => card.type === "amber-legionella-card")) {
  window.customCards.push({
    type: "amber-legionella-card",
    name: "Amber legionella schedule",
    description:
      "Shows the anti-legionella schedule of an Itho Amber heat pump and opens a dialog to change it.",
  });
}

console.info("%c AMBER-LEGIONELLA-CARD ", "background:#03a9f4;color:#fff", "loaded");
