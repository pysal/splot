from setuptools import setup


setup(name='splot', #name of package
      version='1.0.0',
      description= 'plotting for PySAL',
      url= 'https://github.com/pysal/splot',
      maintainer= 'Serge Rey, Stefanie Lumnitz',
      maintainer_email= 'sjsrey@gmail.com, stefanie.lumnitz@gmail.com',
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
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7'
        ],
      license='3-Clause BSD',
      packages=['splot'],
      include_package_data=True,
      install_requires=['numpy', 'libpysal', 'mapclassify', 'geopandas',
                        'esda', 'spreg', 'giddy', 'matplotlib', 'seaborn'],
      zip_safe=False)
