from setuptools import setup, find_packages

setup(
    name='botrun-log',
    version='0.3.0',
    packages=find_packages(),
    install_requires=[
        'google-cloud-bigquery',
        'google-auth',
        'cryptography',
        'python-dotenv',
        'pytz',
        'psycopg2-binary',
    ],
    extras_require={
        'dev': [
            'pytest',
        ],
    },
    author='JcXGTcW',
    author_email='jcxgtcw@gmail.com',
    description='A Python package for botrun-application logging, using Google BigQuery and PostgreSQL.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/bohachu/bigquery_log_jc',
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
)
