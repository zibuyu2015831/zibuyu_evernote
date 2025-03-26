# 子不语个人工具包-evernote

印象笔记的官方SDK年久失修，虽然也能使用，但却得搭配旧版本的Python；

且由于早期的Python风格问题，整个代码没有类型注解和编码提示；

这个版本是我自己对一些常用功能进行的封装，方便使用。

## 安装

```bash
pip install zibuyu-evernote
```

## 新增功能

- 增加了markdown与印象笔记的转换功能；

## 示例代码

```python
from zibuyu_evernote import MyEvernote

my_evernote = MyEvernote(
    auth_token="xxx",  # 从官网获取token
    sandbox=False,  # 是否为沙盒测试环境
    china=True,  # 是否为中国区
)

markdown_content = """
# 样式笔记

## 二级标题

### 三级标题

- 无序列表1
- 无序列表2
"""

result = my_evernote.create_note(
    title="测试笔记",
    markdown_content=markdown_content,
)

print(result)
```