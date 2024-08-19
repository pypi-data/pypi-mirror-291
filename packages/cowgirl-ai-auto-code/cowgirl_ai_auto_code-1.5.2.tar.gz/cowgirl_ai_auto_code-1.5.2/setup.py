from setuptools import setup, find_packages
import os

def read_requirements():
    """Utility function to read the requirements.txt file."""
    requirements_path = "requirements.txt"
    if os.path.isfile(requirements_path):
        with open(requirements_path) as req:
            return req.read().splitlines()
    return []

setup(
    name="cowgirl-ai-auto-code",
    version="1.5.2",
    description="Cowgirl AI - Auto Code",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Cowgirl-AI/auto-code",
    author="Tera Earlywine",
    author_email="dev@teraearlywine.com",
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=read_requirements(),
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            # command=folder.script_name.main       # example
            "auto-code=cli.auto_code:main",         # auto-code refine --file='test.py'
            "front_end=cli.front_end:main",         # front_end refine --file='test.js'
            "back_end=cli.back_end:main",           # back_end refine --file='test.py'
            "qa=cli.qa:main",                       # qa refine --file='test.py'
            "script=cli.scripting_bot:main",        # script refine --file='test.sh'
            "html=cli.html_css:main",               # html refine --file='test.html'
            "network=cli.network:main",             # network refine --file='test.py'
            "md=cli.md_bot:main",                   # md refine --file='test.md'
            "js=cli.java_script:main",              # js refine --file='test.js'
            "dbt-bot=cli.sql_dbt_yml:main"          # dbt-bot refine --file='test.yml' or 'test.sql'
        ],
    },
    include_package_data=True,
    zip_safe=False,
)