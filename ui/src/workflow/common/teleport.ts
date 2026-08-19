import { BaseEdgeModel, BaseNodeModel, GraphModel } from '@logicflow/core'
import { defineComponent, h, reactive, isVue3, Teleport, markRaw, Fragment } from 'vue-demi'

let active = false
const items = reactive<{ [key: string]: any }>({})

export function connect(
  id: string,
  component: any,
  container: HTMLDivElement,
  node: BaseNodeModel | BaseEdgeModel,
  graph: GraphModel,
  get_props?: any,
  get_provide?: any,
) {
  if (!get_props) {
    get_props = (node: BaseNodeModel | BaseEdgeModel, graph: GraphModel) => {
      return { nodeModel: node, graph }
    }
  }
  if (!get_provide) {
    get_provide = (node: BaseNodeModel | BaseEdgeModel, graph: GraphModel) => ({
      getNode: () => node,
      getGraph: () => graph,
    })
  }
  if (active) {
    items[id] = markRaw(
      defineComponent({
        render: () => h(Teleport, { to: container } as any, [h(component, get_props(node, graph))]),
        provide: () => get_provide(node, graph),
      }),
    )
  }
}

export function disconnect(id: string) {
  if (active) {
    delete items[id]
  }
}
export function disconnectByFlow(flowId: string) {
  Object.keys(items).forEach((key) => {
    if (key.startsWith(flowId)) {
      delete items[key]
    }
  })
}
export function disconnectAll() {
  Object.keys(items).forEach((key) => {
    delete items[key]
  })
}

export function isActive() {
  return active
}

export function getTeleport(): any {
  if (!isVue3) {
    throw new Error('teleport is only available in Vue3')
  }
  active = true

  return defineComponent({
    props: {
      flowId: {
        type: String,
        required: true,
      },
    },
    setup(props) {
      return () => {
        const children: Record<string, any>[] = []
        Object.keys(items).forEach((id) => {
          // https://github.com/didi/LogicFlow/issues/1768
          // Multiple pieces and different VueNodeViews will connect to register arriveitemsMedium, so items stores a flow chart that may have multiple piecesflowIds.NumberAccording to
          // When using multiple piecesLogicFlow, it will create morepiecesflowId + at the same timeuseKeepAlive
          // Every time items change, it will trigger the flowId held by differentsetup()implement，The value ofevery timesetup()The execution traverses items, so there is a possibility of repeatedly rendering elements multiple times.Problem
          // That is, items[0] will be InPage1setup()Execution, items[0] will also count thesetup()execute, thereby generating twopiecesitems[0]

          // Compare the flowId displayed on the current interface, onlyrenewitems[Current pageface flowId:nodeId]NumberAccording to
          // for exampleitems[0]Belongs to Page1NumberAccording to，Then Page2 cannot be executed regardless of active=true/false.items[0]

          children.push(items[id])
        })
        return h(
          Fragment,
          {},
          children.map((item) => h(item)),
        )
      }
    },
  })
}
