from setuptools import setup, find_packages

setup(
    name="facilitrol_x_onboarding",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "streamlit>=1.24.0",
        "pandas>=2.0.0",
        "openpyxl>=3.1.0",
    ],
)
