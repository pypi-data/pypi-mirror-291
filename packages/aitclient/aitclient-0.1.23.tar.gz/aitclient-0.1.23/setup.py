from setuptools import setup, find_packages

setup(
    name='aitclient',
    version='0.1.23',  # Update the version number
    packages=find_packages(),
    install_requires=[
        'requests',
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'aitclient=aitclient:main',
        ],
    },
    author='Bobby Svidron',
    author_email='bobby.svidron@sap.com',
    description='A Python library for AIT client operations',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/I835834/aitclient',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    package_data={
        'aitclient': ['certs/SAP_Global_Root.pem'],  # Include the CA certificate file
    },
    include_package_data=True,
)
