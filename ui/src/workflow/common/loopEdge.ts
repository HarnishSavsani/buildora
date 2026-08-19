import { BezierEdge, BezierEdgeModel, h } from '@logicflow/core'

class CustomEdgeModel2 extends BezierEdgeModel {
  getArrowStyle() {
    const arrowStyle = super.getArrowStyle()
    arrowStyle.offset = 0
    arrowStyle.verticalLength = 0
    return arrowStyle
  }

  getEdgeStyle() {
    const style = super.getEdgeStyle()
    // svgproperty
    style.strokeWidth = 2
    style.stroke = '#BBBFC4'
    style.offset = 0
    return style
  }
  /**
   * Override this method to enable savingNumberAccording toYesCan bring an anchor pointNumberAccording to。
   */
  getData() {
    const data: any = super.getData()
    if (data) {
      data.sourceAnchorId = this.sourceAnchorId
      data.targetAnchorId = this.targetAnchorId
    }
    return data
  }
  /**
   * Give the edge a Customize solution so that it supports renewing the path of the edge based on the position of the anchor point.
   */
  updatePathByAnchor() {
    // TODO
    const sourceNodeModel = this.graphModel.getNodeModelById(this.sourceNodeId)
    const sourceAnchor = sourceNodeModel
      .getDefaultAnchor()
      .find((anchor: any) => anchor.id === this.sourceAnchorId)

    const targetNodeModel = this.graphModel.getNodeModelById(this.targetNodeId)
    const targetAnchor = targetNodeModel
      .getDefaultAnchor()
      .find((anchor: any) => anchor.id === this.targetAnchorId)
    if (sourceAnchor && targetAnchor) {
      const startPoint = {
        x: sourceAnchor.x,
        y: sourceAnchor.y - 10
      }
      this.updateStartPoint(startPoint)
      const endPoint = {
        x: targetAnchor.x,
        y: targetAnchor.y + 3
      }

      this.updateEndPoint(endPoint)
    }

    // Will's original pointsListSettingsfor needs to be empty here to trigger bezier's automatic calculation of control points.。
    this.pointsList = []
    this.initPoints()
  }
  setAttributes(): void {
    super.setAttributes()
    this.isHitable = true
    this.zIndex = 0
  }
}

export default {
  type: 'loop-edge',
  view: BezierEdge,
  model: CustomEdgeModel2
}
