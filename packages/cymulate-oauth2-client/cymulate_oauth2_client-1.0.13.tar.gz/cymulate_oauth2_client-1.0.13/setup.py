from setuptools import setup, find_packages

setup(
    name='cymulate_oauth2_client',
    version='1.0.13',
    description='A Python client for OAuth2 authentication with Cymulate API',
    author='Cymulate',
    author_email='roys@cymulate.com',
    url='https://github.com/cymulate-ltd/oauth2-client',
    packages=find_packages(),
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    install_requires=[
        'requests>=2.31.0',
        'tenacity>=8.2.2',
        'urllib3>=2.0.6',
        'aiohttp>=3.8.6',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.12',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
    extras_require={
        'dev': [
            'pytest>=7.4.0',
            'pytest-asyncio>=0.21.0',
            'flake8>=6.1.0',
            'black>=23.7.0',
        ],
    },
    include_package_data=True,
    zip_safe=False,
)