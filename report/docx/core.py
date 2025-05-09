from docx.oxml import CT_P
from docx.shared import Pt, Length
from docx.text.run import Run
from docx.document import Document as DocumentType


def add_picture(picture_path: str, run: Run):
    from util.common import get_image_dimensions

    run.clear()
    doc: DocumentType = run._parent._parent._parent

    original_width, original_height = get_image_dimensions(picture_path)
    left_margin = doc.sections[0].left_margin
    right_margin = doc.sections[0].right_margin

    width = Length(doc.sections[0].page_width - left_margin - right_margin)
    height = Length(int((width / original_width) * original_height))

    pic = run.add_picture(picture_path, width=width, height=height)

    # pic.width = width
    # pic.height = height


def add_text(text: str, run: Run):
    run.element.text = ''
    run.element.text = text


def add_document_content_in_end(main_document: DocumentType, data_document: DocumentType):
    main_body = main_document.element.body
    data_body = data_document.element.body
    # в конце документа последним элементом почему-то вставляется лишний пустой параграф,
    # случается только если документ был создан вручную, а не через код

    # так понял последний параграф отвечает за разметку размерности границ документа
    # и если его не убирать он заменяет основные настройки границ и все может сместиться
    children_elements = list(data_body.iterchildren())[:-2]
    for elem in children_elements:
        main_body.append(elem)


def insert_document_content(paragraph_element: CT_P, document: DocumentType):
    data_body = document.element.body
    children_elements = reversed(list(data_body.iterchildren()))
    for elem in children_elements:
        paragraph_element.addnext(elem)
    main_body = paragraph_element.getparent()
    main_body.remove(paragraph_element)

# def add_document_content(run: Run, document: DocumentType):
#     from docx.oxml import CT_P
#     from docx.oxml import CT_Tbl
#
#     run.element.text = ''
#     parent_elm = document.element.body
#     paste_elements = []
#     for child in parent_elm.iterchildren():
#         if isinstance(child, CT_P):
#             result = Paragraph(child, document)
#         elif isinstance(child, CT_Tbl):
#             result = _make_table_from_child_document(child, document)
#         else:
#             continue
#         if result is not None:
#             paste_elements.append(result._element)
#
#     paragraph = run._element.getparent()
#     if isinstance(paragraph, CT_P):
#         adding_element = paragraph
#     else:
#         adding_element = run._r
#     for elem in reversed(paste_elements):
#         adding_element.addnext(elem)


def show_document_structure(document: DocumentType):
    def print_structure(element, indent=0):
        for child in element.iterchildren():
            print('\t' * indent + f"{child.tag.rsplit('}', 1)[-1]}")
            print_structure(child, indent + 1)

    print_structure(document.element.body)

# def delete_line_breaks(document: DocumentType):
#     for paragraph in document.paragraphs:
#         if paragraph.text is not None and paragraph.text.strip():
#             print(f"\t{paragraph.text}")
#         else:
#             print(f"\t{paragraph._element}")
#             for child in paragraph._element.iterchildren():
#                 if child.text is not None and child.text.strip():
#                     print(f"\t{child.text}")
#                 else:
#                     print(f"\t{child}")
#                     for ch_child in child.iterchildren():
#                         if ch_child.text is not None and ch_child.text.strip():
#                             print(f"\t\t{ch_child.text}")
#                         else:
#                             print(f"\t\t{ch_child}")
#                             for ch_ch_child in ch_child.iterchildren():
#                                 if ch_ch_child.text is not None and ch_ch_child.text.strip():
#                                     print(f"\t\t\t{ch_ch_child.text}")
#                                 else:
#                                     print(f"\t\t\t{ch_ch_child}")
#                                     for ch_ch_ch_child in ch_ch_child.iterchildren():
#                                         if ch_ch_ch_child.text is not None and ch_ch_ch_child.text.strip():
#                                             print(f"\t\t\t\t{ch_ch_ch_child.text}")
#                                         else:
#                                             print(f"\t\t\t\t{ch_ch_ch_child}")
#                     # if isinstance(child, CT_P):
#                     #     if not child.text.strip():
#                     #         paragraph._element.remove(child)
