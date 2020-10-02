# -*- mode: python -*-

block_cipher = None


a = Analysis(['checksum_checker.py'],
             pathex=['C:\\Users\\ben\\Documents\\work\\checksum_checker'],
             binaries=[],
             datas=[('C:\\Users\\ben\\Documents\\work\\checksum_checker\\app\\static\\WRGL_logo.png', 'app\\static'),
                    ('C:\\Users\\ben\\Documents\\work\\checksum_checker\\app\\static\\favicon.ico', 'app\\static')],
             hiddenimports=['tkinter'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='checksum_checker',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True , icon='app/static/favicon.ico')

		  
#import shutil
#shutil.copyfile('transfer.config', '{0}/transfer.config'.format(DISTPATH))
