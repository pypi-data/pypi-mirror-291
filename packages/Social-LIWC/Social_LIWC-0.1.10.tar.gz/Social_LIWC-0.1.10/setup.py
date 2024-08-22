from setuptools import setup

with open("README.md", "r") as arq:
    readme = arq.read()

setup(name='Social_LIWC',
    version='0.1.10',
    license='MIT License',
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=['fastapi', 'liwc', 'pandas'],
    packages=['Social_LIWC/api'],
    include_package_data=True,
    package_data={
        'Social_LIWC': ['dados/v2_LIWC2007_Portugues_win_utf8.dic'],
    }
)