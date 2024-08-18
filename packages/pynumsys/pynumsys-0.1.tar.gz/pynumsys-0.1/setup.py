from distutils.core import setup
setup(
  name = 'pynumsys',         # How you named your package folder (MyLib)
  packages = ['pynumsys'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Python package to convert one number system to another such as '
                'binary to decimal, decimal to binary, hexadecimal to octal, octal to hexadecimal etc...',   # Give a short description
  # about your library
  author = 'Roshaan Mehmood',                   # Type in your name
  author_email = 'roshaan55@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/roshaan555/pynumsys',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/roshaan555/pynumsys/releases/download/v_0.1/pynumsys-0.1.tar.gz',    # I explain this later on
  keywords = ['pynumsys', 'numbersystem', 'octal to hexadecimal', 'binary to octal', 'binary', 'decimal'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          '',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
    'Programming Language :: Python :: 3.10',
    'Programming Language :: Python :: 3.11',
    'Programming Language :: Python :: 3.12',
  ],
)