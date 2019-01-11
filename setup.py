"""
Setup module to build distribution packages of regex4ocr.
"""
from setuptools import setup

setup(
    name="regex4ocr",
    version="1.0.4",
    url="https://github.com/juntossomosmais/regex4ocr",
    license="MIT",
    author="Igor Grillo Peternella",
    author_email="igor.feq@gmail.com",
    description="Extract data from OCR string results based on Document Regexp Models (DRMs).",
    packages=["regex4ocr", "regex4ocr.logger", "regex4ocr.parser"],
    install_requires=["PyYAML==4.2b1", "Unidecode==1.0.23"],
    long_description=open("README.md").read(),
    zip_safe=False,
)
