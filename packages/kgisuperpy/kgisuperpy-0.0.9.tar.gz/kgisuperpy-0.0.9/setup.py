from setuptools import setup, find_packages

with open('README.md', 'r', encoding='UTF-8') as f:
    long_description = f.read()

setup(
    name='kgisuperpy', #pip download project name
    version='0.0.9',
    description='KGI project',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Louis Hsu',
    author_email='Louis.Hsu@kgi.com',
    packages=find_packages(),
    package_data={
        'superpy': [    #dir name and import namespace
            './.libs/Package.dll',
            './.libs/PushClient.dll',
            './.libs/TradeCom.dll',
            './.libs/QuoteCom.dll',
            './.libs/ICSharpCode.SharpZipLib.dll',
            './.libs/Interop.KGICGCAPIATLLib.dll'
        ]
    },
    install_requires=[
        'pythonnet'
    ]
)