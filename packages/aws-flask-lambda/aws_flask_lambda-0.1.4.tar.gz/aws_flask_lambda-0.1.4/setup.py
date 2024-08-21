from setuptools import setup

setup(
    name='aws_flask_lambda',
    version='0.1.4',
    description='Library to run applications on AWS Lambda Function using Flask',
    author='Seven Clouds Technologies',
    author_email='admin@seventechnologies.cloud',
    long_description_content_type='text/markdown',
    long_description=open('README.md').read(),
    packages=["aws_flask_lambda"],
    package_dir={"aws_flask_lambda": "aws_flask_lambda"},
    include_package_data=True,
    install_requires=[
        'Flask==3.0.3',
        'werkzeug==3.0.3'
    ],
    classifiers=[
        'Programming Language :: Python :: 3.8',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
