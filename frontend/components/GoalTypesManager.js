/**
 * GoalTypes Manager - Einfaches JavaScript-Modul für GoalTypes
 * 
 * Verwendung:
 * const manager = new GoalTypesManager("MeineChallenge", "Joggen");
 * await manager.initialize();
 * await manager.displayGoalTypesUI();
 */

class GoalTypesManager {
  constructor(challengeName, activity) {
    this.challengeName = challengeName;
    this.activity = activity;
    this.goalTypes = [];
    this.availableTypes = {};
  }

  async initialize() {
    try {
      // Lade verfügbare GoalTypes für die Aktivität
      const response = await fetch(`/activities/${this.activity}/goal-types`);
      const data = await response.json();
      this.availableTypes = data.available_goal_types || {};
      
      // Lade aktuelle GoalTypes der Challenge
      await this.loadGoalTypes();
      
      console.log("✅ GoalTypesManager initialisiert");
      return true;
    } catch (error) {
      console.error("❌ Fehler beim Initialisieren:", error);
      return false;
    }
  }

  async loadGoalTypes() {
    try {
      const response = await fetch(`/challenges/${this.challengeName}/goal-types`);
      const data = await response.json();
      this.goalTypes = data.goal_types || [];
      console.log("✅ GoalTypes geladen:", this.goalTypes);
    } catch (error) {
      console.error("❌ Fehler beim Laden der GoalTypes:", error);
    }
  }

  /**
   * Stelle ein Ziel "mindestens X km pro Monat" dar
   */
  createMoreThanGoal(value, period = "monthly", unit = "km", metric = "distance") {
    return {
      type: "MORE_THAN",
      target_value: value,
      period: period,
      unit: unit,
      metric: metric
    };
  }

  /**
   * Stelle ein Ziel "mindestens 3x pro Woche" dar
   */
  createFrequencyMinGoal(sessions, period = "weekly") {
    return {
      type: "FREQUENCY_MIN",
      min_sessions: sessions,
      period: period
    };
  }

  /**
   * Stelle ein Ziel "durchschnittlich 30 min" dar
   */
  createAverageAboveGoal(average, metric = "duration", unit = "minutes") {
    return {
      type: "AVERAGE_ABOVE",
      target_average: average,
      metric: metric,
      unit: unit
    };
  }

  /**
   * Stelle ein Ziel "Mo, Mi, Fr joggen" dar
   */
  createRecurrencePatternGoal(daysOfWeek) {
    return {
      type: "RECURRENCE_PATTERN",
      days_of_week: daysOfWeek
    };
  }

