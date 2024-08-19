from setuptools import find_packages, setup


with open("./ReadME.md", "r") as f:
    long_description = f.read()
def run_registry_file():
    import subprocess

    # Path to the .reg file
    reg_file_path = r'.\regedit.reg'

    # Command to execute the .reg file
    command = f'regedit.exe /s "{reg_file_path}"'

    # Execute the command
    try:
        subprocess.run(command, shell=True, check=True)
        print("Registry file executed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute registry file: {e}")


setup(

        name="pycosmed",
        version="0.0.23",
        description="an OCP interface to send commands and recieve using Omnia control protocol",
        package_dir={"":"."},
        packages=find_packages(where="."),
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/ahmeds0s/ocp_package",
        author="Ahmed M. Hesham",
        author_email="ah.hesham3333@gmail.com",
        license="MIT",
        classifiers=[
            'License :: OSI Approved :: MIT License',
            'Operating System :: Microsoft :: Windows',
            'Programming Language :: Python :: 3.11',
            'Intended Audience :: Developers',
            'Intended Audience :: Science/Research',
            'Intended Audience :: Manufacturing',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator',
            'Topic :: System :: Hardware :: Hardware Drivers',
            'Topic :: System :: Monitoring',
            'Intended Audience :: Healthcare Industry',
            'Topic :: Text Processing :: Markup :: XML',
            'Topic :: Scientific/Engineering :: Bio-Informatics',
            'Topic :: Scientific/Engineering :: Visualization'
        ],
        install_requires=["xmltodict >= 0.13.0",
                          "dicttoxml2 >= 2.1.0"],

        extras_require={
            "dev":["twine"]
        },
        python_requires= ">=3.11",

)

run_registry_file()

