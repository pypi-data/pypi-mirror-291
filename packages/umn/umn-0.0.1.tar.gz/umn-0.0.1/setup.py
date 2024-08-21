import setuptools

#working_directory = path.abspath(path.dirname(__file__))

with open('README.md',"r") as fh:
    long_description = fh.read()

setuptools.setup(
                name="umn",
                version="0.0.1",

                #url="https://github.com/umngit/my_package_umn",  # or your project URL
                author="Umeshn7Codes",
                #author_email="umesh.srivatsa@gmail.com",

                description="This is for testing the python package umn",
                long_description= long_description, #open(r"C:\1_ESI_INDIA\Work\2_SYSTEMS_AND_TOOLS\1_PYTHON_UMN\my_package_umn\README.md").read(),
                long_description_content_type="text/markdown",

                #packages=find_packages(),
                python_requires='>=3.6',

)
