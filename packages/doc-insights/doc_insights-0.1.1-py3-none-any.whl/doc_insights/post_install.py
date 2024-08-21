# doc_insights/post_install.py

import os

def post_install_message():
    notebook_path = os.path.join(os.path.dirname(__file__), '../validate.ipynb')
    print("\nThank you for installing doc_insights!")
    print("Please visit the README.md file in the package directory for further instructions.")
    print("Or visit: https://github.com/ChrisMahlke/doc-insights for more details.")
    print(f"\nTo get started, you can run the example notebook located here:\n{notebook_path}\n")
