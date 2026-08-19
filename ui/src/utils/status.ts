import { type Dict } from '@/api/type/common'
interface TaskTypeInterface {
  // vectorization
  EMBEDDING: number
  // generate questions
  GENERATE_PROBLEM: number
  // synchronous
  SYNC: number
  // index
  TOKENIZE: number
}
interface StateInterface {
  // etc.To be
  PENDING: '0'
  // implementMedium
  STARTED: '1'
  // success
  SUCCESS: '2'
  // Failed
  FAILURE: '3'
  // Cancel task
  REVOKE: '4'
  // Cancelsuccess
  REVOKED: '5'
  IGNORED: 'n'
}
const TaskType: TaskTypeInterface = {
  EMBEDDING: 1,
  GENERATE_PROBLEM: 2,
  SYNC: 3,
  TOKENIZE: 4,
}
const State: StateInterface = {
  // etc.To be
  PENDING: '0',
  // implementMedium
  STARTED: '1',
  // success
  SUCCESS: '2',
  // Failed
  FAILURE: '3',
  // Cancel task
  REVOKE: '4',
  // Cancelsuccess
  REVOKED: '5',
  IGNORED: 'n'
}
class Status {
  task_status: Dict<any>
  constructor(status?: string) {
    if (!status) {
      status = ''
    }
    status = status.split('').reverse().join('')
    this.task_status = {}
    for (const key in TaskType) {
      const value = TaskType[key as keyof TaskTypeInterface]
      const index = value - 1
      this.task_status[value] = status[index] ? status[index] : 'n'
    }
  }
  toString() {
    const r = []
    for (const key in TaskType) {
      const value = TaskType[key as keyof TaskTypeInterface]
      r.push(this.task_status[value])
    }
    return r.reverse().join('')
  }
}
export { Status, State, TaskType, type TaskTypeInterface, type StateInterface }
