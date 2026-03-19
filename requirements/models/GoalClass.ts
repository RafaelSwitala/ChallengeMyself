import { GoalPeriodTypeEnum } from "../enums/GoalPeriodTypeEnum"
import { GoalTypeEnum } from "../enums/GoalTypeEnum"
import { IGoal } from "../interfaces/IGoal"

export class Goal implements IGoal {
  description: string
  variableReference: string
  type: GoalTypeEnum;
  target: number;
  period: GoalPeriodTypeEnum;
  secondaryTarget?: number; // For conditional goals
  secondaryReference?: string; // For conditional goals
  createdAt: number;
  updatedAt: number;

  constructor(data: IGoal) {
    this.description = data.description
    this.variableReference = data.variableReference
    this.type = data.type
    this.target = data.target
    this.period = data.period
    this.secondaryTarget = data.secondaryTarget
    this.secondaryReference = data.secondaryReference
    this.createdAt = data.createdAt
    this.updatedAt = data.updatedAt
  }

  isType(type: GoalTypeEnum): boolean {
    return this.type === type
  }
}
