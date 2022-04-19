import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="faux",
    version="1.0.0",
    author="~midsum-salrux",
    author_email="",
    description="Chat bridge between urbit and discord",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/midsum-salrux/faux",
    packages=setuptools.find_packages(),
    install_requires=['quinnat', 'discord.py'],
    classifiers=[],
    python_requires='>=3.7',
)
