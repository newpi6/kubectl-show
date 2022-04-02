import setuptools
from setuptools import setup, find_packages
from setuptools.command.install_scripts import install_scripts
import shutil


class InstallScripts(install_scripts):

    def run(self):
        setuptools.command.install_scripts.install_scripts.run(self)

        # Rename some script files
        for script in self.get_outputs():
            if script.endswith(".py") or script.endswith(".sh"):
                dest = script[:-3]
            else:
                continue
            print("moving %s to %s" % (script, dest))
            shutil.move(script, dest)


# Do not edit these constants. They will be updated automatically
# by scripts/update-client.sh.
CLIENT_VERSION = "22.1.0.9"
PACKAGE_NAME = "kubectl-show"
# DEVELOPMENT_STATUS = "4 - Beta"
DEVELOPMENT_STATUS = "5 - Production/Stable"

# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

EXTRAS = {
    # 'adal': ['adal>=1.0.2']
}
REQUIRES = []
with open('requirements.txt') as f:
    for line in f:
        line, _, _ = line.partition('#')
        line = line.strip()
        if ';' in line:
            requirement, _, specifier = line.partition(';')
            for_specifier = EXTRAS.setdefault(':{}'.format(specifier), [])
            for_specifier.append(requirement)
        else:
            REQUIRES.append(line)

# with open('test-requirements.txt') as f:
#     TESTS_REQUIRES = f.readlines()

setup(

    name=PACKAGE_NAME,
    version=CLIENT_VERSION,
    description="kubectl python plugin",
    author_email="",
    author="harvey",
    license="MIT",
    url="https://github.com/newpi6/kubectl-show.git",
    keywords=["kubectl", "Kubernetes"],
    install_requires=REQUIRES,
    # tests_require=TESTS_REQUIRES,
    extras_require=EXTRAS,
    packages=find_packages(exclude=['tests.*', 'tests']),
    include_package_data=True,
    long_description="kubectl python plugin https://github.com/newpi6/kubectl-show.git",
    python_requires='>=3.6',
    entry_points={
        'console_scripts': ['kubectl-show=kubectl_show.main:main'],
    },
    classifiers=[
        "Development Status :: %s" % DEVELOPMENT_STATUS,
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    # scripts=['kubectl_show/main.py', ],
    # cmdclass={"install-scripts": InstallScripts},
)
