#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import xml.etree.ElementTree as ET
import unicodedata
import argparse
import xmltodict
import pprint
import re


# Delete Control Character
def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

# Safe Filenames
_invalid = (
        34,  # " QUOTATION MARK
        60,  # < LESS-THAN SIGN
        62,  # > GREATER-THAN SIGN
        124, # | VERTICAL LINE
        0, 1, 2, 3, 4, 5, 6, 7,
        8, 9, 10, 11, 12, 13, 14, 15,
        16, 17, 18, 19, 20, 21, 22, 23,
        24, 25, 26, 27, 28, 29, 30, 31,
        58, # : COLON
        42, # * ASTERISK
        63, # ? QUESTION MARK
        92, # \ REVERSE SOLIDUS
        47, # / SOLIDUS
        )

table1 = {}
for i in _invalid:
    table1[i] = 95 # LOW LINE _

table2 = dict(table1)
table2.update((
        (34, 0x201d), # ”
        (60, 0xff1c), # ＜
        (62, 0xff1e), # ＞
        (124, 0xff5c), # ｜
        (58, 0xff1a), # ：
        (42, 0xff0a), # ＊
        (63, 0xff1f), # ？
        (92, 0xffe5), # ￥
        (47, 0xff0f), # ／
        ))

def safefilenames(names, table=table1, add_table=None):
    if add_table is None:
        m = table
    else:
        m = dict(table)
        m.update(add_table)
    for name in names:
        yield name.translate(m)

def safefilename(name, table=table1, add_table=None):
    return next(safefilenames([name], table, add_table))

def check_file_exists(filename):
    return os.path.isfile(filename)

def convert(input, output):
    try:
        with open(input, 'r', encoding='utf-8') as fx:
            xml_dict = xmltodict.parse(fx.read())
    except Exception as e:
        return False
    
    chats = xml_dict['packet']['chat']
    chats = sorted(chats, key=lambda x: x['@vpos'].zfill(10))
    # pprint.pprint(xml_dict)

    ### XMLに変換する辞書の雛形 ###
    converted_dict = {
        'i': {
            'chatserver': 'convert.from.nicovideo.jp',
            'chatid': '0',
            'mission': '0',
            'maxlimit': '1500',
            'state': '0',
            'real_name': '0',
            'source': 'k-v',
            'd': [
            ]
        }
        }
    


    ### 公式コメントと壊れたコメントを選別 ###
    officeId = []
    badItem = []
    for i in range(len(chats)):
        try:
            text = chats[i]['#text']
        except KeyError:
            badItem.append(i)
            continue
        except:
            print(i)
        user_id = chats[i]['@user_id']
        premium = chats[i]['@premium'] if '@premium' in chats[i] else ''
        if premium == '3' or premium == '7':
            officeId.append(user_id)
        elif user_id == "-1":
            officeId.append(user_id)
        if i == len(chats) - 1 and len(officeId) == 0:
            officeId.append('0')
    for i in badItem[:: -1]:
        chats.pop(i)

    for chat in chats:
        
        ### コメント内容の処理 ###
        text = chat['#text']
        user_id = chat['@user_id']  # id
        mail = chat['@mail'] if '@mail' in chat else ''
        premium = chat['@premium'] if '@premium' in chat else ''
        ### 運営コマンド等 不要なコメントはスキップ ###
        if '※ NGコメント' in text or '/clear' in text or '/trialpanel' in text or '/spi' in text or '/disconnect' in text or '/gift' in text or '/commentlock' in text or '/nicoad' in text or '/info' in text or '/jump' in text or '/play' in text or '/redirect' in text:
            continue
        
        elif premium == '2':
            continue
        elif chat['@vpos'] == '':
            continue
        ### 面倒なHTMLタグは無視する ###
        elif '<br>' in text :
            text = text.replace('<br>', '\n')
        elif '<b>' in text or '<s>' in text or '<font' in text or '<i>' in text or '<u>' in text :
            text = re.sub(r'<.*?>', '', text)
        
        ### 1回だけthreadをchatidとして設定
        if 'chatid' not in locals():
            chatid = chat['@thread']

        ### date (Unix秒) をそのまま設定###
        date = chat['@date']

        ### vpos (1/100 秒) から秒数へ ###
        ### 負数の場合0.00000に設定
        if int(chat['@vpos']) < 0:
            seconds = '0.00000'
        else:
            seconds = "{:.5f}".format(float(chat['@vpos']) / 100)


        ### 公式コメントはTop表示 ###
        if chat['@user_id'] in officeId:
            danmaku_type = '5'
        else:
            danmaku_type = '1'

        ### デフォルトの文字サイズ ###
        font_size = '25'
        

        ### スタイル関連 ###

        ### カラーコマンドと10進カラーコードを対応させる ###
        color_map = {'black': '00000000', 'white': '16777215', 'red': '16711680', 'green': '00065280', 'yellow': '16776960', 'blue': '00000255', 'orange': '16763904', 'pink': '16744576', 'cyan': '00065535', 'purple': '12583167', 'niconicowhite': '13421721', 'white2': '13421721', 'truered': '13369395', 'red2': '13369395', 'passionorange': '16737792', 'orange2': '16737792', 'madyellow': '10066176', 'yellow2': '10066176', 'elementalgreen': '00052326', 'green2': '00052326', 'marineblue': '03407820', 'blue2': '03407820', 'nobleviolet': '06697932', 'purple2': '06697932'}

        ### 位置コマンドとdanmakuスタイルを対応させる ###
        scroll_type_map = {'ue': '5' , 'naka': '6', 'shita': '4'}

        ### 大きさコマンドとフォントサイズを対応させる ### 
        font_size_map = {'big': '45' , 'small': '16'}

        color = '16777215'
        color_important = 0

        for style in mail.split(' '):
            if re.match(r'#([0-9A-Fa-f]{6})', style):
                m = re.match(r'([0-9A-Fa-f]{6})', style)
                # 16進 - 10進変換
                color = int(str(m[1]), 16)
                color = str(color)
            elif style in color_map:
                color = color_map[style]
            elif style in scroll_type_map:
                danmaku_type = scroll_type_map[style]
            elif style in font_size_map:
                font_size = font_size_map[style]

        ### コメントとスタイル等を辞書に追加する
        comment_dict = {
            '@p': ','.join([seconds, danmaku_type, font_size, color, date, '0', user_id, '0', '1']) ,
            '#text': text
        }
        converted_dict['i']['d'].append(comment_dict)
            
    converted_dict['i']['chatid'] = chatid
    
    ### 書き出し ###
    output_str = xmltodict.unparse(converted_dict, pretty=True)

    with open(output, "w", encoding='utf-8') as file:
        file.write(output_str)

if __name__ == '__main__' :
    parser = argparse.ArgumentParser(description='niconico danmaku xml to bilibili danmaku xml.', add_help=True)
    parser.add_argument('input', help='Input filename.')
    parser.add_argument('output', help='Output filename. (Optional)', nargs='?', default='out.xml')
    parser.add_argument('-y','--overwrite', help='If there is a file with the same name, overwrite it with the converted file', action='store_true')
    args = parser.parse_args()

    if not args.overwrite and check_file_exists(args.output):
        print('There is a file with the same name as output.')
        exit(1)
    
    convert(args.input, args.output)