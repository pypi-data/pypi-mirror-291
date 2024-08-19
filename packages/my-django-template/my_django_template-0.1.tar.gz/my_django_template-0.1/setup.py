from setuptools import setup, find_packages

setup(
    name='my-django-template',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,  # Ensures static and template files are included
    license='MIT',
    description='A reusable Django template.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Your Name',
    author_email='your.email@example.com',
    url='https://github.com/alanwoodenclouds/my-django-template',  # Your project's URL
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Framework :: Django :: 3.0',
    ],
)
