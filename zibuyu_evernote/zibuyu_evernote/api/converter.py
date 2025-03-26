# -*- coding: utf-8 -*-

"""
--------------------------------------------
project: evernote
author: 子不语
date: 2025/3/11
contact: 【公众号】思维兵工厂
description: Converter是一开始的markdown转换方式，打算舍弃
--------------------------------------------
"""

import re
import markdown
from typing import List, Dict

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter
from markdown.preprocessors import Preprocessor
from markdown.extensions import Extension


class Converter(object):

    def __init__(self):
        self.order_item: List[str] = []
        self.unordered_item: List[str] = []

    @staticmethod
    def handle_inline_style(markdown_text):
        """
        将 Markdown 中的加粗、斜体、透明样式替换为 HTML 的 <span> 标签。
        """

        # 先替换加粗
        markdown_text = re.sub(
            r"\*\*(.*?)\*\*",
            r'<strong style="line-height: 160%; box-sizing: content-box; font-weight: 700;">\1</strong>',
            markdown_text
        )

        # 再替换斜体
        markdown_text = re.sub(
            r"(\*|_)(.*?)(\1)",
            r'<em style="line-height: 160%; box-sizing: content-box; font-style: italic;">\2</em>',
            markdown_text
        )

        # 再替换透明
        markdown_text = re.sub(
            r"&&(.*?)&&",
            r'<span textstyle="" style="color: #ffffff; background-color: #ffffff"">\1</span>',
            markdown_text
        )

        return markdown_text

    @staticmethod
    def convert_h1(content: str) -> str:
        return f'<h1 style="line-height: 160%; box-sizing: content-box; font-weight: 700; font-size: 41px; border-bottom: 3px double #999; color: #000; margin-top: 14px;">{content}</h1>'

    @staticmethod
    def convert_h2(content: str) -> str:
        return f'<h2 style="line-height: 160%; box-sizing: content-box; font-weight: 700; font-size: 34px; border-bottom: 1px solid #dbdbdb; color: #333;">{content}</h2>'

    @staticmethod
    def convert_h3(content: str) -> str:
        return f'<h3 style="line-height: 160%; box-sizing: content-box; font-weight: 700; font-size: 27px; color: #333;">{content}</h3>'

    @staticmethod
    def convert_h4(content: str) -> str:
        return f'<h4 style="line-height: 160%; box-sizing: content-box; font-size: 20px; color: #333;">{content}</h4>'

    @staticmethod
    def convert_h5(content: str) -> str:
        return f'<h5 style="line-height: 160%; box-sizing: content-box; font-weight: 700; font-size: 16px; color: #333;">{content}</h5>'

    @staticmethod
    def convert_h6(content: str) -> str:
        return f'<h6 style="line-height: 160%; box-sizing: content-box; font-size: 13px; color: #333;">{content}</h6>'

    @staticmethod
    def convert_p(content: str) -> str:
        return f'<p style="line-height: 160%; box-sizing: content-box; margin: 20px 0; color: #333;">{content}</p>'

    @staticmethod
    def convert_p_lite(content: str) -> str:
        return f'<p style="line-height: 160%; box-sizing: content-box; margin: 20px 0; color: #333;">{content}</p>'

    @staticmethod
    def convert_quote(content: str) -> str:
        return f'''<blockquote style="line-height: 160%; box-sizing: content-box; margin: 15px 0; border-left: 4px solid #ddd; padding: 0 15px; color: #777;">
<p style="line-height: 160%; box-sizing: content-box; margin: 15px 0; color: #333; margin-top: 0; margin-bottom: 0;">{content}</p>
</blockquote>'''

    @staticmethod
    def convert_image(url: str, content: str) -> str:
        return f'<figure style="margin-top: 10px; margin-bottom: 10px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px; display: flex; flex-direction: column; justify-content: center; align-items: center;"><img src="{url}" alt="{content}" style="display: block; margin-top: 0px; margin-right: auto; margin-bottom: 0px; margin-left: auto; max-width: 100%; border-top-style: none; border-bottom-style: none; border-left-style: none; border-right-style: none; border-top-width: 3px; border-bottom-width: 3px; border-left-width: 3px; border-right-width: 3px; border-top-color: rgba(0, 0, 0, 0.4); border-bottom-color: rgba(0, 0, 0, 0.4); border-left-color: rgba(0, 0, 0, 0.4); border-right-color: rgba(0, 0, 0, 0.4); border-top-left-radius: 0px; border-top-right-radius: 0px; border-bottom-right-radius: 0px; border-bottom-left-radius: 0px; object-fit: fill; box-shadow: rgba(0, 0, 0, 0) 0px 0px 0px 0px;"><figcaption style="color: rgb(136, 136, 136); font-size: 14px; line-height: 1.5em; letter-spacing: 0em; text-align: center; font-weight: normal; margin-top: 5px; margin-bottom: 0px; margin-left: 0px; margin-right: 0px; padding-top: 0px; padding-bottom: 0px; padding-left: 0px; padding-right: 0px;">{content}</figcaption></figure>'

    @staticmethod
    def convert_order_list(content: str):
        item_list = [item.split('. ', maxsplit=1)[-1].strip() for item in content.split('\n') if item.strip()]

        new_item_list = []
        for item in item_list:
            new_item_list.append(f'<li style="line-height: 160%; box-sizing: content-box;">{item}</li>')

        item_str = ''.join(new_item_list)

        return f'''<ol style="line-height: 160%; box-sizing: content-box; display: block; padding-left: 30px; margin: 6px 0 10px; color: #333; list-style-type: decimal;">{item_str}</ol>'''

    @staticmethod
    def convert_unordered_list(content: str) -> str:
        item_list = [item.replace('- ', '').strip() for item in content.split('\n') if item.strip()]

        new_item_list = []
        for item in item_list:
            new_item_list.append(
                f'<li style="line-height: 160%; box-sizing: content-box; position: relative;">{item}</li>'
            )

        item_str = ''.join(new_item_list)

        return f'<ul style="line-height: 160%; box-sizing: content-box; display: block; list-style-type: disc; padding-left: 30px; margin: 6px 0 10px; color: #333;">{item_str}</ul>'

    @staticmethod
    def convert_table(content: str) -> str:

        # 分割表格为行
        lines = content.strip().split('\n')

        # 初始化HTML表格
        html_table = '<table style="margin: 2px 0 14px; color: #333; width: auto; border-collapse: collapse; box-sizing: border-box;">\n<thead style="line-height: 160%; box-sizing: content-box;">\n'

        # 处理表头
        header_row = lines[0].strip()
        header_cells = header_row.split('|')
        header_cells = [cell.strip() for cell in header_cells if cell.strip()]
        html_table += '  <tr style="line-height: 160%; box-sizing: content-box;">\n'
        for cell in header_cells:
            html_table += f'<th style="line-height: 160%; box-sizing: content-box;  padding: 5px 14px 5px 12px; border: 1px solid #72777b; border-top: 0; background-color: #7b8184; font-weight: 300; color: #fff; padding-top: 6px;">{cell}</th>\n'
        html_table += '  </tr>\n'
        html_table += '  </thead>\n'
        html_table += '<tbody style="line-height: 160%; box-sizing: content-box;">\n'

        # 处理分隔行（用于确定对齐方式）
        separator_row = lines[1].strip()
        separator_cells = separator_row.split('|')
        alignments = []
        for cell in separator_cells:
            cell = cell.strip()
            if cell.startswith(':') and cell.endswith(':'):
                alignments.append('center')
            elif cell.startswith(':'):
                alignments.append('left')
            elif cell.endswith(':'):
                alignments.append('right')
            else:
                alignments.append('left')

        # 处理数据行
        for line in lines[2:]:
            data_row = line.strip()
            data_cells = data_row.split('|')
            data_cells = [cell.strip() for cell in data_cells if cell.strip()]

            html_table += '<tr style="line-height: 160%; box-sizing: content-box;">'
            for i, cell in enumerate(data_cells):
                align = alignments[i]
                html_table += f'<td style="line-height: 160%; box-sizing: content-box;  padding: 5px 14px 5px 12px; border: 1px solid #eaeaea;">{cell}</td>'

            html_table += '  </tr>\n'

        html_table += '</tbody>'
        html_table += '</table>'

        return html_table

    @property
    def split_line(self):
        return '<hr style="line-height: 160%; box-sizing: content-box; border-top: 1px solid #eee; margin: 16px 0;"/>'

    def convert(self, markdown_content: str, result_dict: dict) -> str:

        if not markdown_content:
            return ""

        if not isinstance(markdown_content, str):
            return ""

        html_content = ""
        lines = markdown_content.split('\n')

        i = 0
        while i < len(lines):

            line = self.handle_inline_style(lines[i])
            image_pattern = r'!\[(.*?)\]\((.*?)\)'
            # 查找所有匹配的图片
            matches = re.findall(image_pattern, line)
            if matches:

                for name, path in matches:
                    if name not in result_dict:
                        continue

                    data_dict = result_dict[name]
                    html_content += data_dict['image_obj'].final_content

            # 处理标题
            elif line.startswith("# "):
                html_content += self.convert_h1(line[2:])
            elif line.startswith("## "):
                html_content += self.convert_h2(line[3:])
            elif line.startswith("### "):
                html_content += self.convert_h3(line[4:])
            elif line.startswith("#### "):
                html_content += self.convert_h4(line[5:])
            elif line.startswith("##### "):
                html_content += self.convert_h5(line[6:])
            elif line.startswith("###### "):
                html_content += self.convert_h6(line[7:])

            # 处理颜色段落
            elif line.startswith("@l "):
                html_content += self.convert_p_lite(line[3:])

            # 处理引用
            elif line.startswith("> "):
                html_content += self.convert_quote(line[2:])

            elif line.strip() == '---':
                html_content += self.split_line

            # 处理图片
            elif re.match(r'!\[.*\]\(.*\)', line):
                match = re.match(r'!\[(.*)\]\((.*)\)', line)
                alt_text = match.group(1)
                url = match.group(2)
                html_content += self.convert_image(url, alt_text)

            # 处理有序列表
            elif re.match(r'^\d+\. ', line.strip()):  # 匹配以数字加 `.` 开头的行
                ordered_list_content = ""
                while i < len(lines) and re.match(r'^\d+\. ', lines[i].strip()):
                    ordered_list_content += lines[i].strip() + "\n"
                    i += 1
                html_content += self.convert_order_list(ordered_list_content.strip())
                i -= 1

            # 处理无序列表
            elif line.strip().startswith(("- ", "* ", "+ ")):
                unordered_list_content = ""
                while i < len(lines) and lines[i].strip().startswith(("- ", "* ", "+ ")):
                    unordered_list_content += lines[i].strip() + "\n"
                    i += 1
                html_content += self.convert_unordered_list(unordered_list_content.strip())
                i -= 1

            # 处理表格
            elif line.strip().startswith("|"):
                table_content = ""
                while i < len(lines) and lines[i].strip().startswith("|"):
                    table_content += lines[i].strip() + "\n"
                    i += 1
                html_content += self.convert_table(table_content.strip())
                i -= 1

            # 处理段落
            elif line.strip() == "" and html_content and not html_content.endswith("<br>"):
                html_content += "<br></br>"
            elif line.strip() != "":
                html_content += self.convert_p(line)
            i += 1

        return f'<!DOCTYPE en-note SYSTEM \'http://xml.evernote.com/pub/enml2.dtd\'><en-note>{html_content}</en-note>'


