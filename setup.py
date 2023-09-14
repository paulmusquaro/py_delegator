import setuptools

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()



setuptools.setup(
      name = 'py_delegator',
      version = '0.1.7',
      description = 'The First Team Project',
      long_description= long_description,
      long_description_content_type = 'text/markdown',
      url = 'https://github.com/paulmusquaro/py_delegator.git',
      author = 'Paul Musquaro, Serhii Mahdysiuk, Leonid Hutnyk, Dmytro Avrushchenko, Dmytro Rozhko',
      author_email = 'paulren9200@ukr.net, magdisyuk228@gmail.com, leohutnyk@gmail.com, trippyfren@gmail.com, dimalikegtr@gmail.com',
      packages = setuptools.find_namespace_packages(),
      include_package_data=True,
      install_requires=['requests==2.31.0'],
      entry_points = {'console_scripts': ['py_delegator = src.py_delegator.menu:main']},
      classifiers=[
          'Programming Language :: Python :: 3',
          'License :: OSI Approved :: MIT License',
          'Operating System :: OS Independent',
      ],
      python_requires='>=3.7',
      )