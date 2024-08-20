"""
Set-up configuration for package
"""

from setuptools import setup, find_packages


with open('README.md', 'r', encoding='utf-8') as _f:
    long_description = _f.read()


setup(
    name='gofetch',
    version='0.1.2',
    author='Alex Miller',
    author_email='info@alba-analytics.co.uk',
    description="Fetch data from popular resources.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/alba-analytics/gofetch',
    packages=find_packages(
        exclude=[
            'test*',
            '.github*',
            '.vscode*',
            '.gitignore',
            '.pylintrc'
        ]
    ),
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
    ],
    extras_require={
        'shopify': [
            "ShopifyAPI==12.6.0",
            "beautifulsoup4==4.12.3",
            "pandas==2.1.2",
            "pytz==2024.1"
        ],
    },
    platforms=['linux', 'macOS'],
    test_suite='tests',
    python_requires='>=3.8.0'
)
