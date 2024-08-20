from setuptools import setup, find_packages

setup(
    name="Machina Sports Core SDK",
    version="0.1.15",
    description="Machina Core SDK",
    author="Fernando Bombassaro Martins",
    author_email="fernando@machina.gg",
    packages=find_packages(where="src"),  # Look inside the `src` directory
    package_dir={"": "src"},
    install_requires=[
        "requests>=2.26.0,<3.0.0",
        "pydantic>=1.8.2,<2.0.0"
    ],
    python_requires=">=3.9,<4.0"
)
