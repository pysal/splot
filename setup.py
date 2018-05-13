from setuptools import setup

try:
    from distutils.command.build_py import build_py_2to3 as build_py
except ImportError:
    from distutils.command.build_py import build_py

setup(name='splot', #name of package
      version='1.0.0dev',
      description= 'plotting for PySAL',
      url= 'https://github.com/pysal/splot',
      maintainer= 'Serge Rey',
      maintainer_email= 'sjsrey@gmail.com',
      test_suite = 'nose.collector',
      tests_require=['nose'],
      keywords='spatial statistics',
      classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: GIS',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
        ],
      license='3-Clause BSD',
      packages=[],
      install_requires=['numpy', 'scipy', 'libpysal', 'mapclassify', 'palettable',
                        'esda', 'pysal',],
      zip_safe=False,
      cmdclass = {'build.py':build_py})
