import { BezierEdge, BezierEdgeModel, h } from '@logicflow/core'
import { createApp, h as vh } from 'vue'
import { isActive, connect, disconnect } from './teleport'
import CustomLine from './CustomLine.vue'
function isMouseInElement(element: any, e: any) {
  const rect = element.getBoundingClientRect()
  return (
    e.clientX >= rect.left &&
    e.clientX <= rect.right &&
    e.clientY >= rect.top &&
    e.clientY <= rect.bottom
  )
}
const DEFAULT_WIDTH = 32
const DEFAULT_HEIGHT = 32
class CustomEdge2 extends BezierEdge {
  isMounted
  customLineApp?: any
  root?: any
  constructor() {
    super()
    this.isMounted = false
    this.handleMouseUp = (e: any) => {
      this.props.graphModel.clearSelectElements()
      this.props.model.isSelected = true
      const element = e.target.parentNode.parentNode.querySelector('.lf-custom-edge-wrapper')
      if (isMouseInElement(element, e)) {
        this.props.model.graphModel.deleteEdgeById(this.props.model.id)
      }
    }
  }
  /**
   * renderingvueComponents
   * @param root
   */
  protected renderVueComponent(root: any) {
    this.unmountVueComponent()
    this.root = root
    const { graphModel } = this.props
    if (root) {
      if (isActive()) {
        connect(
          this.targetId(),
          CustomLine,
          root,
          this.props.model,
          graphModel,
          (node: any, graph: any) => {
            return { model: node, graph }
          },
        )
      } else {
        this.customLineApp = createApp({
          render: () => vh(CustomLine, { model: this.props.model }),
        })
        this.customLineApp?.mount(root)
      }
    }
  }
  protected targetId() {
    return `${this.props.graphModel.flowId}:${this.props.model.id}`
  }
  /**
   * ComponentsThat is, Will uninstall hook
   */
  componentWillUnmount() {
    if (super.componentWillUnmount) {
      super.componentWillUnmount()
    }
    if (isActive()) {
      disconnect(this.targetId())
    }
    this.unmountVueComponent()
  }
  /**
   * uninstallvue
   * @returns
   */
  protected unmountVueComponent() {
    if (this.customLineApp) {
      this.customLineApp.unmount()
      this.customLineApp = null
    }
    if (this.root) {
      this.root.innerHTML = ''
    }
    return this.root
  }

  getEdge() {
    const { model } = this.props
    const id = model.id
    const { customWidth = DEFAULT_WIDTH, customHeight = DEFAULT_HEIGHT } = model.getProperties()
    const { startPoint, endPoint, path, isAnimation, arrowConfig } = model
    const animationStyle = model.getEdgeAnimationStyle()
    const {
      strokeDasharray,
      stroke,
      strokeDashoffset,
      animationName,
      animationDuration,
      animationIterationCount,
      animationTimingFunction,
      animationDirection,
    } = animationStyle
    const positionData = {
      x: (startPoint.x + endPoint.x - customWidth) / 2,
      y: (startPoint.y + endPoint.y - customHeight) / 2,
      width: customWidth,
      height: customHeight,
    }
    const style = model.getEdgeStyle()
    const wrapperStyle = {
      width: customWidth,
      height: customHeight,
    }

    setTimeout(() => {
      const s = document.getElementById(id)
      if (s && !this.isMounted) {
        this.isMounted = true
        this.renderVueComponent(s)
      }
    }, 0)

    delete style.stroke

    return h('g', {}, [
      h(
        'style' as any,
        { type: 'text/css' },
        '.lf-edge{stroke:#afafaf}.lf-edge:hover{stroke: #3370FF;}',
      ),
      h('path', {
        d: path,
        ...style,
        ...arrowConfig,
        ...(isAnimation
          ? {
              strokeDasharray,
              stroke,
              style: {
                strokeDashoffset,
                animationName,
                animationDuration,
                animationIterationCount,
                animationTimingFunction,
                animationDirection,
              },
            }
          : {}),
      }),
      h(
        'foreignObject',
        {
          ...positionData,
          y: positionData.y + 5,
          x: positionData.x + 5,
          style: {},
        },
        [
          h('div', {
            id,
            style: { ...wrapperStyle },
            className: 'lf-custom-edge-wrapper',
          }),
        ],
      ),
    ])
  }
}

class CustomEdgeModel2 extends BezierEdgeModel {
  getArrowStyle() {
    const arrowStyle = super.getArrowStyle()
    arrowStyle.offset = 1
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
        y: sourceAnchor.y,
      }
      this.updateStartPoint(startPoint)
      const endPoint = {
        x: targetAnchor.x,
        y: targetAnchor.y,
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
  type: 'app-edge',
  view: CustomEdge2,
  model: CustomEdgeModel2,
}
