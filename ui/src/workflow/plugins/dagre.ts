import { DagreLayout, type DagreLayoutOptions } from '@antv/layout'

export default class Dagre {
  static pluginName = 'dagre'
  lf: any
  option: DagreLayoutOptions | any
  render(lf: any) {
    this.lf = lf
  }

  /**
   * option: {
   *   rankdir: "TB", // layout direction, Optional TB, BT, LR, RL
   *   align: undefined, // NodeAlignment, optional UL, UR, DL, DR
   *   nodeSize: undefined, // Nodesize
   *   nodesepFunc: undefined, // Nodehorizontal spacing(px)
   *   ranksepFunc: undefined, // NodeBetween spacing for each layer
   *   nodesep: 40, // Nodehorizontal spacing(px) Notice：likeIf there is a grid, it is necessary to ensure that the nodesepforgrid is even Number times
   *   ranksep: 40, // NodeBetween spacing for each layer Notice：likeIf there is a grid, you need to ensure that the ranksepforgrid is even Number times
   *   controlPoints: false, // YesWhether to retain the control points of the layout connection
   *   radial: false, // YesNo based on dagre Perform radial layout
   *   focusNode: null, // radial for true Effective at that time, attention is paid toNode
   * };
   */
  layout(option = {}) {
    const { nodes, edges, gridSize } = this.lf.graphModel
    // forIn order to ensure the generated NodeIngirdSize, Processing is required.。
    let nodesep = 40
    let ranksep = 40
    if (gridSize > 20) {
      nodesep = gridSize * 2
      ranksep = gridSize * 2
    }
    this.option = {
      type: 'dagre',
      rankdir: 'LR',
      // align: 'UL',
      // align: 'UR',
      align: 'DR',
      nodesep,
      ranksep,
      begin: [120, 120],
      ...option,
    }
    const layoutInstance = new DagreLayout(this.option)
    const layoutData = layoutInstance.layout({
      nodes: nodes.map((node: any) => ({
        id: node.id,
        size: {
          width: node.width,
          height: node.height,
        },
        model: node,
      })),
      edges: edges.map((edge: any) => ({
        source: edge.sourceNodeId,
        target: edge.targetNodeId,
        model: edge,
      })),
    })

    layoutData.nodes?.forEach((node: any) => {
      // @ts-ignore: pass node data
      const { model } = node
      model.set_position({ x: node.x, y: node.y })
    })
    this.lf.fitView()
  }
}
