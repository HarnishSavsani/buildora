/**
 * UsersInput parameter tilingWhitelist
 *
 * only these input_type Fields can be displayed tiled on the Settingsfor external parameter (InChat box）。
 * Changing this will affect 3 piecesConsumer, Noticesynchronous semantics：
 * - UserInputTitleDialog.vue —— Gear pop-up windowMedium select option of disabled Judgment
 * - inline-params/index.vue  —— Perform filtering during rendering to prevent Whitelist from being bypassed
 * - base-node/UserInputFieldTable.vue —— FieldsTypeCleanup when changing/DeletingNumberAccording to
 */
export const ALLOWED_EXPOSED_TYPES = [
  'Model',
  'Knowledge',
  'SwitchInput',
  'DatePicker',
  'TreeSelect',
  'SingleSelect',
  'MultiSelect',
] as const
