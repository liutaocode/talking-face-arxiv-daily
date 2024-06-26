"""
Grobid XML to Markdown for cleaner LLM corpus
@Author: Cheng Deng
"""
import os
import time

from grobid_parser import parse
from pdf_parser import Parser

def pipeline(xml_tmp_path, file_path, rich_markdown_host, rich_markdown_port):
    parser = Parser('grobid', host=rich_markdown_host, port=rich_markdown_port)
    parser.parse('text', file_path, xml_tmp_path, 50)
    print("FINISH PARSING")
    result = []
    xml_result = []
    with open(f'''{xml_tmp_path}/{file_path.split('/')[-1].replace('.pdf', '')}.grobid.xml''') as f:
        xml_text = f.read()
        xml_result.append(xml_text)
        res = parse.parse_document_xml(xml_text)
        result = [res.header, res.abstract, res.body]
    
    print(res.header)
    title = result[0].title
    abstract = result[1]
    
    print(title, abstract)
    if len(title.strip()) != '':
        title_text = f"\n\n# {title}\n\n"
    else:
        title_text = ''
    
    if abstract is not None and len(abstract.strip()) != '':
        abstract_text = f"## Abstract\n\n{abstract}\n\n"
    else:
        abstract_text = ''
    
    final_text = f"{title_text}{abstract_text}{result[2]}"
    xml_res = xml_result[0]
    print("FINISH REPARSING")
    return xml_res, final_text