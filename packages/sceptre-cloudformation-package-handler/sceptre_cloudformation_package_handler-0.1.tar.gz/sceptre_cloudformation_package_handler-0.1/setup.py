from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="sceptre-cloudformation-package-handler",
    version="0.1",
    author="Trinopoty Biswas",
    author_email="trinopoty@outlook.com",
    description="A template handler for cloudformation package command.",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/trinopoty/sceptre-cloudformation-package-handler",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    py_modules=["sceptre-cloudformation-package-handler"],
    entry_points={
        'sceptre.template_handlers': [
            'cloudformation_package = sceptre_cloudformation_package_handler:PackagedTemplate'
        ],
    },
)
