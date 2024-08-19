from setuptools import setup

setup(
    entry_points={
        'sqlalchemy.dialects': [
            'gbasedbt = sqlalchemy_gbasedbt.dbtdb:GBasedbtDialect',
        ]
    }
)
