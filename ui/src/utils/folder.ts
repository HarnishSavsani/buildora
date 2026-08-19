/**
 * Bitwise Sortingtool functionNumber
 * High 16 bits - whole Number, low 16 bits - smallNumber
 */

const FRACTION_BITS = 16
const FRACTION_MASK = 0xffff

// Encode 32-bit integerNumber
function encode(integer: number, fraction = 0) {
  return (integer << FRACTION_BITS) | (fraction & FRACTION_MASK)
}

// Calculate the position of two pieces Mediumvalue 
function mid(pos1: number, pos2: number) {
  const midPos = (pos1 + pos2) >> 1
  if (midPos === pos1 || midPos === pos2) {
    return null
  }
  return midPos
}

// Rebalancing, when the adjacent position difference is less than 2, it cannot be inserted.
// positions - { nodeId: position }
function rebalance(positions: any) {
  const sorted = Object.entries(positions).sort((a: any, b: any) => a[1] - b[1])

  const rebalanced = {} as Record<string, number>
  sorted.forEach(([nodeId], index) => {
    rebalanced[nodeId] = encode(index + 1, 0)
  })
  return rebalanced
}


export { encode, rebalance, mid }
