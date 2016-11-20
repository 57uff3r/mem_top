"""
Shows top suspects for memory leaks in your Python program.

Usage:

    pip install mem_top
    from mem_top import mem_top

    # From time to time:
    logging.debug(mem_top()) # Or just print().

Please see full description here:
https://github.com/denis-ryzhkov/mem_top/blob/master/README.md

mem_top version 0.1.3  
Copyright (C) 2014-2016 by Denis Ryzhkov <denisr@denisr.com>  
MIT License, see http://opensource.org/licenses/MIT
"""

#### import

from collections import defaultdict
import gc

#### mem_top

def mem_top(limit=10, width=100, sep='\n', refs_format='{num}\t{type} {obj}', types_format='{num}\t {obj}', verbose_types=None, verbose_file_name='/tmp/mem_top'):

    gc.collect()
    objs = gc.get_objects()

    nums_by_types = defaultdict(int)
    reprs_by_types = defaultdict(list)

    for obj in objs:
        _type = type(obj)
        nums_by_types[_type] += 1
        if verbose_types and _type in verbose_types:
            reprs_by_types[_type].append(repr(obj))

    if verbose_types:
        verbose_result = sep.join(sep.join(
            types_format.format(num=len(s), obj=s[:width])
            for s in sorted(reprs_by_types[_type], key=lambda s: -len(s))
        ) for _type in verbose_types)

        if verbose_file_name:
            with open(verbose_file_name, 'w') as f:
                f.write(verbose_result)
        else:
            return verbose_result

    return sep.join((
        '',
        'refs:',
        _top(limit, width, sep, refs_format, (
            (len(gc.get_referents(obj)), obj) for obj in objs
        )),
        '',
        'types:',
        _top(limit, width, sep, types_format, (
            (num, _type) for _type, num in nums_by_types.items()
        )),
        '',
    ))

#### _top

def _top(limit, width, sep, format, nums_and_objs):
    return sep.join(
        format.format(num=num, type=type(obj), obj=repr(obj)[:width])
        for num, obj in sorted(nums_and_objs, key=lambda num_obj: -num_obj[0])[:limit]
    )

#### tests

if __name__ == '__main__':
    print(mem_top())
