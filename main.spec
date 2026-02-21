# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('fonts', 'fonts'),
        ('Simulations', 'Simulations'),
        ('Sounds', 'Sounds'),
    ],
    hiddenimports=[
        'Simulations.growing_sphere',
        'Simulations.shrinking_ring',
        'Simulations.butterfly_effect',
        'Simulations.duplicating_balls',
        'Simulations.bounce_countdown',
        'Simulations.time_countdown',
        'Simulations.gravity_well',
        'Simulations.chain_reaction',
        'Simulations.pendulum_wave',
        'pygame.gfxdraw',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
