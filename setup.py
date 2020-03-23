from setuptools import setup
from os import path

package = "splot"

# Get __version__ from package/__init__.py
with open(package + "/__init__.py", "r") as f:
    exec(f.readline())

def _get_requirements_from_files(groups_files):
    groups_reqlist = {}

    for k,v in groups_files.items():
        with open(v, 'r') as f:
            pkg_list = f.read().splitlines()
        groups_reqlist[k] = pkg_list

    return groups_reqlist

_groups_files = {
    'base': 'requirements.txt', #basic requirements
    'dev': 'requirements_dev.txt', #requirements for dev, doc, test
}

reqs = _get_requirements_from_files(_groups_files)
install_reqs = reqs.pop('base')
extras_reqs = reqs

# add long_description form README.md
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()
    
setup(name=package, #name of package
      version=__version__,
      description='Visual analytics for spatial analysis with PySAL.',
      long_description=long_description,
      long_description_content_type='text/markdown',
      url='https://github.com/pysal/splot',
      maintainer= 'Serge Rey, Stefanie Lumnitz',
      maintainer_email='sjsrey@gmail.com, stefanie.lumnitz@gmail.com',
      test_suite = 'nose.collector',
      tests_require=['nose'],
      keywords='spatial statistics visualization',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: GIS',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
        ],
      license='3-Clause BSD',
      packages=['splot'],
      include_package_data=True,
      install_requires=install_reqs,
      extras_require=extras_reqs,
      zip_safe=False)
