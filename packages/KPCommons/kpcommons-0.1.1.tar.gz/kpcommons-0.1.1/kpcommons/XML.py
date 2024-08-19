import re
from typing import Tuple
from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from kpcommons.Util import get_namespace


INDIRECT_QUOTE = '\u03B1'


def get_text_from_element(file_path: str):
    """

    :param file_path:
    :return: The text
    """
    root = ElementTree.parse(file_path).getroot()
    ns = get_namespace(root.tag)
    body_content = root.find(f'.//{ns}body')

    result, _ = __get_text_from_element(ns, body_content, True, False, [])

    result = result.strip()
    result = re.sub(' +', ' ', result, flags=re.DOTALL)
    result = re.sub(' \n', '\n', result, flags=re.DOTALL)
    return result

def __get_text_from_element(ns: str, element: Element, is_first_head: bool, use_tail: bool, stack) -> Tuple[str, bool]:
    result: str = ''

    if element.tag == f'{ns}div':
        div_type = element.attrib.get('type')
        stack.append(div_type)
    elif element.tag == f'{ns}note':
        note_type = element.attrib.get('type')
        stack.append(note_type)
    elif element.tag == f'{ns}q':
        quote_type = element.attrib.get('type')

        if quote_type == 'lit1':
            stack.append('q_lit1')
        elif quote_type == 'sum' or quote_type == 'para':

            if quote_type == 'sum':
                stack.append('q_sum')
            else:
                stack.append('q_para')
        else:
            stack.append('q_other')
    elif element.tag == f'{ns}bibl':
        bibl_type = element.attrib.get('type')

        if not bibl_type or (not bibl_type == 'other' and not bibl_type == 'ignore'):
            stack.append('b_use')
        else:
            stack.append('b_not_use')
    else:
        stack.append(element.tag.removeprefix(ns))

    if element.tag == f'{ns}p':
        result += '\n\n'
        is_first_head = False
    elif element.tag == f'{ns}head':
        if not is_first_head:
            result += '\n\n'
        is_first_head = False
    elif 'q_lit1' == stack[-1]:
        quote_ref_id = None
        if element.attrib.get('corresp'):
            attrib_corresp = element.attrib.get('corresp')

            if not attrib_corresp.startswith('#') and not attrib_corresp == 'none':
                raise Exception('Something is wrong')

            if attrib_corresp != 'none':
                parts = attrib_corresp.split('_', 1)
                quote_ref_id = parts[1]
        else:
            print('No corresp info')
            quote_ref_id = None

        if quote_ref_id:
            result += f'@{quote_ref_id}@'
        else:
            result += '@@'
        is_first_head = False
    elif 'q_sum' == stack[-1] or 'q_para' == stack[-1]:
        attrib_id = element.attrib.get('{http://www.w3.org/XML/1998/namespace}id')
        source = element.attrib.get('source')
        prev_id = element.attrib.get('prev')

        if attrib_id:
            parts = attrib_id.split('_', 1)
            q_id = parts[1]
            result += f'{INDIRECT_QUOTE}@{q_id}@{source}{INDIRECT_QUOTE}'
        elif prev_id:
            parts = prev_id.split('_', 1)
            prev_id = parts[1]
            result += f'{INDIRECT_QUOTE}#{prev_id}#{INDIRECT_QUOTE}'
        else:
            result += f'{INDIRECT_QUOTE}{source}{INDIRECT_QUOTE}'
    elif 'q_other' == stack[-1]:
        result += '€'
        is_first_head = False
    elif 'b_use' == stack[-1]:
        attrib_id = element.attrib.get('{http://www.w3.org/XML/1998/namespace}id')

        if attrib_id:
            parts = attrib_id.split('_', 1)
            bibl_id = parts[1]
            result += f'§µ{bibl_id}§'
        else:
            result += f'§µ§'

    if element.text:
        text = element.text
        if text:
            result += __clean_text(text)

    for text in element:
        inner_text, is_first_head = __get_text_from_element(ns, text, is_first_head, True, stack)
        result += inner_text

    if 'q_lit1' == stack[-1]:
        result += '@@'
    elif 'q_sum' == stack[-1] or 'q_para' == stack[-1]:
        result += f'{INDIRECT_QUOTE}{INDIRECT_QUOTE}'
    elif 'q_other' == stack[-1]:
        result += '€'
    elif 'b_use' == stack[-1]:
        result += '§µ§'
    elif 'footnote' == stack[-1]:
        result = f'[[[{result}]]]'
    elif 'p' == stack[-1]:
        result = result.rstrip(' ')

    if use_tail and element.tail and stack[-1] != 'p' and stack[-1] != 'head':
        text = element.tail
        if text:
            result += __clean_text(text)

    stack.pop()
    return result, is_first_head

def __clean_text(text: str) -> str:
    result = re.sub(' +', ' ', text, flags=re.DOTALL)
    result = re.sub(' *\n *', ' ', result, flags=re.DOTALL)
    result = re.sub(' +', ' ', result, flags=re.DOTALL)
    return result