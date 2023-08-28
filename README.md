# pylizard

This package is made to speed up the process of building scripts which interact with the Lizard v4 API. The package is open source, so feel free to contribute. The aim is to eventually support all endpoints of the Lizard api v4.


## Installation

The package is installed with:

    $ pip install git+https://github.com/JJFlorian/pylizard


## Usage

Import the package as:

    $ import pylizard.pylizard as liz

Now all the functions and classes can be used. For example:

    $ headers = liz.get_headers('YOUR_API_KEY')
    $ organisation = liz.Organisation(name='YOUR_ORGANISATION_NAME')