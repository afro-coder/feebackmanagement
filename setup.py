from setuptools import setup

setup(
        name='flask_tools',
        version='1.0',
        py_modules=['flasktools'],
        install_requires=[
            'Click'
            ],
        entry_points='''
            [console_scripts]
            flasktools=flasktools:cli
        '''
)
