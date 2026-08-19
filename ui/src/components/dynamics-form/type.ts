import type { Dict } from '@/api/type/common'

interface ViewCardItem {
  /**
   * Type
   */
  type: 'eval' | 'default'
  /**
   * Title
   */
  title: string
  /**
   * value RootAccording toTypeDifferent Getting the value is also different default= row[value_field] eval `${parseFloat(row.number).toLocaleString("zh-CN",{style: "decimal",maximumFractionDigits:1})}%&nbsp;&nbsp;&nbsp;`
   */
  value_field: string
}

interface TableColumn {
  /**
   * Fields|Componentsname | computable templatecharacter string
   */
  property: string
  /**
   *Header
   */
  label: string
  /**
   * surfaceNumberAccording toFields
   */
  value_field?: string

  attrs?: Attrs
  /**
   * Type
   */
  type: 'eval' | 'component' | 'default'

  props_info?: PropsInfo
}
interface ColorItem {
  /**
   * color#f56c6c
   */
  color: string
  /**
   * Progress
   */
  percentage: number
}
interface Attrs {
  /**
   * hintlanguage
   */
  placeholder?: string
  /**
   * Tagslength，For example '50px'。 Operationfor Form direct subelement form-item will inherit thevalue。 Canuse auto。
   */
  labelWidth?: string
  /**
   * Suffix of table Single field Tags
   */
  labelSuffix?: string
  /**
   * The position of the asterisk。
   */
  requireAsteriskPosition?: 'left' | 'right'

  color?: Array<ColorItem>

  [propName: string]: any
}
interface PropsInfo {
  /**
   * sheetselectedcard
   */
  view_card?: Array<ViewCardItem>
  /**
   * sheetchoose
   */
  table_columns?: Array<TableColumn>
  /**
   * selectMedium message
   */
  active_msg?: string

  /**
   * ComponentsStyle
   */
  style?: Dict<any>

  /**
   * el-form-item Style
   */
  item_style?: Dict<any>
  /**
   * Table Single calibrationVerification This piecesandelement is the same as Verification
   */
  rules?: Dict<any>
  /**
   * default Not for empty schoolVerificationhint
   */
  err_msg?: string
  /**
   *tabswhenuse
   */
  tabs_label?: string

  [propName: string]: any
}

interface FormField {
  field: string
  /**
   * Input boxType
   */
  input_type: string
  /**
   * hint
   */
  label?: string | any
  /**
   * Yesno Required
   */
  required?: boolean
  /**
   * default value
   */
  default_value?: any
  /**
   * YesNo displaydefault value
   */
  show_default_value?: boolean
  /**
   *  {field:field_value_list} expressIn fieldhavevalue ,and valueInfield_value_listMedium will only display
   */
  relation_show_field_dict?: Dict<Array<any>>
  /**
   * {field:field_value_list} expressIn fieldhavevalue ,And valueInfield_value_listMedium is execution letterNumberget NumberAccording to
   */
  relation_trigger_field_dict?: Dict<any>
  /**
   * ExecutorType  OPTION_LISTaskOption_listNumberAccording to CHILD_FORMSRequest subtableSingle
   */
  trigger_type?: 'OPTION_LIST' | 'CHILD_FORMS'
  /**
   * Front endattrNumberAccording to
   */
  attrs?: Attrs
  /**
   * otherAdditionalinformation
   */
  props_info?: PropsInfo
  /**
   * Drop down selectionFieldsfield
   */
  text_field?: string
  /**
   * Drop down selection value
   */
  value_field?: string
  /**
   * Drop down selectionNumberAccording to
   */
  option_list?: Array<any>
  /**
   * supplier
   */
  provider?: string
  /**
   * execution letterNumber
   */
  method?: string

  children?: Array<FormField>
  required_asterisk?: boolean
  [propName: string]: any
}
export type { FormField }
