from setuptools import setup, find_packages

setup(
    name='easywindcss',
    version='1.1',  # Update this version as needed
    description='A Python library to automate Tailwind CSS setup in your python environment.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Sayed Afaq',
    packages=find_packages(),
    install_requires=[
        'colorama',
    ],
    python_requires='>=3.6',
    entry_points={
        "console_scripts":[
            "easywindcss = easywindcss:install",
            "easywindcss-v = easywindcss:check_et"
        ]
    }
)
