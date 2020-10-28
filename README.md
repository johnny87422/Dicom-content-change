# Dicom-content-change

主程式:dicom-change.py

需要與更改內容的.xlsx檔放在一起只要副檔名對就

可以了，然後他是用.xlsx檔裡面的PatientID欄位去尋找包含該欄

位的資料夾修改該資料夾內容的dicom檔案。詳細看.xlsx檔的擺放

方式。.xlsx檔的欄位名稱設定，B列的名稱要放修改後PatientID的

資料去對應資料夾，C列開始之後放要修改的欄位名稱，放置的名稱

需要與pydicom呼叫dicom欄位的名稱相同，所以有在做一個 dicom_dir.py

來確認欄位的名稱。


dicom_dir.py 使用方式:

把想查詢的 dicom檔 跟 dicom_dir.py 放在一起直接滑鼠右鍵點

IDLE開程式，然後按F5跑程式。就會輸出該dicom檔的欄位名稱了
