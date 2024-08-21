from setuptools import setup, find_packages

setup(
    name='codefeedback',
    version='0.3.0',
    description='na',
    packages=find_packages(),
    python_requires='>=3.6',
    install_requires=[
        'numpy',
        'pandas',
        'openai==0.28',
        'python-dotenv'
    ],
)
