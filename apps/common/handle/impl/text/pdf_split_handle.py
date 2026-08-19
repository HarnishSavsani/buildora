# coding=utf-8
"""
@project: maxkb
@Author：Tiger
@file： text_split_handle.py
@date：2024/3/27 18:19
@desc:
"""

import os
import re
import tempfile
import time
import traceback
from typing import List

from django.utils.translation import gettext_lazy as _
from pypdf import PdfReader
from pypdf.generic import Destination

from common.handle.base_split_handle import BaseSplitHandle
from common.utils.logger import maxkb_logger
from common.utils.split_model import SplitModel, smart_split_paragraph

default_pattern_list = [
    re.compile("(?<=^)# .*|(?<=\\n)# .*"),
    re.compile("(?<=\\n)(?<!#)## (?!#).*|(?<=^)(?<!#)## (?!#).*"),
    re.compile("(?<=\\n)(?<!#)### (?!#).*|(?<=^)(?<!#)### (?!#).*"),
    re.compile("(?<=\\n)(?<!#)#### (?!#).*|(?<=^)(?<!#)#### (?!#).*"),
    re.compile("(?<=\\n)(?<!#)##### (?!#).*|(?<=^)(?<!#)##### (?!#).*"),
    re.compile("(?<=\\n)(?<!#)###### (?!#).*|(?<=^)(?<!#)###### (?!#).*"),
    re.compile("(?<!\n)\n\n+"),
]


def check_links_in_pdf(doc):
    for page in doc.pages:
        if PdfSplitHandle.get_internal_links(doc, page):
            return True
    return False


def get_pdf_object(value):
    if hasattr(value, "get_object"):
        return value.get_object()
    return value


