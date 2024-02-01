# Hash-Calculator 雜湊值計算器
A simple hash value calculation program written in PyQt5<br>
一個用PyQt5編寫的簡單雜湊值計算器

![Hash Calculator](Hash_Calculator_v1.5.png)

### Features 特點以及功能
-Written in Pyhon and PyQt<br>
-使用Python以及PyQt編寫<br>
-Export results<br>
-匯出結果<br>
-Compare results<br>
-比較結果<br>

### Special Feature in v1.5+ 1.5及更高版本中的特殊功能
If there is a "hash_values.json" available in the working directory, Hash_Calculator will auto compare the results, and change the color* of results in GUI windows.<br>
如果在工作目錄下有"hash_values.json"，那麼Hash_Calculator將會自動對比結果並且改變圖形化介面的結果顏色*<br>
*Green Texts: Matched, Red Texts: Didn't match 綠色字體：相符，紅色字體：不符<br>

### JSON file format JSON文件格式
```JSON
{
  "MD5": "<MD5VALUE, MD5值>",
  "SHA1": "<SHA1VALUE, SHA1值>",
  "SHA256": "<SHA256VALUE, SHA256值>",
  "SHA512": "<SHA512VALUE, SHA512值>",
  "CRC32": "<CRC32VALUE, CRC32值>"
}

```
<br>
JSON File can be incomplete<br>
JSON 文件可以不完整

## Build and Environment 構建以及環境
### Environment 環境
-Python 3<br>
-PyQt5<br>
1. Download Python from [www.python.org](<www.python.org>) and install it.<br>
   從[www.python.org](<www.python.org>)下載並且安裝Python
2. Run `pip install pyqt5` in terminal or `pip install -r requirements.txt`<br>
   在終端中執行`pip install pyqt5`或者`pip install -r requirements.txt`

### Build for Windows 為Windows構建
1. Run`pip install pyinstaller` (If you installed pyinstaller, just skip it)<br>
   執行`pip install pyinstaller`（如果你已經安裝過，請跳過）<br>
2. Run`pyinstaller <path to main.py>`to create executable file<br>
   執行`pyinstaller <main.py的路徑>`來穿件可執行文件<br>
-Add`--onefile`if you want a single file version<br>
 如果你只想要組建單個可執行文件，請添加`--onefile`<br>
-Add`--noconsole`if you want to hide the terminal<br>
 如果你想要隱藏終端窗口，請添加`--noconsole`

## IMPORTANT 注意
Please note that you may encounter Windows Defender mistakenly identifying it as a "Trojan horse virus". Just unblock it. The software does not have any virus functions and is completely clean. If you still have concerns, you can check the software source code or build the executable file from the source code yourself to ensure security. I also promise not to plant any viruses into this project.<br>
請注意Windows Defender可能會錯誤地將該程序識別為特洛伊木馬病毒。只需要將其解除封鎖即可。該軟體完全沒有任何的病毒功能並且是完全乾淨的，如果你仍有疑慮可以檢查原始碼或者自己構建可執行檔案以確保安全。我也承諾不會添加任何的病毒到該項目。
## NEW FEATURES 新功能
!!!To use these functions, you MUST selected a file!!!<br>
！！！如需使用以下功能，你必須選擇一項檔案！！！
### EXPORT 匯出 (v1.4)
You can use this function by pressing "Ctrl+S" or going to "File" -> "Export"<br>
你可以通過"Ctrl+S"或者前往"File" -> "Export"

### COMPARE 比較 (v1.5)
You can use this function by pressing "Ctrl+H" or going to "File" -> "Compare"<br>
你可以通過"Ctrl+H"或者前往"File" -> "Compare"

## Changelog 更新日志
v1.5<br>
New 新功能<br>
-Compare feature 比較功能<br>
-Redirect Changelog to here 將Changelog重新導向至此<br>
-New update message box for special situation 特殊情況下的更新對話框

v1.4.1<br>
New 新功能<br>
-More shortcuts 更多快速鍵<br>
-Check for update 檢查更新

v1.4<br>
New 新功能<BR>
-Export 匯出

## About 關於
[LICENSE 授權](LICENSE.txt)

## Sponsor 抖內
李涵博 $0.42 CNY 人民幣
![WeChat 微信](WeChat.JPG)