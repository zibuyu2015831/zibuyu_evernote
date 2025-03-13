# -*- coding: utf-8 -*-

"""
--------------------------------------------
project: python_test
author: 子不语
date: 2025/3/12
contact: 【公众号】思维兵工厂
description: 最顶层封装各类调用
--------------------------------------------
"""

import re
import os
import hashlib
import binascii
import requests

from typing import Optional, Dict, List

import html2text

from ..edam.error.ttypes import EDAMUserException, EDAMErrorCode
from .ttypes import ImageItem
from .converter import md_to_html
from .client import EvernoteClient
from ..edam.type.ttypes import Note, Notebook, Data, Resource, Tag
from ..edam.notestore import ttypes as note_store_types
from ..edam.userstore import constants as UserStoreConstants


class BaseEvernote(object):
    def __init__(self, auth_token: str, sandbox: bool = False, china: bool = True):
        self.auth_token = auth_token
        self.sandbox: bool = sandbox
        self.china: bool = china

        self._user_store = None
        self._note_store = None
        self._html2md = None

        self._client: Optional[EvernoteClient] = None

    @property
    def html2md(self):
        if not self._html2md:
            self._html2md = html2text.HTML2Text()

        return self._html2md

    @property
    def client(self) -> EvernoteClient:
        if not self._client:
            self._client = EvernoteClient(
                token=self.auth_token,
                sandbox=self.sandbox,
                china=self.china
            )

        return self._client

    @property
    def user_store(self):

        if not self._user_store:
            self._user_store = self.client.get_user_store()

        return self._user_store

    @property
    def note_store(self):
        if not self._note_store:
            self._note_store = self.client.get_note_store()
        return self._note_store

    def if_version_ok(self) -> bool:
        """ 检查API版本是否可用 """

        return bool(
            self.user_store.checkVersion(
                "Evernote EDAMTest (Python)",
                UserStoreConstants.EDAM_VERSION_MAJOR,
                UserStoreConstants.EDAM_VERSION_MINOR
            )
        )


class NotebooksManager(BaseEvernote):
    def get_all_notebooks(self) -> List[Notebook]:
        """获取所有的笔记本"""
        return self.note_store.listNotebooks()

    def list_notebooks(self, notebook_guid: str) -> List[note_store_types.NoteMetadata]:
        """遍历某个笔记本下的所有笔记"""

        # 创建 NoteFilter
        note_filter = note_store_types.NoteFilter()
        note_filter.notebookGuid = notebook_guid  # 指定笔记本的 GUID

        # 设置 NotesMetadataResultSpec（指定返回的笔记元数据）
        result_spec = note_store_types.NotesMetadataResultSpec(includeTitle=True, includeContentLength=True)

        # 分页获取笔记列表
        offset = 0
        page_size = 50  # 每页最多获取 50 条笔记
        note_objs: List[note_store_types.NoteMetadata] = []
        while True:
            # 获取当前页的笔记列表
            notes_metadata_list = self.note_store.findNotesMetadata(note_filter, offset, page_size, result_spec)
            note_objs.extend(notes_metadata_list.notes)
            # 检查是否还有更多笔记
            if len(notes_metadata_list.notes) < page_size:
                break

            # 更新偏移量
            offset += page_size
        return note_objs

    def create_notebook(self, notebook_name: str, catalog: str = '') -> Notebook:
        """
        创建笔记本
        :param notebook_name: 笔记本名称
        :param catalog: 笔记本分类
        :return:
        """
        notebook = Notebook()
        notebook.name = notebook_name
        notebook.stack = catalog
        return self.note_store.createNotebook(notebook)

    def update_notebook(self, notebook: Notebook):
        return self.note_store.updateNotebook(notebook)

    def get_default_notebook(self):
        return self.note_store.getDefaultNotebook()

    def get_notebook(self, notebook_guid: str) -> Optional[Notebook]:
        """获取笔记本"""

        if not notebook_guid:
            return None

        return self.note_store.getNotebook(notebook_guid)