class CustomStyle:
    @staticmethod
    def convert_h1(content: str) -> str:
        return f'<h1 style="line-height: 160%; box-sizing: content-box; font-weight: 700; font-size: 41px; border-bottom: 3px double #999; color: #000; margin-top: 14px;">{content}</h1>'

    @staticmethod
    def convert_h2(content: str) -> str:
        return f'<h2 style="line-height: 160%; box-sizing: content-box; font-weight: 700; font-size: 34px; border-bottom: 1px solid #dbdbdb; color: #333;">{content}</h2>'

    @staticmethod
    def convert_h3(content: str) -> str:
        return f'<h3 style="line-height: 160%; box-sizing: content-box; font-weight: 700; font-size: 27px; color: #333;">{content}</h3>'

    @staticmethod
    def convert_h4(content: str) -> str:
        return f'<h4 style="line-height: 160%; box-sizing: content-box; font-size: 20px; color: #333;">{content}</h4>'

    @staticmethod
    def convert_h5(content: str) -> str:
        return f'<h5 style="line-height: 160%; box-sizing: content-box; font-weight: 700; font-size: 16px; color: #333;">{content}</h5>'

    @staticmethod
    def convert_h6(content: str) -> str:
        return f'<h6 style="line-height: 160%; box-sizing: content-box; font-size: 13px; color: #333;">{content}</h6>'

    @staticmethod
    def convert_p(content: str) -> str:
        return f'<p style="line-height: 160%; box-sizing: content-box; margin: 20px 0; color: #333;">{content}</p>'

    @staticmethod
    def convert_quote(content: str) -> str:
        return (
            f'<blockquote style="line-height: 160%; box-sizing: content-box; margin: 15px 0; '
            f'border-left: 4px solid #ddd; padding: 0 15px; color: #777;">'
            f'<p style="line-height: 160%; box-sizing: content-box; margin: 15px 0; color: #333; margin-top: 0; margin-bottom: 0;">{content}</p>'
            f'</blockquote>'
        )

    @staticmethod
    def convert_order_list(content: str) -> str:
        # 处理每一行形如 "1. 内容"
        item_list = [item.split('. ', maxsplit=1)[-1].strip() for item in content.split('\n') if item.strip()]
        new_item_list = []
        for item in item_list:
            new_item_list.append(f'<li style="line-height: 160%; box-sizing: content-box;">{item}</li>')
        item_str = ''.join(new_item_list)
        return (
            f'<ol style="line-height: 160%; box-sizing: content-box; display: block; padding-left: 30px; '
            f'margin: 6px 0 10px; color: #333; list-style-type: decimal;">{item_str}</ol>'
        )

    @staticmethod
    def convert_unordered_list(content: str) -> str:
        # 处理每一行形如 "- 内容"
        item_list = [item.replace('- ', '').strip() for item in content.split('\n') if item.strip()]
        new_item_list = []
        for item in item_list:
            new_item_list.append(
                f'<li style="line-height: 160%; box-sizing: content-box; position: relative;">{item}</li>'
            )
        item_str = ''.join(new_item_list)
        return (
            f'<ul style="line-height: 160%; box-sizing: content-box; display: block; list-style-type: disc; '
            f'padding-left: 30px; margin: 6px 0 10px; color: #333;">{item_str}</ul>'
        )

    @staticmethod
    def convert_table(content: str) -> str:
        # 将 Markdown 表格文本转换为 HTML 表格
        lines = content.strip().split('\n')
        html_table = (
            '<table style="margin: 2px 0 14px; color: #333; width: auto; border-collapse: collapse; '
            'box-sizing: border-box;">\n<thead style="line-height: 160%; box-sizing: content-box;">\n'
        )
        # 表头
        header_row = lines[0].strip()
        header_cells = [cell.strip() for cell in header_row.split('|') if cell.strip()]
        html_table += '  <tr style="line-height: 160%; box-sizing: content-box;">\n'
        for cell in header_cells:
            html_table += (
                f'<th style="line-height: 160%; box-sizing: content-box; padding: 5px 14px 5px 12px; '
                f'border: 1px solid #72777b; border-top: 0; background-color: #7b8184; '
                f'font-weight: 300; color: #fff; padding-top: 6px;">{cell}</th>\n'
            )
        html_table += '  </tr>\n</thead>\n<tbody style="line-height: 160%; box-sizing: content-box;">\n'

        # 分隔行：用于确定对齐方式
        separator_row = lines[1].strip()
        separator_cells = separator_row.split('|')
        alignments = []
        for cell in separator_cells:
            cell = cell.strip()
            if cell.startswith(':') and cell.endswith(':'):
                alignments.append('center')
            elif cell.startswith(':'):
                alignments.append('left')
            elif cell.endswith(':'):
                alignments.append('right')
            else:
                alignments.append('left')

        # 数据行
        for line in lines[2:]:
            data_cells = [cell.strip() for cell in line.strip().split('|') if cell.strip()]
            html_table += '<tr style="line-height: 160%; box-sizing: content-box;">'
            for i, cell in enumerate(data_cells):
                align = alignments[i] if i < len(alignments) else 'left'
                html_table += (
                    f'<td style="line-height: 160%; box-sizing: content-box; padding: 5px 14px 5px 12px; '
                    f'border: 1px solid #eaeaea; text-align: {align};">{cell}</td>'
                )
            html_table += '</tr>\n'
        html_table += '</tbody>\n</table>'
        return html_table

    @staticmethod
    def convert_image(line: str) -> str:
        """
        将 Markdown 图片语法转换为 HTML 图片标签，保持默认样式
        """
        # m = re.match(r'!\[(.*?)\]\((.*?)\)', line.strip())
        # if m:
        #     alt = m.group(1)
        #     src = m.group(2)
        #     # 这里可根据需要增加 title 或其它属性
        #     return f'<img alt="{alt}" src="{src}" />'
        # return line
        return line

    @property
    def split_line(self) -> str:
        return '<hr style="line-height: 160%; box-sizing: content-box; border-top: 1px solid #eee; margin: 16px 0;"/>'


