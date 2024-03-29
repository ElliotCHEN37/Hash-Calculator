# Hash-Calculator 雜湊值計算器

A simple hash value calculation program written in PyQt5<br>
一個用PyQt5編寫的簡單雜湊值計算器

<table>
    <tr>
        <td>
            <a href="https://github.com/ElliotCHEN37/Hash-Calculator/releases/latest/download/Hash_Calculator_Windows.exe"><img src="download.png" alt="Download Standard version" /></a>
        </td>
        <td>
            <a href="https://github.com/ElliotCHEN37/Hash-Calculator/releases/download/v1.9/Hash_Calculator_Windows_DEBUG.exe"><img src="download_debug.png" alt="Download Debug version" /></a>
        </td>
        <td>
            <a href="https://github.com/ElliotCHEN37/Hash-Calculator/releases/download/v1.5.1/Hash_Calculator_Windows_CLI.exe"><img src="download_cli.png" alt="Download Command line version" /></a>
        </td>
    </tr>
</table>

![Hash Calculator](2.0.png)

## SUPPORT ARGUMENTS LIST 支援的參數清單
1. Hash_Calculator_Windows.exe -path <path to file 文件路徑>
2. Hash_Calculator_Windows.exe -string <strings 字符串>

## NO LONGER SUPPORT FEATURES LIST 不再支援的功能的清單

-[Auto Compare 自動比較](#auto-compare-自動比較-v15-v18)<br>
-[JSON Compare JSON對比](#JSON-file-format-JSON-文件格式)

## Build and Environment 構建以及環境

### Environment 環境

-Python 3<br>
-PyQt5<br>
-QDarkStyle<br>

1. Download Python 3 from <a href="https://www.python.org">www.python.org</a> and install it.<br>
   從<a href="https://www.python.org">www.python.org</a>下載並且安裝Python 3
2. Run `pip install pyqt5` in terminal or `pip install -r requirements.txt`<br>
   在終端中執行`pip install pyqt5`或者`pip install -r requirements.txt`
3. Run `pip install qdarkstyle` in terminal or `pip install -r requirements.txt`<br>
   在終端中執行`pip install qdarkstyle`或者`pip install -r requirements.txt`

### Build for Windows 為Windows構建

#### PyQt5

1. Run`pip install pyinstaller` (If you installed pyinstaller, just skip it)<br>
   執行`pip install pyinstaller`（如果你已經安裝過，請跳過）<br>
2. Run`pyinstaller <path to main.py>`to create executable file<br>
   執行`pyinstaller <main.py的路徑>`來創建可執行文件<br>
   -Add`--onefile`if you want a single file version<br>
   如果你只想要組建單個可執行文件，請添加`--onefile`<br>
   -Add`--noconsole`if you want to hide the terminal<br>
   如果你想要隱藏終端窗口，請添加`--noconsole`

#### CLI Version 命令行版本 NO LONGER SUPPORT 不再支援

1. Run`pip install pyinstaller` (If you installed pyinstaller, just skip it)<br>
   執行`pip install pyinstaller`（如果你已經安裝過，請跳過）<br>
2. Run`pyinstaller <path to main.py>`to create executable file<br>
   執行`pyinstaller <main.py的路徑>`來創建可執行文件<br>
   -Add`--onefile`if you want a single file version<br>
   如果你只想要組建單個可執行文件，請添加`--onefile`<br>

## Variants 變體

#### CLI (Command Line) Edition 命令行版本<br>

#### Usage 用法

1. Run the program directly. <br>
   直接執行程序
2. Run the program with argument in terminal. <br>
   在終端中以參數啟動程序<br>
   `Hash_Calculator_CLI.exe <file_path 文件路徑>`<br>

#### DEBUG EDITION 除錯版本 NO LONGER SUPPORT 不再支援

#### Usage 用法

As same as the standard version<br>
與標準版相同

## Changelog 更新日志

#### PyQt5 Edition PyQt5版本

v2.1<br>
NEW 新功能<br>
-Start with argument 以參數啟動<br>

v2.0<br>
NEW 新功能<br>
-Add dark theme 添加黑暗模式<Br>

v1.9.1<br>
NEW 新功能<br>
-Add a progress bar 增加了進度列<br>
FIX 修正<Br>
-Fix some BUGs 修正一些錯誤

v1.9<br>
!!!BIG UPDATE 重大更新!!!<br>
-RE-MADE COMPARE FEATURE 重製Compare功能<br>
FIX 修復<br>
-Icon will show in the title bar and the task bar now 現在標誌會在標題列與工作列中顯示

v1.8<br>
This version is based on v1.6 but include v1.7's function 該版本基於v1.6但是擁有完整的v1.7功能<br>
New 新功能
-Re-support drag and drop 重新支援拖拽<br>
-Adjust the GUI 調整GUI介面

v1.7<br>
New 新功能<br>
-Support text input 支援文字輸入<br>
!!!BIG CHANGE 重大改動!!!<br>
-NO LONGER SUPPORT "DRAG AND DROP" FUNCTION 不再支援拖拽功能<br>
-REMOVE BROWSE BUTTON 移除瀏覽按鈕 (It may be restored in the next version 可能會在下一個版本中恢復)

v1.6<br>
New 新功能<br>
-Support export results as TXT or JSON 支援以TXT或者JSON格式匯出結果<br>
-Clean up and re-format some codes 整理並格式化部分代碼<br>
-App icon from Google Fonts 從Google Fonts來的軟體圖標

v1.5.5<br>
New 新功能<br>
-Online Compare 線上對比

v1.5.4<br>
Fix 修復<br>
-Fix compare function 修復比較功能<br>
-Fix BUGs 修正程錯

v1.5.3<br>
Fix 修復<br>
-Fix compare logic 修復比較邏輯

v1.5.2<br>
New 新功能<br>
-New export format 新的匯出格式

v1.5.1<br>
Fix 修復<br>
-Changelog link 更新日誌連結<br>
New 新功能<br>
-Debug mode 除錯模式

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

#### CLI Edition 命令行版本 NO LONGER SUPPORT 不再支援

v1.0<br>
Initial Release 初版

## About 關於

[LICENSE 授權](LICENSE.txt)

![Google Fonts](gfonts.png)