class NotesManager(BaseEvernote):

    @staticmethod
    def is_url(path) -> bool:
        # 常见的URL协议
        url_protocols = ['http://', 'https://']

        # 检查路径是否以URL协议开头
        return any(path.startswith(protocol) for protocol in url_protocols)

    @staticmethod
    def get_image_data(item: ImageItem) -> bytes:
        try:

            if item.is_url:
                response = requests.get(item.image_path)
                if not response.status_code == 200:
                    return b''
                return response.content
            else:
                if not os.path.exists(item.image_path):
                    return b''

                with open(item.image_path, 'rb') as f:
                    return f.read()
        except:
            return b''

    @staticmethod
    def markdown_to_html(markdown_content: str, result_dict: dict) -> str:

        html = md_to_html(markdown_content)

        if not html:
            return ''

        html = html.replace('class="highlight"', '').replace('<br>', '<br/>')

        lines = html.split('\n')
        new_line = []
        for line in lines:

            strip_line = line.strip().replace('<p>', '').replace('</p>', '')
            if strip_line in result_dict:
                data_dict = result_dict[strip_line]
                new_line.append(data_dict['image_obj'].final_content)
                continue

            new_line.append(line)
            continue

        final_content = '\n'.join(new_line)
        return f"<!DOCTYPE en-note SYSTEM \'http://xml.evernote.com/pub/enml2.dtd\'><en-note>{final_content}</en-note>"

    def extract_images_from_markdown(self, markdown_content, dir_name: str = '') -> List[ImageItem]:
        md_image_pattern = r'!\[(.*?)\]\((.*?)\)'
        html_pattern = r'<img\s+(?:[^>]*?\s+)?src="([^"]+)"\s+(?:[^>]*?\s+)?alt="([^"]+)"\s*[^>]*?>'

        # 查找所有匹配的图片
        md_matches = re.finditer(md_image_pattern, markdown_content)
        html_matches = re.finditer(html_pattern, markdown_content)

        md_matches = [(md_match.group(0), md_match.group(1), md_match.group(2)) for md_match in md_matches]
        html_matches = [(md_match.group(0), md_match.group(2), md_match.group(1)) for md_match in html_matches]

        total_matches = list(md_matches) + list(html_matches)

        result = []

        for md_match in total_matches:
            original, name, path = md_match

            image_suffix = path.rsplit('.')[-1]

            if image_suffix not in ['png', 'jpg', 'jpeg', 'gif', 'bmp', 'svg', 'webp']:
                image_suffix = 'png'

            if self.is_url(path):
                image_obj = ImageItem(
                    image_name=name,
                    image_path=path,
                    original_text=original,
                    is_url=True,
                    image_suffix=image_suffix
                )
            else:
                image_obj = ImageItem(
                    image_name=name,
                    original_text=original,
                    image_path=path if os.path.isabs(path) else os.path.join(dir_name, path),
                    is_url=False,
                    image_suffix=image_suffix
                )
            result.append(image_obj)

        # 将结果存储为字典，键为图片名称，值为图片路径
        return result

    def check_image(self, markdown_content: str, dir_name: str = '') -> Dict:
        result = dict()

        images: List[ImageItem] = self.extract_images_from_markdown(markdown_content, dir_name)

        if not images:
            return result

        resource_list = []
        for image_obj in images:
            image_data: bytes = self.get_image_data(image_obj)

            if not image_data:
                continue

            md5 = hashlib.md5()
            md5.update(image_data)
            hash_bytes = md5.digest()

            data = Data()
            data.size = len(image_data)
            data.bodyHash = hash_bytes
            data.body = image_data

            hash_hex = binascii.hexlify(hash_bytes)
            hash_str = hash_hex.decode("UTF-8")
            image_obj.hash_str = hash_str
            image_obj.final_content = f'<div><en-media type="image/{image_obj.image_suffix}" hash="{hash_str}"/></div>'

            resource = Resource()
            resource.mime = f'image/{image_obj.image_suffix}'
            resource.data = data

            result[image_obj.original_text] = {
                'resource_obj': resource,
                "image_obj": image_obj
            }
            resource_list.append(resource)

        result['resource_list'] = resource_list
        return result

    def get_note(
            self,
            note_guid: str,
            with_content: bool = True,
            with_resources_data: bool = True,
            with_resources_recognition: bool = False,
            with_resources_alternate_data: bool = False
    ) -> Note:

        return self.note_store.getNote(
            note_guid,
            with_content,
            with_resources_data,
            with_resources_recognition,
            with_resources_alternate_data
        )

    def create_note(
            self,
            title: str,
            markdown_content: str = '',
            markdown_file_path: str = '',
    ) -> Note:
        """创建笔记"""

        if markdown_file_path and os.path.exists(markdown_file_path):

            dir_name = os.path.dirname(markdown_file_path)
            with open(markdown_file_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()
        else:
            dir_name = ''

        if not markdown_content:
            raise ValueError('markdown_content and markdown_file_path cannot be both empty')

        result_dict = self.check_image(markdown_content, dir_name)

        note = Note()
        note.title = title
        note.resources = result_dict.get('resource_list', [])

        note.content = self.markdown_to_html(markdown_content, result_dict)

        return self.note_store.createNote(note)

    def download_note(self, note_guid: str, save_path: str) -> bool:

        if not os.path.isdir(save_path):
            return False

        note_obj = self.note_store.getNote(note_guid, True, False, False, False)

        if not note_obj.resources:
            return False

        html_content = note_obj.content

        file_name = note_obj.title if note_obj.title and note_obj.title.endswith('.md') else f"{note_obj.title}.md"
        file_path = os.path.join(save_path, file_name)
        if not note_obj.resources:
            pass

        assets_path = os.path.join(save_path, 'assets', note_obj.title)
        os.makedirs(assets_path, exist_ok=True)

        for resource in note_obj.resources:

            suffix = resource.mime.split('/', maxsplit=1)[-1]
            resource_path = os.path.join(assets_path, f"{resource.guid}.{suffix}")
            resource_obj = self.note_store.getResource(resource.guid, True, False, False, False)
            resource_data = resource_obj.data.body
            if not resource_data:
                continue

            with open(resource_path, 'wb') as image_file:
                image_file.write(resource_data)

            body_hash_hex = resource.data.bodyHash.hex()
            if resource.mime.startswith('image'):
                old_content = f'<en-media type="{resource.mime}" hash="{body_hash_hex}"/>'
                new_content = f'![{resource.guid}](assets/{note_obj.title}/{resource.guid}.{suffix})'
                html_content = html_content.replace(old_content, new_content)

        markdown_content = self.html2md.handle(html_content)

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        return True

    def update_note_tags(
            self,
            tag_names: List[str],
            note_guid: str = '',
            note_obj: Note = None,
    ) -> bool:

        if not note_obj and not note_guid:
            return False

        if not note_obj or not isinstance(note_obj, Note):
            note_obj = self.note_store.getNote(note_guid, True, False, False, False)

        if not note_obj:
            return False

        if not note_obj.tagGuids:
            note_obj.tagGuids = []

        for tag_name in tag_names:

            tag = Tag()
            tag.name = tag_name
            try:
                tag = self.note_store.createTag(tag)
            except EDAMUserException as e:
                if e.errorCode == EDAMErrorCode.DATA_CONFLICT:
                    # 标签已存在，获取现有标签
                    tags = self.note_store.listTags()
                    for t in tags:
                        if t.name == tag_name:
                            tag = t
                            break

            # 添加标签到笔记
            if tag.guid not in note_obj.tagGuids:
                note_obj.tagGuids.append(tag.guid)

        self.note_store.updateNote(note_obj)
        return True


class TagsManager(BaseEvernote):
    def list_tags(self) -> List[Tag]:
        """罗列所有的标签"""
        return self.note_store.listTags()

    def create_tag(self, tag_name: str):
        """创建一个标签"""
        self.note_store.createTag(Tag(name=tag_name))


class MyEvernote(NotebooksManager, NotesManager, TagsManager):
    pass
