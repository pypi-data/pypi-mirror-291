from setuptools import setup, find_packages

setup(
    name="consolellm",                
    version="0.1.2",                  
    author="Anshul Sharma",
    author_email="thevoxium@gmail.com",
    description="Access Llama in your terminal.  ",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/thevoxium/consoleLLM", 
    packages=find_packages(),         
    install_requires=[          
        'markdown2==2.5.0',
        'openai==1.41.0',
        'rich==13.7.1',
        'toml==0.10.2',
    ],
    classifiers=[                      
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'consolellm=consolellm.app:main',  # Specify the entry point for the console command
        ],
    },
)
