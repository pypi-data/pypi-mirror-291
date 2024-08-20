from setuptools import setup


def get_readme_content():
    with open("README.md", encoding="utf-8") as f:
        return f.read()


setup(
    name="reliable-finalizer",
    version="1.0.0",
    author="TimurTimergalin",
    author_email="tmtimergalin8080@gmail.com",
    description="Python utility for creation of reliable finalizer as an alternative to __del__ method",
    long_description=get_readme_content(),
    long_description_content_type="text/markdown",
    url="https://github.com/TimurTimergalin/reliable-finalizer",
    packages=["reliable_finalizer"],
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    keywords="python finalize",
    python_requires=">=3.2"
)
