import { IChallenge } from "../interfaces/IChallenge";
import { Goal } from "./GoalClass";
import { Session } from "./SessionClass";

export class Challenge implements IChallenge {
  sessions: Session[] = [];
  goal?: Goal;

  constructor(
    public id: string,
    public name: string,
    public activityType: string,
    public createdAt: number = Date.now(),
    public updatedAt: number = Date.now(),
    sessions?: Session[],
    goal?: Goal
  ) {
    this.sessions = sessions || [];
    this.goal = goal;
  }

  addSession(session: Session) {
    this.sessions.push(session);
    // Keep sessions sorted by date and time
    this.sessions.sort((a, b) => {
      const dateCompare = a.date.localeCompare(b.date);
      return dateCompare !== 0 ? dateCompare : a.time.localeCompare(b.time);
    });
    this.updatedAt = Date.now();
  }

  setGoal(goal: Goal) {
    this.goal = goal;
    this.updatedAt = Date.now();
  }

  removeGoal() {
    this.goal = undefined;
    this.updatedAt = Date.now();
  }





}