from setuptools import setup, find_packages

setup(
    name='audit_ninja',
    version='0.1.1',
    description='This is a auditing tool for Django Applications',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Anand Singh',
    author_email='anandi1990singh@gmail.com',
    url='',
    packages=find_packages(),  # Automatically finds the `audit_ninja_app` directory
    include_package_data=True,
    install_requires=[
        'django',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
    ],
)