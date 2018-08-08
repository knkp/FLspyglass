# -*- mode: python -*-

block_cipher = None


a = Analysis(['spyglass.py'],
             pathex=['c:\\Users\\knkp9\\Documents\\Projects\\spyglass\\src'],
             datas=[ 
                 ('C:\\Users\\knkp9\\Documents\\Projects\\spyglass\\src\\vi\\ui\\*ui','src\\vi\\ui'),
                 ('C:\\Users\\knkp9\\Documents\\Projects\\spyglass\\src\\vi\\ui\\res\\*wav','src\\vi\\ui\\res'),
                 ('C:\\Users\\knkp9\\Documents\\Projects\\spyglass\\src\\vi\\ui\\res\\*png','src\\vi\\ui\\res'),
                 ('C:\\Users\\knkp9\\Documents\\Projects\\spyglass\\src\\vi\\ui\\res\\*cmd','src\\vi\\ui\\res'),
                 ('C:\\Users\\knkp9\\Documents\\Projects\\spyglass\\src\\vi\\ui\\res\\mapdata\\*svg','src\\vi\\ui\\res\\mapdata'),
                 ('C:\\Users\\knkp9\\Documents\\Projects\\spyglass\\src\\vi\\ui\\res\\styles\\*css','src\\vi\\ui\\res\\styles'),
                 ('C:\\Users\\knkp9\\Documents\\Projects\\spyglass\\src\\vi\\ui\\res\\styles\\*yaml','src\\vi\\ui\\res\\styles')
             ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='spyglass',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=False )
