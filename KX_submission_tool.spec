# -*- mode: python -*-
a = Analysis(['showUI.py'],
             pathex=['E:\\Scripts\\Eclipse\\kx_submission_tool'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='KX_submission_tool.exe',
          debug=False,
          strip=None,
          upx=True,
          console=False , icon='E:\\Scripts\\Eclipse\\kx_submission_tool\\kx_submission_tool.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=None,
               upx=True,
               name='KX_submission_tool')
