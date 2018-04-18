############
RSTExtras
############

This module implements a series of extensions for Sphinx and Docutils, including abstracts, shell blocks and an updated link role.

Installation
===============

.. code-block:: console

   $ python setup.py install --user

  
Configuration
===============

Import the module into your Sphinx ``conf.py`` file.

.. code-block:: py

   import rstextras
   extensions = ['rstextras']

Currently, the only configuration option is ``rstextras_prompt``, which controls how RSTExtras renders the content of shell blocks.

.. code-block:: py

   rstextras_prompt = {
      "m": {
         "ps1": "MariaDB> ",
         "ps2": "         ",
         "lang": "sql"},
      "$": {
         "ps1": "$ ",
         "ps2": "      ",
         "lang": "sh"},
      "#": {
         "ps1": "# ",
         "ps2": "      ",
         "lang": "sh"}
   }

Note: At the moment, shell blocks do **not** provide syntax highlighting. The ``lang`` variable is unused, but stored on the controlling class for future application.

Usage
=======

Shell Block
--------------

Sphinx handles the displaying program code through a directive called the ``code-block``. Code blocks are very effective in rendering snippets from programs, (i.e., your particular ``.c`` or ``.py`` files, for instance), but they are less effective when it comes to shells.

Shells have prompts, as well as sections of code that user writes and sections that the system outputs.  When applying this paradigm to a code block, Sphinx, Docutils or Pygments applies syntax highlighting to the entire block, rather than just those sections where applicable.

This behavior can prove confusing in cases such as a MariaDB client instance, as it can result in inconsistent highlighting applied to error messages and the result-set.

By default, the shell block renders all content without syntax highlighting of any kind. Lines indicated as user input are bolded, with configured prompts for further emphasis.

For instance,

.. code-block:: rst

   .. shell-block::

      m>  SELECT * FROM table_name
      ->  WHERE id = 1;

      +----+----+
      | A  | B  |
      +----+----+
      |  1 |  3 |
      +----+----+

Using the configuration given above, ``m>`` prompts translate to ``MariaDB> ``, while the generic PS2 prompt of ``->`` is replaced by enough spaces to line the text up with the initial position in the PS1 prompt.  The SQL statment is placed in bold, but not highlighted (we're still looking into how to highlight it properly).  The unmarked lines of the result-set table are rendered without markup as additional text in the ``<pre>`` block.


Abstract
----------

The ``abstract`` directive allows you to create a limited metadata statement for use with the ``link`` role and other tools. By default, abstracts are hidden from view.  In order to use an abstract, you must add a slug to the line immediately above, (as shown below).

.. code-block:: rst

   .. _`sql-select`:

   .. abstract:: ``SELECT``

      Retrieves data from the table.

During the collection phase, Sphinx stores the first element as a title and the remainder as a description.


Link
---------

Using the ``link`` role you can generate links in your document.  It is similar to the ``ref`` role in that it matches to slugs, but is designed specifically to work with the ``abstract`` directive.

When Sphinx processes a ``link``, it doesn't just auto-generate the ``href``.  It draws the link content from the first line of the abstract, so you don't have to worry about old titles floating around as links in your document.  Additionally, it uses the body of the abstract to generate hover text. 

This means that:

.. code-block:: rst

   The :link:`sql-select` statement...

the link in this text renders ``SELECT`` with the appropriate formatting, (as defined in the abstract).  In HTML it also pulls a description of the ``SELECT`` statement from the ``abstract`` directive. So, hovering your mouse over the text raises a small block with a short explanation of what the statement does.  So, you can quickly reference the text without jumping to another page.

.. note:: More coming.



