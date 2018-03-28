#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os, json, re
from models.models import Author, Poetry
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from multiprocessing import Process
from zhconv import convert_for_mw

#     zh-cn 大陆简体
#     zh-tw 台灣正體
#     zh-hk 香港繁體
#     zh-hans 简体
#     zh-hant 繁體

Font = 'zh-cn'
# engine = create_engine('mysql+pymysql://root:jiwenxuan@114.113.126.247/poetry?charset=utf8mb4')
engine = create_engine('postgresql+psycopg2://jiwenxuan:jiwenxuan@114.113.126.247:5432/poetry')
dbsession = sessionmaker(bind=engine, autoflush=True)
poet_file_list = os.listdir('json_data')
split_list = [poet_file_list[i:i + 20] for i in range(0, len(poet_file_list), 20)]


def Write_database(list):
    session = dbsession()
    for i in list:
        if re.search('authors.song.', i) or re.search('authors.tang.', i):
            if re.search('song', i):
                dynasty = '宋'
            else:
                dynasty = '唐'
            for j in json.load(open(os.path.join('json_data', i), encoding='utf8')):
                author_table = Author(Font_conversion(j['name']), Font_conversion(j['desc']), dynasty)
                session.add(author_table)
                session.commit()
        elif re.search('poet.song.', i) or re.search('poet.tang.', i):
            if re.search('song', i):
                dynasty = '宋'
            else:
                dynasty = '唐'
            for j in json.load(open(os.path.join('json_data', i), encoding='utf8')):
                poet_table = Poetry(Font_conversion(j['title']), Font_conversion(j['author']), dynasty,
                                    Font_conversion(json.dumps(j['paragraphs'], ensure_ascii=False)),
                                    Font_conversion(json.dumps(j['strains'], ensure_ascii=False)))
                session.add(poet_table)
                session.commit()
        else:
            pass
            session.close()


def Font_conversion(string):
    if Font == 'zh-hant':
        return string
    else:
        content = convert_for_mw(string, Font)
    return content


if __name__ == '__main__':

    for i in split_list:
        work = Process(target=Write_database, args=(i,))
        work.start()

# Write_database(poet_file_list)
