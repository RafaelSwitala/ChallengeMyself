import { ISession } from "../interfaces/ISession";

export class Session implements ISession {
  constructor(
    public id: string,
    public date: string,
    public time: string,
    public values: Record<string, any>,
    public createdAt: number = Date.now(),
    public updatedAt: number = Date.now()
  ) {}

  
}