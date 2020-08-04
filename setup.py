import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="packagetracker", # Replace with your own username
    version="1.0",
    author="Wasi Ahmed, Areeq Hasan",
    author_email="wasi.shams.ahmed@gmail.com",
    description="Shipment Tracker API used to conveniently implement in code to track packages that are carried by UPS, USPS, and FEDEX",
    long_description="Shipment Tracker API used to conveniently implement in code to track packages that are carried by UPS, USPS, and FEDEX",
    long_description_content_type="text/markdown",
    url="https://github.com/wahmed937/packagetracker",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
