from setuptools import setup, find_packages

setup(
    name="json4ocr",
    version="0.1",
    url="https://github.com/juntossomosmais/json4ocr",
    license="MIT",
    author="Igor Grillo Peternella",
    author_email="igor.feq@gmail.com",
    description="Converts OCR string results into Python Dicts based on Document Regexp Models (DRMs).",
    packages=find_packages(exclude=["tests"]),
    long_description=open("README.md").read(),
    zip_safe=False,
)