class PdfSplitHandle(BaseSplitHandle):
    def handle(
        self,
        file,
        pattern_list: List,
        with_filter: bool,
        limit: int,
        get_buffer,
        save_image,
    ):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            # WillSave uploaded document temporarilydocumentMedium
            for chunk in file.chunks():
                temp_file.write(chunk)
            # getThe path to the temporary document
            temp_file_path = temp_file.name

        try:
            with open(temp_file_path, "rb") as pdf_file:
                pdf_document = PdfReader(pdf_file)
                if type(limit) is str:
                    limit = int(limit)
                if type(with_filter) is str:
                    with_filter = with_filter.lower() == "true"
                # Processingwith catalogpdf
                result = self.handle_toc(pdf_document, limit)
                if result is not None:
                    return {"name": file.name, "content": result}

                # There is no directory but Yes has a link.pdf
                result = self.handle_links(pdf_document, pattern_list, with_filter, limit)
                if result is not None and len(result) > 0:
                    return {"name": file.name, "content": result}

                # There is no directorypdf
                content = self.handle_pdf_content(file, pdf_document)

                if pattern_list is not None and len(pattern_list) > 0:
                    split_model = SplitModel(pattern_list, with_filter, limit)
                else:
                    split_model = SplitModel(default_pattern_list, with_filter=with_filter, limit=limit)
        except BaseException as e:
            maxkb_logger.error(f"File: {file.name}, error: {e}, {traceback.format_exc()}")
            return {"name": file.name, "content": []}
        finally:
            # ProcessingAfter completion, you can delete the temporarydocument
            os.remove(temp_file_path)

        return {"name": file.name, "content": split_model.parse(content)}

    @staticmethod
    def handle_pdf_content(file, pdf_document):
        # Step 1: Collect allCharacter body size
        font_sizes = []
        page_lines = []
        for page in pdf_document.pages:
            lines = PdfSplitHandle.extract_page_lines(page)
            page_lines.append(lines)
            for line_text, font_size in lines:
                if line_text and font_size > 0:
                    font_sizes.append(font_size)

        # Calculate text Character body size(PublicNumber)
        if not font_sizes:
            body_font_size = 12
        else:
            from collections import Counter

            body_font_size = Counter(font_sizes).most_common(1)[0][0]

        # Step 2: Extractcontent
        content = ""
        for page_num, page in enumerate(pdf_document.pages):
            start_time = time.time()

            for text, font_size in page_lines[page_num]:
                if not text:
                    continue

                # RootAccording toJudgment of difference value from text Character font
                size_diff = font_size - body_font_size

                if size_diff > 2:  # Significantly larger than the text
                    content += f"## {text}\n\n"
                elif size_diff > 0.5:  # Slightly larger than the text
                    content += f"### {text}\n\n"
                else:  # text
                    content += f"{text}\n"

            for image_index in range(PdfSplitHandle.get_page_image_count(page)):
                content += f"![image](image_{page_num}_{image_index})\n\n"

            content = content.replace("\0", "")

            elapsed_time = time.time() - start_time
            maxkb_logger.debug(f"File: {file.name}, Page: {page_num + 1}, Time: {elapsed_time:.3f}s")

        return content

    @staticmethod
    def extract_page_lines(page):
        lines = []
        current_text = []
        current_sizes = []

        def flush_line():
            text = "".join(current_text).strip()
            if text:
                font_size = current_sizes[0] if current_sizes else 0
                lines.append((text, font_size))
            current_text.clear()
            current_sizes.clear()

        def visitor_text(text, cm, tm, font_dict, font_size):
            if text is None:
                return
            parts = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
            for index, part in enumerate(parts):
                current_text.append(part)
                if part.strip() and font_size:
                    current_sizes.append(float(font_size))
                if index < len(parts) - 1:
                    flush_line()

        try:
            page.extract_text(visitor_text=visitor_text)
        except BaseException:
            text = PdfSplitHandle.extract_page_text(page)
            return [(line.strip(), 0) for line in text.splitlines() if line.strip()]
        flush_line()
        if lines:
            return lines

        text = page.extract_text() or ""
        return [(line.strip(), 0) for line in text.splitlines() if line.strip()]

    @staticmethod
    def get_page_image_count(page):
        try:
            return len(page.images)
        except BaseException:
            return 0

    @staticmethod
    def extract_page_text(page):
        return (page.extract_text() or "").replace("\0", "")

    @staticmethod
    def get_toc(doc):
        try:
            outline = doc.outline
        except BaseException:
            return []

        toc = []
        PdfSplitHandle.collect_toc(doc, outline, 1, toc)
        return toc

    @staticmethod
    def collect_toc(doc, outline, level, toc):
        for item in outline:
            if isinstance(item, list):
                PdfSplitHandle.collect_toc(doc, item, level + 1, toc)
                continue

            page_number = PdfSplitHandle.get_destination_page_number(doc, item)
            if page_number is None:
                continue

            title = getattr(item, "title", None)
            if title is None and hasattr(item, "get"):
                title = item.get("/Title")
            if title is None:
                title = str(item)
            toc.append(
                (
                    level,
                    str(title).replace("\0", ""),
                    page_number,
                    PdfSplitHandle.get_destination_top(item),
                )
            )

    @staticmethod
    def get_destination_top(destination):
        top = getattr(destination, "top", None)
        try:
            return float(top)
        except (TypeError, ValueError):
            return None

    @staticmethod
    def extract_page_text_by_position(page, top=None, bottom=None):
        if top is None and bottom is None:
            return PdfSplitHandle.extract_page_text(page)

        text_parts = []

        def visitor_text(text, cm, tm, font_dict, font_size):
            if not text:
                return

            # Text matrix coordinates can be relative to a page-level transform.
            # Convert the text origin to PDF user-space coordinates before comparing
            # it with the outline destination's /Top value.
            x = tm[4] if len(tm) > 4 else 0
            y = tm[5] if len(tm) > 5 else 0
            if len(cm) > 5:
                y = x * cm[1] + y * cm[3] + cm[5]

            if top is not None and y > top:
                return
            if bottom is not None and y <= bottom:
                return
            text_parts.append(text)

        try:
            page.extract_text(visitor_text=visitor_text)
        except BaseException:
            return PdfSplitHandle.extract_page_text(page)
        return "".join(text_parts).replace("\0", "")

    @staticmethod
    def remove_leading_title(text, *titles):
        for title in titles:
            title = title.strip()
            if not title:
                continue
            pattern = r"^\s*" + r"\s*".join(re.escape(char) for char in title)
            stripped_text, count = re.subn(pattern, "", text, count=1)
            if count:
                return stripped_text
        return text

    @staticmethod
    def discard_ambiguous_destination_tops(toc):
        position_counts = {}
        for _level, _title, page_number, top in toc:
            if top is not None:
                position = (page_number, top)
                position_counts[position] = position_counts.get(position, 0) + 1

        ambiguous_tops = {top for (_page_number, top), count in position_counts.items() if count > 1}

        return [
            (level, title, page_number, None if top in ambiguous_tops else top)
            for level, title, page_number, top in toc
        ]

    @staticmethod
    def handle_toc(doc, limit):
        # Find the arrival directory
        toc = PdfSplitHandle.get_toc(doc)
        if toc is None or len(toc) == 0:
            return None
        # Some PDF generators assign the same default position to every bookmark
        # on a page. Such coordinates cannot define chapter boundaries, so preserve
        # the title-based behavior for those entries.
        toc = PdfSplitHandle.discard_ambiguous_destination_tops(toc)

        # createNumber group that stores chapter content
        chapters = []

        # Traverse the directory andaccording toChapter extractiontext
        for i, entry in enumerate(toc):
            level, title, start_page, start_top = entry
            chapter_title = title
            # Determine the Finish page number, if Yes, the last piece chapter isarriveDocumentationend
            if i + 1 < len(toc):
                _next_level, next_title, next_start_page, next_top = toc[i + 1]
                # A positioned bookmark can start partway down a page. Include that
                # page and keep only the text above the next bookmark for this chapter.
                end_page = next_start_page if next_top is not None else next_start_page - 1
            else:
                end_page = len(doc.pages) - 1
                next_title = None
                next_start_page = None
                next_top = None
            end_page = max(start_page, end_page)

            # Remove the TitleMedium symbol
            title = PdfSplitHandle.handle_chapter_title(title)

            # Extract the chaptertext content
            chapter_text = ""
            for page_num in range(start_page, end_page + 1):
                page_top = start_top if page_num == start_page else None
                page_bottom = next_top if page_num == next_start_page else None
                text = PdfSplitHandle.extract_page_text_by_position(doc.pages[page_num], page_top, page_bottom)
                text = re.sub(r"(?<!。)\n+", "", text)
                text = re.sub(r"(?<!.)\n+", "", text)

                if page_num == start_page:
                    if start_top is not None:
                        text = PdfSplitHandle.remove_leading_title(text, chapter_title, title)
                    else:
                        idx = text.find(title)
                        if idx > -1:
                            text = text[idx + len(title) :]

                if next_title is not None and next_top is None:
                    handled_next_title = PdfSplitHandle.handle_chapter_title(next_title)
                    idx = text.find(handled_next_title)
                    if idx > -1:
                        text = text[:idx]

                chapter_text += text  # extracttext

            # Null characters are not allowed.
            chapter_text = chapter_text.replace("\0", "")
            # limitTitlelength
            real_chapter_title = chapter_title[:256]
            # limitChapter content length
            if 0 < limit < len(chapter_text):
                split_text = smart_split_paragraph(chapter_text, limit)
                for text in split_text:
                    chapters.append(
                        {"title": real_chapter_title, "content": text.encode("utf-8", "ignore").decode("utf-8")}
                    )
            else:
                chapters.append(
                    {
                        "title": real_chapter_title,
                        "content": (chapter_text if chapter_text else real_chapter_title)
                        .encode("utf-8", "ignore")
                        .decode("utf-8"),
                    }
                )
            # save chaptercontentandChapter title
        return chapters

    @staticmethod
    def handle_links(doc, pattern_list, with_filter, limit):
        # Check DocumentationYes to include internal links
        if not check_links_in_pdf(doc):
            return
        # createNumber group that stores chapter content
        chapters = []
        toc_start_page = -1
        page_content = ""
        handle_pre_toc = True
        # Traverse PDF for each page, find pages with directory links
        for page_num, page in enumerate(doc.pages):
            links = PdfSplitHandle.get_internal_links(doc, page)
            # likeIf the directory Start page number does not have Settings, thenSettingsforCurrent pagecode
            if len(links) > 0 and toc_start_page < 0:
                toc_start_page = page_num
            if toc_start_page < 0:
                page_content += PdfSplitHandle.extract_page_text(page)
            # Check the page Yes or No Include internal links (that is, pages pointing to internal Documentation）
            for num in range(len(links)):
                link = links[num]
                # getLink to Target’s page
                dest_page = link["page"]
                rect = link["from"]  # getlinked rectangular area
                # likeIf the directory Start page number includes the preface, there will be no Processing preface
                if dest_page < toc_start_page:
                    handle_pre_toc = False

                # Extract the text of the link areaforTitle
                link_title = PdfSplitHandle.extract_link_title(page, rect)
                if not link_title:
                    link_title = PdfSplitHandle.extract_first_line(doc.pages[dest_page])
                # Extract the Target page content for the chapterStart
                start_page = dest_page
                end_page = dest_page
                # Nextpieceslink
                next_link = links[num + 1] if num + 1 < len(links) else None
                next_link_title = None
                if next_link is not None:
                    next_link_title = PdfSplitHandle.extract_link_title(page, next_link["from"])
                    if not next_link_title:
                        next_link_title = PdfSplitHandle.extract_first_line(doc.pages[next_link["page"]])
                    end_page = next_link["page"]

                # Extract chapterscontent
                chapter_text = ""
                for p_num in range(start_page, min(end_page, len(doc.pages) - 1) + 1):
                    text = PdfSplitHandle.extract_page_text(doc.pages[p_num])
                    text = re.sub(r"(?<!。)\n+", "", text)
                    text = re.sub(r"(?<!.)\n+", "", text)

                    idx = text.find(link_title)
                    if idx > -1:
                        text = text[idx + len(link_title) :]

                    if next_link_title is not None:
                        idx = text.find(next_link_title)
                        if idx > -1:
                            text = text[:idx]
                    chapter_text += text

                # Null characters are not allowed.
                chapter_text = chapter_text.replace("\0", "")

                # limitChapter content length
                if 0 < limit < len(chapter_text):
                    split_text = smart_split_paragraph(chapter_text, limit)
                    for text in split_text:
                        chapters.append({"title": link_title, "content": text})
                else:
                    # save chapterinformation
                    chapters.append({"title": link_title, "content": chapter_text})

        # Table of contents Medium does not have a preface, manualProcessing
        if handle_pre_toc:
            pre_toc = []
            lines = page_content.strip().split("\n")
            try:
                for line in lines:
                    if re.match(r"^Preface\s*Preface", line):
                        pre_toc.append({"title": line, "content": ""})
                    else:
                        pre_toc[-1]["content"] += line
                for i in range(len(pre_toc)):
                    pre_toc[i]["content"] = re.sub(r"(?<!。)\n+", "", pre_toc[i]["content"])
                    pre_toc[i]["content"] = re.sub(r"(?<!.)\n+", "", pre_toc[i]["content"])
            except BaseException as e:
                maxkb_logger.error(_("This document has no preface and is treated as ordinary text: {e}").format(e=e))
                if pattern_list is not None and len(pattern_list) > 0:
                    split_model = SplitModel(pattern_list, with_filter, limit)
                else:
                    split_model = SplitModel(default_pattern_list, with_filter=with_filter, limit=limit)
                # Insert the part before the directory
                page_content = re.sub(r"(?<!。)\n+", "", page_content)
                page_content = re.sub(r"(?<!.)\n+", "", page_content)
                page_content = page_content.strip()
                pre_toc = split_model.parse(page_content)
            chapters = pre_toc + chapters
        return chapters

    @staticmethod
    def get_internal_links(doc, page):
        links = []
        annotations = getattr(page, "annotations", None) or []
        for annotation in annotations:
            annotation = get_pdf_object(annotation)
            if not hasattr(annotation, "get"):
                continue
            if annotation.get("/Subtype") != "/Link":
                continue
            dest_page = PdfSplitHandle.get_annotation_destination_page_number(doc, annotation)
            if dest_page is None or dest_page < 0 or dest_page >= len(doc.pages):
                continue
            rect = annotation.get("/Rect")
            links.append({"page": dest_page, "from": PdfSplitHandle.normalize_rect(rect)})
        return links

    @staticmethod
    def get_annotation_destination_page_number(doc, annotation):
        destination = annotation.get("/Dest")
        if destination is None:
            action = get_pdf_object(annotation.get("/A"))
            if hasattr(action, "get") and action.get("/S") == "/GoTo":
                destination = action.get("/D")
        return PdfSplitHandle.get_destination_page_number(doc, destination)

    @staticmethod
    def get_destination_page_number(doc, destination):
        if destination is None:
            return None

        destination = get_pdf_object(destination)

        if isinstance(destination, bytes):
            destination = destination.decode(errors="ignore")

        if isinstance(destination, str):
            destination = doc.named_destinations.get(destination)
            if destination is None:
                return None

        if isinstance(destination, Destination):
            try:
                page_number = doc.get_destination_page_number(destination)
                return page_number if page_number >= 0 else None
            except BaseException:
                return None

        if isinstance(destination, (list, tuple)) and len(destination) > 0:
            return PdfSplitHandle.get_page_number_by_reference(doc, destination[0])

        if hasattr(destination, "get") and destination.get("/D") is not None:
            return PdfSplitHandle.get_destination_page_number(doc, destination.get("/D"))

        return None

    @staticmethod
    def get_page_number_by_reference(doc, page_reference):
        try:
            page_number = int(page_reference)
            if 0 <= page_number < len(doc.pages):
                return page_number
        except BaseException:
            pass

        try:
            page = get_pdf_object(page_reference)
            page_number = doc.get_page_number(page)
            return page_number if page_number >= 0 else None
        except BaseException:
            return None

    @staticmethod
    def normalize_rect(rect):
        if rect is None or len(rect) < 4:
            return None
        left, bottom, right, top = [float(value) for value in rect[:4]]
        return min(left, right), min(bottom, top), max(left, right), max(bottom, top)

    @staticmethod
    def extract_link_title(page, rect):
        if rect is None:
            return ""

        left, bottom, right, top = rect
        tolerance = 2
        text_parts = []

        def visitor_text(text, cm, tm, font_dict, font_size):
            if not text:
                return
            x = tm[4] if len(tm) > 4 else 0
            y = tm[5] if len(tm) > 5 else 0
            text_top = y + (float(font_size) if font_size else 0)
            in_horizontal_range = left - tolerance <= x <= right + tolerance
            in_vertical_range = (
                bottom - tolerance <= y <= top + tolerance or bottom - tolerance <= text_top <= top + tolerance
            )
            if in_horizontal_range and in_vertical_range:
                text_parts.append(text)

        try:
            page.extract_text(visitor_text=visitor_text)
        except BaseException:
            return ""

        return "".join(text_parts).replace("\0", "").strip().split("\n")[0].replace(".", "").strip()

    @staticmethod
    def extract_first_line(page):
        text = PdfSplitHandle.extract_page_text(page).strip()
        return text.split("\n")[0].replace(".", "").strip() if text else ""

    @staticmethod
    def handle_chapter_title(title):
        title = title.replace("\0", "")
        title = re.sub(r"[One, two, three, four, five, six, seven, eight, ninety\s*]、\s*", "", title)
        title = re.sub(r"Chapter [1234567890]\s*", "", title)
        return title

    def support(self, file, get_buffer):
        file_name: str = file.name.lower()
        if file_name.endswith(".pdf") or file_name.endswith(".PDF"):
            return True
        return False

    def get_content(self, file, save_image):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            # WillSave uploaded document temporarilydocumentMedium
            temp_file.write(file.read())
            # getThe path to the temporary document
            temp_file_path = temp_file.name

        try:
            with open(temp_file_path, "rb") as pdf_file:
                pdf_document = PdfReader(pdf_file)
                return self.handle_pdf_content(file, pdf_document)
        except BaseException as e:
            traceback.print_exception(e)
            return f"{e}"
        finally:
            os.remove(temp_file_path)
