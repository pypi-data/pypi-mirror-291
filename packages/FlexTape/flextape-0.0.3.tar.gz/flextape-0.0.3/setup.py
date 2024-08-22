from setuptools import setup

    



setup(
    name             ='FlexTape',
    version          ='0.0.3',
    description      ='Python library to download multiple images at once with a request limit.',
    long_description              = open('README.md', 'r').read(),
    long_description_content_type = 'text/markdown',
    author           ='Duckling Dean',
    author_email     ='duckling.dean@proton.me',
    packages         =["flextape",],
    install_requires = [
        "requests>=2.32.2,<3.0.0",
        "fake-useragent==1.5.1",
    ]
)

