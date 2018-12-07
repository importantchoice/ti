=================================
ti -- A silly simple time tracker
=================================

``ti`` is a small command line time-tracking application.
Simple basic usage looks like this::

    $ ti start my-project
    $ ti stop

You can also give it human-readable times::

    $ ti start my-project 9:15

``ti`` sports many other cool features. Read along to discover.

Wat?
====

``ti`` is a simple command line time tracker. It has been completely rewritten
in Python (originally a bash script) and has (almost) complete test coverage. It
is inspired by `timed <http://adeel.github.com/timed>`_, which is a nice project
that you should check out if you don't like ``ti``. ``ti`` also takes
inspiration from the simplicity of `t <http://stevelosh.com/projects/t/>`_.

If a time-tracking tool makes me think for more than 3-5 seconds, I lose my line
of thought and forget what I was doing. This is why I created ``ti``. With
``ti``, you'll be as fast as you can type, which you should be good with anyway.

The most important part about ``ti`` is that it provides just a few commands to
manage your time-tracking and then gets out of your way.

All data is saved in a JSON file ,``~/.ti-sheet``. (This can be changed using the
``$SHEET_FILE``  environment variable.) The JSON is easy to access and can be
processed into other more stylized documents. Some ideas:

- Read your JSON file to generate beautiful HTML reports.
- Build monthly statistics based on tags or tasks.
- Read your currently working project and display it in your terminal prompt.
  Maybe even with the number of hours you've been working.

It's *your* data.

Oh and by the way, the source is a fairly small Python script, so if you know
Python, you may want to skim over it to get a better feel of how it works.

*Note*: If you have used the previous bash version of ``ti``, which was horribly
tied up to only work on Linux, you might notice the lack of plugins in this
Python version. I am not really missing them, so I might not add them. If anyone
has any interesting use cases for it, I'm willing to consider.

Usage
=====

Here's the minimal usage style::

    $ ti start my-project 12:00
    Start working on my-project.

    $ ti status
    You have been working on my-project for less than a minute.

    $ ti stop 12:30
    So you stopped working on my-project.

``start`` and ``stop`` can take a time (format described further down) at which to
apply the action::

Put brief notes on what you've been doing::

    $ ti note waiting for Napoleon to take over the world
    $ ti n another simple note for demo purposes

Tag your activities for fun and profit::

    $ ti tag imp

Get a log of all activities with the ``log`` (or ``l``) command::

    $ ti log

Get a list of all activities in CSV format, so that they can be imported into your favourite spreadsheet editor

    $ ti csv
    $ ti --no-color csv | grep 2018-01 #will show all entries you logged in January 2018

Get a report for your project:

    $ ti report customeur
    $ ti report customeur | grep 2018-10

Gimme!
======

You can download ``ti`` `from the source on
GitHub <https://raw.github.com/tbekolay/ti/master/bin/ti>`_.

- Put it somewhere in your ``$PATH`` and make sure it has executable permissions.
- Install ``pyyaml`` using the command ``pip install --user pyyaml``.
- Install ``colorama`` using the command ``pip install --user colorama``.

After that, ``ti`` should be working fine.

Also, visit the `project page on GitHub <https://github.com/tbekolay/ti>`_ for
any further details.

Who?
====

Originally created and fed by Shrikant Sharat
(`@sharat87 <https://twitter.com/#!sharat87>`_).
and
(`@tbekolay <https://github.com/tbekolay>`_) and friends on GitHub.

License
=======

`MIT License <http://mitl.sharats.me>`_.
