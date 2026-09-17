{
    'name': "Command Pallete Search Records",
    'version': '1.2',
    'summary': "Command Pallete Search Records",
    'sequence': 10,
    'license': "AGPL-3",
    'author' : 'Jagadish M',
    'depends': ['base', 'web'],
    'author': "JD DEVS",
    'data' : [
        'views/views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            "command_palette_search_records/static/src/js/command_palette.js",
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/assets/screenshots/banner.png'],
    'icon': "/command_palette_search_records/static/description/icon.png",
}

