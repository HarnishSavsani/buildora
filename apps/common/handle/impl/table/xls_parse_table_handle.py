# coding=utf-8
import logging
import traceback

import xlrd

from common.handle.base_parse_table_handle import BaseParseTableHandle
from common.utils.logger import maxkb_logger


class XlsParseTableHandle(BaseParseTableHandle):
    def support(self, file, get_buffer):
        file_name: str = file.name.lower()
        buffer = get_buffer(file)
        if file_name.endswith(".xls") and xlrd.inspect_format(content=buffer):
            return True
        return False

    def handle(self, file, get_buffer, save_image):
        buffer = get_buffer(file)
        try:
            wb = xlrd.open_workbook(file_contents=buffer, formatting_info=True)
            result = []
            sheets = wb.sheets()
            for sheet in sheets:
                # getMerge SingleYuan formatRangeinformation
                merged_cells = sheet.merged_cells
                data = []
                paragraphs = []
                # getThe first line is the forTitle line
                headers = [sheet.cell_value(0, col_idx) for col_idx in range(sheet.ncols)]
                # Traverse each line from the second line Start (skip the Title line）
                for row_idx in range(1, sheet.nrows):
                    row_data = {}
                    for col_idx in range(sheet.ncols):
                        cell_value = sheet.cell_value(row_idx, col_idx)

                        # Check Yes or No for empty SingleYuan format, like if for empty Check Yes or No In merge areaMedium
                        if cell_value == "":
                            # Check whether the currentSingleYuan format Yes is in the merge area
                            for (rlo, rhi, clo, chi) in merged_cells:
                                if rlo <= row_idx < rhi and clo <= col_idx < chi:
                                    # useThe upper left corner of the merged area SingleYuanvalue
                                    cell_value = sheet.cell_value(rlo, clo)
                                    break

                        # WillTitleAs the for key, the SingleYuan value is used as forvalue and stored in the Character dictionary.
                        row_data[headers[col_idx]] = cell_value
                    data.append(row_data)

                for row in data:
                    row_output = "; ".join([f"{key}: {value}" for key, value in row.items()])
                    # print(row_output)
                    paragraphs.append({'title': '', 'content': row_output})

                result.append({'name': sheet.name, 'paragraphs': paragraphs})

        except BaseException as e:
            maxkb_logger.error(f"Error processing XLS file {file.name}: {e}, {traceback.format_exc()}")
            return [{'name': file.name, 'paragraphs': []}]
        return result

    def get_content(self, file, save_image):
        # Open .xls document
        try:
            workbook = xlrd.open_workbook(file_contents=file.read(), formatting_info=True)
            sheets = workbook.sheets()
            md_tables = ''
            for sheet in sheets:
                # filter blanksheet
                if sheet.nrows == 0 or sheet.ncols == 0:
                    continue

                # getHeaderandcontent
                headers = sheet.row_values(0)
                data = [sheet.row_values(row_idx) for row_idx in range(1, sheet.nrows)]

                # Build Markdown sheet
                md_table = '| ' + ' | '.join(headers) + ' |\n'
                md_table += '| ' + ' | '.join(['---'] * len(headers)) + ' |\n'
                for row in data:
                    # WillThe content of each pieceSingleYuan Medium replaces the newline characterfor <br> to retain the originalFormat
                    md_table += '| ' + ' | '.join(
                        [str(cell)
                         .replace('\r\n', '<br>')
                         .replace('\n', '<br>')
                         if cell else '' for cell in row]) + ' |\n'
                md_tables += md_table + '\n\n'

            return md_tables
        except Exception as e:
            maxkb_logger.error(f'excel split handle error: {e}')
            return f'error: {e}'
