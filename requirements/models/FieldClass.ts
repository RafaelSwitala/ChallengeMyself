import { ChartTypeEnum } from "../enums/ChartTypeEnum";
import { FieldKeyEnum } from "../enums/FieldKeyEnum";
import { FieldTypeEnum } from "../enums/FieldTypeEnum";

export class Field<T = any> {
  constructor(
    public key: FieldKeyEnum,
    public label: string,
    public fieldType: FieldTypeEnum,
    public chartType: ChartTypeEnum,
    public trackable: boolean = false,
    public hidden: boolean = false,
    public unit?: string,
    public options?: T,
    public required?: boolean // Optional = false, Required = true
  ) {}
}

