# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['..\\src\\main\\main.py'],
    pathex=['..\\'],
    binaries=[],
    datas=[
		('..\\src\\collar_survey\\*', 'collar_survey'),
		('..\\src\\dh_survey\\*', 'dh_survey'),
		('..\\src\\gui\\*', 'gui'),
		('..\\src\\import_data\\*', 'import_data'),
		('..\\src\\scene_control\\*', 'scene_control'),
		('..\\src\\text\\*', 'text'),
		('..\\src\\triangulation\\*', 'triangulation'),
		('..\\icon\\GeoView.ico', 'icon'),
		('..\\README.md', '.'),
		],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

splash = Splash('..\\splash\\GeoSplash.png',
                binaries=a.binaries,
                datas=a.datas,
                text_pos=None,
                text_size=12,
                text_color='black')

exe = EXE(
    pyz,
    a.scripts,
	splash,
	splash.binaries,
    a.binaries,
    a.datas,
    [],
    name='GeoView v0.0.3',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='..\\icon\\GeoView.ico'
)