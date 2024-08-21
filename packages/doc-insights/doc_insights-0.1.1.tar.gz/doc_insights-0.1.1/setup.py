from setuptools import setup, find_packages
import os

def post_install_message():
    notebook_path = os.path.join(os.path.dirname(__file__), 'validate.ipynb')
    print("\nThank you for installing doc_insights!")
    print("Please visit the README.md file in the package directory for further instructions.")
    print("Or visit: https://github.com/c3-chrismahlke/doc-insights for more details.")
    print(f"\nTo get started, you can run the example notebook located here:\n{notebook_path}\n")


setup(
    name='doc_insights',
    version='0.1.1',
    author='Chris Mahlke',
    author_email='Chris.Mahlke@c3.ai',
    description='A tool for validating documentation and related resources',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ChrisMahlke/doc-insights',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'ipython',
        'jupyter',
    ],
    entry_points={
        'console_scripts': [
            'doc_insights_post_install=doc_insights.post_install:post_install_message',
        ],
    },
    package_data={
        '': ['validate.ipynb'],
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
