#!/usr/bin/env python
# -*- coding: utf-8; py-indent-offset:4 -*-
###############################################################################
# Copyright (C) 2020 Daniel Rodriguez
# Use of this source code is governed by the MIT License
###############################################################################
import textwrap

from . import linesholder
from . import params as metaparams

__all__ = []


def wrap_indent(txt, ilevel=0, ichar='    ', width=78, cr=1):
    ifill = (ilevel + 1) * ichar
    wrapped_lines = []
    for line in txt.splitlines():
        wrapped = textwrap.wrap(
            line,
            initial_indent=ifill,
            subsequent_indent=ifill,
            # drop_whitespace=False,
            replace_whitespace=False,
            width=width,
        )
        wrapped_lines.extend(wrapped)

    return '\n'*cr + '\n'.join(wrapped_lines)


def _generate(cls, bases, dct, **kwargs):
    # Get actual docstring

    cls.__doc_orig__ = clsdoc = (cls.__doc__ or '').lstrip('\n').rstrip()
    gendoc = clsdoc

    if getattr(cls, 'alias', None):
        txt = '\n'
        txt += 'Aliases: ' + ', '.join(cls.alias)
        gendoc += wrap_indent(txt, cr=2)

    if getattr(cls, 'inputs', None):
        txt = '\n'
        txt += 'Inputs: ' + ', '.join(cls.inputs)
        gendoc += wrap_indent(txt, cr=2)

    if getattr(cls, 'outputs', None):
        txt = '\n'
        txt += 'Outputs: ' + ', '.join(cls.outputs)
        gendoc += wrap_indent(txt, cr=2)

    if getattr(cls, 'params', None):
        txt = '\n'
        txt += 'Params:'
        gendoc += wrap_indent(txt, cr=2)

        pinfo = metaparams.get_pinfo(cls)
        for name, val in cls.params.items():
            if isinstance(val, str):
                val = "'{}'".format(val)
            elif isinstance(val, linesholder.LinesHolder):
                val = val.__name__

            txt = ''
            txt += '\n  - {} (default: {})'.format(name, val)

            pdoc = pinfo.get(name, {}).get('doc', '')
            if pdoc:
                txt += '\n\n    {}'.format(pdoc)

            gendoc += wrap_indent(txt, cr=1)

    _talib = getattr(cls, '_talib', None)
    if _talib:  # must be mehot
        tadoc = getattr(_talib, '__doc__', '') or ''
        if tadoc:
            txt = 'TA-LIB (with compatibility flag "_talib=True"):'
            gendoc += wrap_indent(txt, cr=2)
            gendoc += wrap_indent('  - ' + tadoc)

    cls.__doc__ = gendoc
