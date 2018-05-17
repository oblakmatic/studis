# studis

## modules
### Python pdf
1. Install python-pdfkit:

.. code-block:: bash

	$ pip install pdfkit  (or pip3 for python3)

2. Install wkhtmltopdf:

* Debian/Ubuntu:

.. code-block:: bash

	$ sudo apt-get install wkhtmltopdf
	
* macOS:

.. code-block:: bash

	$ brew install caskroom/cask/wkhtmltopdf

**Warning!** Version in debian/ubuntu repos have reduced functionality (because it compiled without the wkhtmltopdf QT patches), such as adding outlines, headers, footers, TOC etc. To use this options you should install static binary from `wkhtmltopdf <http://wkhtmltopdf.org/>`_ site or you can use `this script <https://github.com/JazzCore/python-pdfkit/blob/master/travis/before-script.sh>`_.

* Windows and other options: check wkhtmltopdf `homepage <http://wkhtmltopdf.org/>`_ for binary installers

### Others TODO