class CodeHilitePreprocessor(Preprocessor):
    def __init__(self, md):
        super().__init__(md)
        self.code_block_re = re.compile(r'^```(\w*)\s*$')

    def run(self, lines):
        new_lines = []
        in_code_block = False
        code_lines = []
        language = None

        while lines:
            line = lines.pop(0)
            code_start = self.code_block_re.match(line)
            if code_start:
                if in_code_block:
                    lexer = get_lexer_by_name(language) if language else None
                    formatter = HtmlFormatter(noclasses=True, style='default')
                    code_content = '\n'.join(code_lines).replace(' ', 'nbsp;')
                    highlighted = highlight(code_content, lexer, formatter)
                    # 将生成的 HTML 通过 htmlStash 存储
                    new_lines.append(self.md.htmlStash.store(highlighted.replace('nbsp;', '&nbsp;')))
                    in_code_block = False
                    code_lines = []
                    language = None
                else:
                    in_code_block = True
                    language = code_start.group(1).strip() or None
            elif in_code_block:
                code_lines.append(line)
            else:
                new_lines.append(line)

        return new_lines


class CustomStylePreprocessor(Preprocessor):
    img_html_pattern = r'<img\s+(?:[^>]*?\s+)?src="([^"]+)"\s+(?:[^>]*?\s+)?alt="([^"]+)"\s*[^>]*?>'

    def run(self, lines):
        new_lines = []
        i = 0
        paragraph_buffer = []

        def flush_paragraph():
            nonlocal paragraph_buffer
            if paragraph_buffer:
                content = " ".join(paragraph_buffer).strip()
                # 通过 htmlStash 存储段落 HTML
                new_lines.append(self.md.htmlStash.store(CustomStyle.convert_p(content)))
                paragraph_buffer.clear()

        while i < len(lines):
            line = lines[i]

            # 检测图片语法，不做自定义处理，而是转换为默认的 HTML 图片标签
            if re.match(r'!\[.*\]\(.*\)', line.strip()) or re.match(self.img_html_pattern, line.strip()):
                flush_paragraph()
                new_lines.append(self.md.htmlStash.store(CustomStyle.convert_image(line)))
                i += 1
                continue

            if not line.strip():
                flush_paragraph()
                new_lines.append('')
                i += 1
                continue

            # 处理标题
            heading_match = re.match(r'^(#{1,6})\s*(.+)$', line)
            if heading_match:
                flush_paragraph()
                level = len(heading_match.group(1))
                content = heading_match.group(2)
                if level == 1:
                    new_lines.append(self.md.htmlStash.store(CustomStyle.convert_h1(content)))
                elif level == 2:
                    new_lines.append(self.md.htmlStash.store(CustomStyle.convert_h2(content)))
                elif level == 3:
                    new_lines.append(self.md.htmlStash.store(CustomStyle.convert_h3(content)))
                elif level == 4:
                    new_lines.append(self.md.htmlStash.store(CustomStyle.convert_h4(content)))
                elif level == 5:
                    new_lines.append(self.md.htmlStash.store(CustomStyle.convert_h5(content)))
                else:
                    new_lines.append(self.md.htmlStash.store(CustomStyle.convert_h6(content)))
                i += 1
                continue

            # 处理引用
            if line.startswith('>'):
                flush_paragraph()
                quote_lines = []
                while i < len(lines) and lines[i].startswith('>'):
                    quote_lines.append(lines[i][1:].strip())
                    i += 1
                content = "<br>".join(quote_lines)
                new_lines.append(self.md.htmlStash.store(CustomStyle.convert_quote(content)))
                continue

            # 处理有序列表
            if re.match(r'^\d+\.\s+', line):
                flush_paragraph()
                list_lines = []
                while i < len(lines) and re.match(r'^\d+\.\s+', lines[i]):
                    list_lines.append(lines[i])
                    i += 1
                content = "\n".join(list_lines)
                new_lines.append(self.md.htmlStash.store(CustomStyle.convert_order_list(content)))
                continue

            # 处理无序列表
            if line.startswith('- '):
                flush_paragraph()
                list_lines = []
                while i < len(lines) and lines[i].startswith('- '):
                    list_lines.append(lines[i])
                    i += 1
                content = "\n".join(list_lines)
                new_lines.append(self.md.htmlStash.store(CustomStyle.convert_unordered_list(content)))
                continue

            # 处理表格（简单检测含 "|" 且下一行为分隔符的情况）
            if '|' in line and i + 1 < len(lines) and re.match(r'^\s*\|?[\s:-]+\|', lines[i + 1]):
                flush_paragraph()
                table_lines = []
                while i < len(lines) and '|' in lines[i]:
                    table_lines.append(lines[i])
                    i += 1
                content = "\n".join(table_lines)
                new_lines.append(self.md.htmlStash.store(CustomStyle.convert_table(content)))
                continue

            # 处理分割线
            if re.match(r'^(---|\*\*\*|___)\s*$', line):
                flush_paragraph()
                new_lines.append(self.md.htmlStash.store(CustomStyle().split_line))
                i += 1
                continue

            # 其他内容加入段落
            paragraph_buffer.append(line.strip())
            i += 1

        flush_paragraph()
        return new_lines


