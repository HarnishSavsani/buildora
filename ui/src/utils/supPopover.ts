// supPopover.ts
import {
  computePosition,
  flip,
  offset,
  shift,
  arrow,
  autoUpdate,
  type Placement,
} from '@floating-ui/dom'
import DOMPurify from 'dompurify'
let tooltipEl: HTMLDivElement | null = null
let arrowEl: HTMLDivElement | null = null
let contentEl: HTMLDivElement | null = null
let currentSup: HTMLElement | null = null
let cleanupAutoUpdate: (() => void) | null = null
let initialized = false

// ---- create tooltip DOM ----
function createTooltip() {
  const el = document.createElement('div')
  el.className = 'sup-popover'

  const inner = document.createElement('div')
  inner.className = 'sup-popover__content'
  el.appendChild(inner)

  const av = document.createElement('div')
  av.className = 'sup-popover__arrow'
  el.appendChild(av)

  document.body.appendChild(el)
  return { el, arrowEl: av, contentEl: inner }
}

// ---- Positioning calculation ----
async function updatePosition(reference: HTMLElement) {
  if (!tooltipEl || !arrowEl) return

  const { x, y, placement, middlewareData } = await computePosition(reference, tooltipEl, {
    placement: 'top',
    middleware: [offset(10), flip(), shift({ padding: 8 }), arrow({ element: arrowEl })],
  })

  Object.assign(tooltipEl.style, { left: `${x}px`, top: `${y}px` })
  tooltipEl.dataset.placement = placement

  const { x: ax, y: ay } = middlewareData.arrow ?? {}
  const side = placement.split('-')[0] as 'top' | 'bottom' | 'left' | 'right'
  const staticSide = { top: 'bottom', bottom: 'top', left: 'right', right: 'left' }[side]

  Object.assign(arrowEl.style, {
    left: '',
    top: '',
    right: '',
    bottom: '',
    ...(ax != null ? { left: `${ax}px` } : {}),
    ...(ay != null ? { top: `${ay}px` } : {}),
    [staticSide]: '-5px',
  })
}

// ---- show / hide ----
function show(sup: HTMLElement) {
  if (!tooltipEl || !contentEl) return

  // filter XSS，Keep only safe ones HTML Tagsandproperty
  contentEl.innerHTML = DOMPurify.sanitize(sup.dataset.title ?? '')

  tooltipEl.style.display = 'block'
  tooltipEl.style.pointerEvents = 'auto'

  cleanupAutoUpdate?.()
  cleanupAutoUpdate = autoUpdate(sup, tooltipEl, () => updatePosition(sup))
}

function hide() {
  if (!tooltipEl) return
  tooltipEl.style.display = 'none'
  cleanupAutoUpdate?.()
  cleanupAutoUpdate = null
  currentSup = null
}

// ---- Core: use pointer Path judgment Yes is in the safe zone ----
// Record mouse coordinates
let mouseX = 0
let mouseY = 0
document.addEventListener(
  'mousemove',
  (e) => {
    mouseX = e.clientX
    mouseY = e.clientY
  },
  { passive: true },
)

function isMouseInsideSafeZone(): boolean {
  if (!tooltipEl || !currentSup) return false

  const supRect = currentSup.getBoundingClientRect()
  const tipRect = tooltipEl.getBoundingClientRect()

  // Put sup and tooltip of rect Each extension 2px Tolerance，
  // Then determine whether the mouse Yes is In the convex hull of the two pieces rectangle（union bbox）Inside
  const pad = 2
  const minX = Math.min(supRect.left, tipRect.left) - pad
  const maxX = Math.max(supRect.right, tipRect.right) + pad
  const minY = Math.min(supRect.top, tipRect.top) - pad
  const maxY = Math.max(supRect.bottom, tipRect.bottom) + pad

  return mouseX >= minX && mouseX <= maxX && mouseY >= minY && mouseY <= maxY
}

// ---- EventsProcessing ----
function onMouseOver(e: MouseEvent) {
  const sup = (e.target as HTMLElement).closest('sup[data-title]') as HTMLElement | null
  if (!sup) return

  if (sup !== currentSup) {
    currentSup = sup
    show(sup)
  }
}

function onMouseMove(e: MouseEvent) {
  if (!currentSup) return

  // mouseIn tooltip Internally, skip directly and do nothingProcessing
  if (tooltipEl && (e.target === tooltipEl || tooltipEl.contains(e.target as Node))) return

  const overSup = (e.target as HTMLElement).closest('sup[data-title]')

  if (!overSup && !isMouseInsideSafeZone()) {
    hide()
  }
}

// ---- SingleExamplecommon API ----
export const supPopover = {
  init() {
    if (initialized) return
    initialized = true

    const els = createTooltip()
    tooltipEl = els.el
    arrowEl = els.arrowEl
    contentEl = els.contentEl

    document.addEventListener('mouseover', onMouseOver)
    document.addEventListener('mousemove', onMouseMove, { passive: true })
  },

  destroy() {
    document.removeEventListener('mouseover', onMouseOver)
    document.removeEventListener('mousemove', onMouseMove)
    cleanupAutoUpdate?.()
    tooltipEl?.remove()
    tooltipEl = null
    arrowEl = null
    contentEl = null
    currentSup = null
    initialized = false
  },
}
