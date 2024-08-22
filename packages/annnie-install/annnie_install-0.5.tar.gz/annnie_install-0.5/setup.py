from setuptools import setup, find_packages

setup(
    name='annnie_install',
    version='0.5',
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
        # pip install openai
        # pip install Flask
        # sudo apt-get install python3-tk
        'numpy',
        'openai',
        'Flask',
        # 'python3-tk',
        'requests',
    ],
    author='Siyu Qiu',
    author_email='siyu.qiu1@unsw.edu.au',
    description='Everything you need to install for the LLM4HW tool',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/annnie_file',  # Replace with your repo URL
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
