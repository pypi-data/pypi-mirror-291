from setuptools import setup, find_packages

setup(
    name="robotframework-xlibrary",
    version="12.1.1",
    author="Tassana Khrueawan",
    author_email="tassana.khr@gmail.com",
    description="Library Custom For Automate",
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Khrx1999/robotframework-xlibrary.git",
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=[
        # Robot Framework and related libraries
        'robotframework>=6.1.1',
        'robotframework-appiumlibrary>=2.0.0',
        'robotframework-requests>=0.9.7',
        'robotframework-seleniumlibrary>=6.3.0',
        'robotframework-mongodb-library>=3.2',
        'robotframework-jsonlibrary>=0.5',
        'robotframework-jsonvalidator>=2.0.0',
        'robotframework-ride>=1.7.4.2',
        'robotframework-xlibrary>=12.0.3',
        'robotframework-appiumflutterlibrary>=1.0.0',
        'rf-googlesheetslibrary>=0.2',

        # Python and testing libraries
        'selenium>=4.11.2',
        'requests>=2.31.0',
        'bson>=0.5.10',
        'pymongo>=4.7.2',
        'pandas>=1.3.5',
        'openpyxl>=3.1.3',
        'beautifulsoup4>=4.12.3',
        'requests_oauthlib>=2.0.0',
        'pytest>=7.4.4',

        # CV and image processing
        'opencv-python>=4.10.0.84',
        'numpy>=1.21.6',
        'Pillow>=9.5.0',

        # Google and authentication libraries
        'google-api-python-client>=2.132.0',
        'google-auth>=2.29.0',
        'google-auth-oauthlib>=1.2.0',
        'google-auth-httplib2>=0.2.0',

        # Others
        'httplib2>=0.22.0',
        'jsonpath-ng>=1.6.1',
        'jsonpath-rw>=1.4.0',
        'jsonpath-rw-ext>=1.2.2',
        'oauthlib>=3.2.2',
        'dnspython>=2.3.0',
        'tqdm>=4.66.4',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Framework :: Robot Framework',
    ],
    python_requires='>=3.6',
)
