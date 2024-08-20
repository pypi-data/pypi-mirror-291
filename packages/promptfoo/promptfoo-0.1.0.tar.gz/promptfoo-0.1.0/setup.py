from setuptools import setup, find_packages

setup(
   name="promptfoo",
   version="0.1.0",
   packages=find_packages(where="src"),
   package_dir={"": "src"},
   entry_points={
       "console_scripts": [
           "promptfoo=promptfoo.main:main",
       ],
   },
   author="Ian Webster",
   author_email="ian@promptfoo.dev",
   description="LLM evals and red teaming",
   long_description=open("README.md").read(),
   long_description_content_type="text/markdown",
   url="https://github.com/promptfoo/promptfoo",
   classifiers=[
       "Programming Language :: Python :: 3",
       "License :: OSI Approved :: MIT License",
       "Operating System :: OS Independent",
   ],
   python_requires=">=3.6",
)
