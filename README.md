# nico_xml_to_bili

Convert niconico (nicovideo.jp) comments (danmaku) xml to bilibili danmaku xml

ニコニコのxml形式のコメントをbilibiliのxml形式のコメント(弾幕/danmaku/danmu)に変換するツール

--- ---
--- ---

## Why made this tool?

Because there are few applications that can handle niconico xml files.

On the other hand, there are many applications developed in China that can handle bilibili xml files.
--- ---
ニコニコのxmlファイルを扱えるアプリが少なく、逆にbilibiliのxmlファイルを扱えるアプリは中国国内で多数開発されているから。

特にAndroidでローカルファイルを見ようとすると、既存ツールでは再生速度が変えられなかったり、PiPが使えなかったりと不便に感じることも多かった。

主に生放送コメントを変換することを自身の目的としているため、細かいレイアウトは考慮していません。

--- ---
--- ---

## Usage

```code
usage: nico_xml_to_bili.py [-h] [-y] input [output]

niconico danmaku xml to bilibili danmaku xml.

positional arguments:
  input            Input filename.
  output           Output filename. (Optional)

options:
  -h, --help       show this help message and exit
  -y, --overwrite  If there is a file with the same name, overwrite it with the converted file
```

--- ---
--- ---

## What can/can't do?

- [x] Basic comments / 基本的なコメント
- [x] Color, font size, and position data written in "Nicoscript" / ニコスクリプトで書かれた色、大きさ、位置
- [x] Delete comments that disturb, such as commands by management / 運営コマンドなど、邪魔になるコメント削除
- [ ] time on screen and font data written in "Nicoscript" / ニコスクリプトで書かれた秒数、フォント
- [ ] HTML contained in comments / コメントに含まれるHTML
- [ ] Survey function / アンケート(投票)機能
- [ ] etc. / 他の様々な未実装機能

--- ---
--- ---

## Contribute

It is in the development stage and may contain various bugs.

開発中で、様々な不具合を含む可能性があります。

1. Please use "Issues" if you encounter problems.  
  不具合に遭遇したら、"Issues"を利用してください。
2. Please use "Pull Requests" if you want to help improve the functionality of the code.
  コードを改良してくれる方は、"Pull Requests"を利用してください。
3. Please use "Discussion" for questions and discussions.
  質問や議論したいことがあれば、"Discussion"を利用してください。

--- ---
--- ---

## Related Links

- [b站弹幕信息解释 - 哔哩哔哩](https://www.bilibili.com/read/cv6997749/)
  - bilibiliのコメントスタイルを解析するのに役立った (若干古い部分はあったが)
- [kumaneru/nicoxml2ass](https://github.com/kumaneru/nicoxml2ass)
  - ニコニコのコメントスタイルを処理するのに役立った
- [xmltodict · PyPI](https://pypi.org/project/xmltodict/)
  - 利用している外部ライブラリ
- [KikoPlayProject/KikoPlay](https://github.com/KikoPlayProject/KikoPlay)
  - danmaku付きで再生できるマルチプラットフォームの動画プレイヤー
- [xyoye/DanDanPlayForAndroid](https://github.com/xyoye/DanDanPlayForAndroid)
  - danmaku付きで再生できるAndroid向け動画プレイヤー