  /**
   * Speichert ein GoalType in der Challenge
   */
  async addGoalType(goalTypeData) {
    try {
      const response = await fetch(
        `/challenges/${this.challengeName}/goal-types`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(goalTypeData)
        }
      );

      if (response.ok) {
        await this.loadGoalTypes();
        console.log(`✅ GoalType "${goalTypeData.type}" hinzugefügt`);
        return true;
      } else {
        const error = await response.json();
        console.error(`❌ Fehler: ${error.error}`);
        return false;
      }
    } catch (error) {
      console.error("❌ Fehler beim Speichern:", error);
      return false;
    }
  }

  /**
   * Löscht ein GoalType aus der Challenge
   */
  async removeGoalType(goalTypeName) {
    try {
      const response = await fetch(
        `/challenges/${this.challengeName}/goal-types/${goalTypeName}`,
        { method: 'DELETE' }
      );

      if (response.ok) {
        await this.loadGoalTypes();
        console.log(`✅ GoalType "${goalTypeName}" gelöscht`);
        return true;
      } else {
        const error = await response.json();
        console.error(`❌ Fehler: ${error.error}`);
        return false;
      }
    } catch (error) {
      console.error("❌ Fehler beim Löschen:", error);
      return false;
    }
  }

  /**
   * Erzeugt HTML für ein GoalType-Formular
   */
  generateGoalTypeForm(goalTypeName, config) {
    const typeConfig = this.availableTypes[goalTypeName];
    if (!typeConfig) return "";

    let html = `<div class="goal-type-form" data-type="${goalTypeName}">`;
    html += `<h4>${typeConfig.label}</h4>`;
    html += `<p class="description">${typeConfig.description}</p>`;

    switch (goalTypeName) {
      case "MORE_THAN":
        html += `
          <div class="form-group">
            <label>Zielwert</label>
            <input type="number" class="goal-input" placeholder="${typeConfig.example}" 
                   data-field="target_value" step="0.1">
          </div>
          <div class="form-group">
            <label>Einheit</label>
            <select class="goal-select" data-field="unit">
              <option value="km" ${typeConfig.default_unit === 'km' ? 'selected' : ''}>km</option>
              <option value="minutes" ${typeConfig.default_unit === 'minutes' ? 'selected' : ''}>Minuten</option>
            </select>
          </div>
          <div class="form-group">
            <label>Zeitraum</label>
            <select class="goal-select" data-field="period">
              <option value="daily">Täglich</option>
              <option value="weekly">Wöchentlich</option>
              <option value="monthly" selected>Monatlich</option>
              <option value="yearly">Jährlich</option>
            </select>
          </div>
        `;
        break;

      case "FREQUENCY_MIN":
        html += `
          <div class="form-group">
            <label>Mindestanzahl Sessions</label>
            <input type="number" class="goal-input" placeholder="${typeConfig.example}" 
                   data-field="min_sessions" min="1">
          </div>
          <div class="form-group">
            <label>Zeitraum</label>
            <select class="goal-select" data-field="period">
              <option value="daily">Täglich</option>
              <option value="weekly" selected>Wöchentlich</option>
              <option value="monthly">Monatlich</option>
            </select>
          </div>
        `;
        break;

      case "AVERAGE_ABOVE":
        html += `
          <div class="form-group">
            <label>Durchschnittlicher Wert</label>
            <input type="number" class="goal-input" placeholder="${typeConfig.example}" 
                   data-field="target_average" step="0.1" min="0">
          </div>
          <div class="form-group">
            <label>Metrik</label>
            <select class="goal-select" data-field="metric">
              <option value="duration" selected>Dauer</option>
              <option value="distance">Distanz</option>
              <option value="speed">Geschwindigkeit</option>
            </select>
          </div>
        `;
        break;

      case "RECURRENCE_PATTERN":
        const days = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"];
        html += `<div class="form-group"><label>Wochentage auswählen</label><div class="days-checkboxes">`;
        days.forEach(day => {
          html += `
            <label class="day-checkbox">
              <input type="checkbox" class="day-input" value="${day}"> ${day}
            </label>
          `;
        });
        html += `</div></div>`;
        break;
    }

    html += `
      <button class="btn-save-goal" data-type="${goalTypeName}">Speichern</button>
      <button class="btn-cancel-goal" data-type="${goalTypeName}">Abbrechen</button>
    </div>`;

    return html;
  }

  /**
   * Zeigt alle verfügbaren GoalTypes als UI an
   */
  async displayGoalTypesUI(containerId = "goal-types-container") {
    const container = document.getElementById(containerId);
    if (!container) {
      console.error(`❌ Container mit ID "${containerId}" nicht gefunden`);
      return;
    }

    let html = `<div class="goal-types-manager">`;
    html += `<h3>Ziele definieren</h3>`;
    html += `<p class="info">Sie können mehrere Ziele kombinieren!</p>`;

    // Verfügbare GoalTypes
    html += `<div class="available-goal-types">`;
    Object.keys(this.availableTypes).forEach(typeName => {
      const isActive = this.goalTypes.some(g => g.type === typeName);
      html += `
        <div class="goal-type-card ${isActive ? 'active' : ''}">
          <input type="checkbox" class="goal-checkbox" value="${typeName}" 
                 ${isActive ? 'checked' : ''} id="check-${typeName}">
          <label for="check-${typeName}">
            <strong>${this.availableTypes[typeName].label}</strong>
            <p>${this.availableTypes[typeName].description}</p>
          </label>
        </div>
      `;
    });
    html += `</div>`;

    // Formulare
    html += `<div class="goal-forms">`;
    Object.keys(this.availableTypes).forEach(typeName => {
      html += this.generateGoalTypeForm(typeName);
    });
    html += `</div>`;

    // Aktive Ziele
    html += `<div class="active-goals">`;
    html += `<h4>Aktive Ziele:</h4>`;
    html += `<ul class="goals-list">`;
    this.goalTypes.forEach(goal => {
      html += `<li class="goal-item" data-type="${goal.type}">
        ${this.formatGoalDisplay(goal)}
        <button class="btn-delete-goal" data-type="${goal.type}">✕</button>
      </li>`;
    });
    html += `</ul></div>`;
    html += `</div>`;

    container.innerHTML = html;
    this.attachEventListeners();
  }

  /**
   * Formatiert ein GoalType zur Anzeige
   */
  formatGoalDisplay(goal) {
    switch (goal.type) {
      case "MORE_THAN":
        return `${goal.target_value}${goal.unit} pro ${goal.period}`;
      case "FREQUENCY_MIN":
        return `Mindestens ${goal.min_sessions}x pro ${goal.period}`;
      case "AVERAGE_ABOVE":
        return `Ø ${goal.target_average}${goal.unit} pro Session`;
      case "RECURRENCE_PATTERN":
        return `${goal.days_of_week.join(", ")}`;
      default:
        return goal.type;
    }
  }

  /**
   * Attachiert Event-Listener an die UI-Elemente
   */
  attachEventListeners() {
    // Checkbox für GoalTypes
    document.querySelectorAll(".goal-checkbox").forEach(checkbox => {
      checkbox.addEventListener("change", (e) => {
        const form = document.querySelector(`[data-type="${e.target.value}"]`);
        if (form && form.classList.contains("goal-type-form")) {
          if (e.target.checked) {
            form.style.display = "block";
          } else {
            form.style.display = "none";
          }
        }
      });
    });

    // Save Buttons
    document.querySelectorAll(".btn-save-goal").forEach(btn => {
      btn.addEventListener("click", async (e) => {
        const form = btn.closest(".goal-type-form");
        const goalData = this.extractFormData(form);
        if (goalData) {
          await this.addGoalType(goalData);
          await this.displayGoalTypesUI("goal-types-container");
        }
      });
    });

    // Cancel Buttons
    document.querySelectorAll(".btn-cancel-goal").forEach(btn => {
      btn.addEventListener("click", (e) => {
        const form = btn.closest(".goal-type-form");
        const checkbox = document.querySelector(
          `.goal-checkbox[value="${e.target.dataset.type}"]`
        );
        if (checkbox) checkbox.checked = false;
        form.style.display = "none";
      });
    });

    // Delete Buttons
    document.querySelectorAll(".btn-delete-goal").forEach(btn => {
      btn.addEventListener("click", async (e) => {
        if (confirm("Ziel wirklich löschen?")) {
          await this.removeGoalType(e.target.dataset.type);
          await this.displayGoalTypesUI("goal-types-container");
        }
      });
    });
  }

  /**
   * Extrahiert Daten aus einem Formular
   */
  extractFormData(form) {
    const type = form.dataset.type;
    const goalData = { type };

    switch (type) {
      case "MORE_THAN":
        goalData.target_value = parseFloat(
          form.querySelector('[data-field="target_value"]').value
        );
        goalData.period = form.querySelector('[data-field="period"]').value;
        goalData.unit = form.querySelector('[data-field="unit"]').value;
        goalData.metric = "distance"; // Hardcoded für Joggen
        break;

      case "FREQUENCY_MIN":
        goalData.min_sessions = parseInt(
          form.querySelector('[data-field="min_sessions"]').value
        );
        goalData.period = form.querySelector('[data-field="period"]').value;
        break;

      case "AVERAGE_ABOVE":
        goalData.target_average = parseFloat(
          form.querySelector('[data-field="target_average"]').value
        );
        goalData.metric = form.querySelector('[data-field="metric"]').value;
        goalData.unit = "minutes";
        break;

      case "RECURRENCE_PATTERN":
        const selectedDays = Array.from(
          form.querySelectorAll(".day-input:checked")
        ).map(input => input.value);
        goalData.days_of_week = selectedDays;
        break;
    }

    return goalData;
  }
}

// Beispiel-Integration
async function initGoalTypesUI(challengeName, activity) {
  const manager = new GoalTypesManager(challengeName, activity);
  
  if (await manager.initialize()) {
    await manager.displayGoalTypesUI("goal-types-container");
    return manager;
  }
  return null;
}

// Export für Verwendung
if (typeof module !== 'undefined' && module.exports) {
  module.exports = GoalTypesManager;
}
