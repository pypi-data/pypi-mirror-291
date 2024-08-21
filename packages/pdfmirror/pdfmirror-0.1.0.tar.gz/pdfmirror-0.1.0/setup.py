from setuptools import setup, find_packages

setup(
    name='pdfmirror',
    version='0.1.0',
    packages=find_packages(),
    py_modules=['main_threaded'],
    entry_points={
        'console_scripts': [
            'my_tool = my_tool:main',
        ],
    },
    install_requires=[
        # List any dependencies your tool needs here
    ],
    author='Hunter Kievet',
    description='A CLI tool to mirror a pdf',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/hkievet/pdfmirror',  # Link to your GitHub repo
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)