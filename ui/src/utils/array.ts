/**
 * Split Number group Split each npieces for one piecesNumber group
 * @param sourceDataList resourceNumberAccording to
 * @param splitNum       Split every how many pieces for a piecesNumber group
 * @returns              Number group after splitting
 */
export function splitArray<T>(sourceDataList: Array<T>, splitNum: number) {
  const count =
    sourceDataList.length % splitNum == 0
      ? sourceDataList.length / splitNum
      : sourceDataList.length / splitNum + 1
  const arrayList: Array<Array<T>> = []
  for (let i = 0; i < count; i++) {
    let index = i * splitNum
    const list: Array<T> = []
    let j = 0
    while (j < splitNum && index < sourceDataList.length) {
      list.push(sourceDataList[index++])
      j++
    }
    arrayList.push(list)
  }
  return arrayList
}
/*
Tree structure flattened
*/
export function TreeToFlatten(treeData: any[]) {
  return treeData.reduce((acc, node) => {
    const { children, ...rest } = node
    return [...acc, rest, ...(children ? TreeToFlatten(children) : [])]
  }, [])
}

/*
  Filter out the corresponding objects from the specified Number group Medium
*/
export function relatedObject(list: any, val: any, attr: string) {
  const filterData: any = list.find((item: any) => item[attr] === val)
  return filterData || null
}

// Sorting
export function arraySort(list: Array<any>, property: any, desc?: boolean) {
  return list.sort((a: any, b: any) => {
    return desc ? b[property] - a[property] : a[property] - b[property]
  })
}

// Determine allpropertyallfor is empty in the object
export function isAllPropertiesEmpty(obj: object) {
  return Object.values(obj).every(
    (value) =>
      value === null || typeof value === 'undefined' || (typeof value === 'string' && !value),
  )
}

// NumberA collection of a certain property value of the group object Medium
export function getAttrsArray(array: Array<any>, attr: string) {
  return array.map((item) => {
    return item[attr]
  })
}

// Ask forand
export function getSum(array: Array<any>) {
  return array.reduce((total, item) => total + item, 0)
}

// Object Number group deduplication
export function uniqueArray(array: Array<any>, key: string) {
  const map = new Map()
  return array.filter((item) => {
    return !map.has(item[key]) && map.set(item[key], 1)
  })
}