class CustomMarkdownExtension(Extension):
    def extendMarkdown(self, md):
        md.preprocessors.register(CodeHilitePreprocessor(md), 'codehilite', 30)
        md.preprocessors.register(CustomStylePreprocessor(md), 'customstyle', 25)


def handle_inline_style(markdown_text: str) -> str:
    """
    将 Markdown 中的加粗、斜体、透明样式替换为 HTML 的 <span> 标签。
    """

    # 先替换加粗
    markdown_text = re.sub(
        r"\*\*(.*?)\*\*",
        r'<strong style="line-height: 160%; box-sizing: content-box; font-weight: 700;">\1</strong>',
        markdown_text
    )

    # 再替换斜体
    markdown_text = re.sub(
        r"(\*|_)(.*?)(\1)",
        r'<em style="line-height: 160%; box-sizing: content-box; font-style: italic;">\2</em>',
        markdown_text
    )

    # 再替换透明
    markdown_text = re.sub(
        r"&&(.*?)&&",
        r'<span textstyle="" style="color: #ffffff; background-color: #ffffff"">\1</span>',
        markdown_text
    )

    return markdown_text


def md_to_html(md_text) -> str:
    """
    将 Markdown 格式内容转换为 HTML，并对代码块进行语法着色（使用内联样式），
    同时将代码块中的空格替换为&nbsp;以防止浏览器连续空格被忽略。
    """

    md = markdown.Markdown(extensions=[CustomMarkdownExtension()])
    html = md.convert(handle_inline_style(md_text))
    return html
