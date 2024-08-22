from setuptools import setup, find_packages

setup(
    name='ns-django-custom-auth',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    license='MIT License',
    description='A custom Django authentication module',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Navjot singh',
    author_email='ns848410@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 5.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'Django>=3.2',
        'djangorestframework'
    ],
)
