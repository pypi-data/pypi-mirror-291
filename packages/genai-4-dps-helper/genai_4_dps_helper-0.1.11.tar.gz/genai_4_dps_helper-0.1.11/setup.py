from setuptools import find_packages, setup

setup(
    name="genai_4_dps_helper",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        # List any dependencies your library needs
        "pandas",
        "ibm_watsonx_ai",
        "pymilvus",
        "setuptools",
    ],
    description="A common library for reusable and repeated code for the GenAI4DPS Training Courses .",
    author="Benjamin Janes",
    author_email="benjamin.janes@se.ibm.com",
)
