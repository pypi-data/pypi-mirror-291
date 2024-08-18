from setuptools import setup, find_packages

setup(
    name="ola-ai",
    version="1.0.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
        "PyYAML",
        "openai",
	"python-dotenv"
    ],
    entry_points={
        "console_scripts": [
            "ola=ola_cli.cli:main",
        ],
    },
)
