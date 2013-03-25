========================
Wunderlist Task Exporter
========================

Introduction
------------
I wrote this to export my tasks in an easy format from the Wunderlist page.
The Wunderlist API is not documented but they provide helpful error messages
and have a clean structure (for those parts I used at least). My script does
only a bare minimum but should be enough to give everyone an idea of how it
works.


Configuration
-------------

    $ cp wunderlist_config.py.sample wunderlist_config.py
    $ vim wunderlist_config.py

Enter username and password.


Usage
-----
Just run it with `python wunderlist_parser.py` and it will take some time to
load all lists and their tasks. The final data will be organized as a dict
with one entry for each list. The key is the internal ID (really only
important for matching task and list) and the value is a tuple: The first
element is the title of the list, the second one is a list of all tasks in
that list.

The tasks themselves are organized as classes as they are somewhat complex and
that makes it easier to write an for them. Take a look at the `Task` class to
see what is accessible and how (the names really don't need any explanation).

Currently, the script just spits out the final result at the end. If you want
something different, you can actually build on top of that: Delete the printing
lines and just import the file as a module. Then access 
`wunderlist_parser.lists` and you have your result: All tasks of all lists,
including those already completed.


Contribute
----------
This is only a **very** basic script that just achieves what I needed: A clean
data representation to organize the data. If you need more functionality, just
add it. I will then be happy to incorporate your changes here.

If you clean up the module to make it less dirty, I will also gladly include
it.
