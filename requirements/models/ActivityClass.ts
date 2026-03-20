import { ActivityTypeEnum } from "../enums/ActivityTypeEnum";
import { FieldKeyEnum } from "../enums/FieldKeyEnum";
import { Field } from "./FieldClass";
import { fieldModels } from "./fieldModels";

export interface FieldConfig {
  key: FieldKeyEnum;
  required?: boolean;
}

export class Activity {
  type: ActivityTypeEnum;
  fields: Field[];

  constructor(type: ActivityTypeEnum, fieldConfigs: (FieldKeyEnum | FieldConfig)[]) {
    this.type = type;
    this.fields = fieldConfigs.map(config => {
      const key = typeof config === "string" ? config : config.key;
      const field = fieldModels[key];
      
      // Falls required gesetzt ist, kopieren wir das Field und setzen required
      if (typeof config === "object" && config.required !== undefined) {
        return new Field(
          field.key,
          field.label,
          field.fieldType,
          field.chartType,
          field.trackable,
          field.hidden,
          field.unit,
          field.options,
          config.required
        );
      }
      
      return field;
    });
  }
}

