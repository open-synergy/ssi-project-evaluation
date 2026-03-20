import setuptools

with open('VERSION.txt', 'r') as f:
    version = f.read().strip()

setuptools.setup(
    name="odoo14-addons-open-synergy-ssi-project-evaluation",
    description="Meta package for open-synergy-ssi-project-evaluation Odoo addons",
    version=version,
    install_requires=[
        'odoo14-addon-ssi_project_evaluation',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Odoo',
        'Framework :: Odoo :: 14.0',
    ]
)
