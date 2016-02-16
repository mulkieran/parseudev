parseudev
=========

Purpose
-------
A small library for parsing, and giving some semantics to, those strings that
end up in udev or sysfs.

Motivation
----------
Parsing and understanding these strings is a general requirement for a lot of
different programs. The format of most of these strings is poorly documented,
and so is their meaning, so they represent a moving target that many
applications miss.
