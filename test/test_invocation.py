#! /usr/bin/env python

import sys
import os
import logging
import platform
import hiyapyco

sys.path.insert(
        0,
        os.path.join(
            os.path.dirname(
                os.path.realpath(os.path.abspath(sys.argv[0]))
                ),
            'lib'
            )
        )
import testsetup

logger = testsetup.setup(sys.argv[1:])

basepath = os.path.dirname(os.path.realpath(__file__))

print('start test %s using python %s (loglevel:%s)' %
        (__file__, platform.python_version(), logging.getLevelName(logger.getEffectiveLevel()))
    )

logger.info('basic invocation test ...')
conf = hiyapyco.HiYaPyCo(
        os.path.join(basepath, 'base.yaml'),
        method=hiyapyco.METHOD_SIMPLE,
        failonmissingfiles=True
        )

logger.info('test kwarg nonbool ...')
try:
    conf = hiyapyco.HiYaPyCo(
            os.path.join(basepath, 'base.yaml'),
            interpolate='ABC'
            )
    raise Exception('we should newer get here: missing exception')
except hiyapyco.HiYaPyCoInvocationException as e:
    assert str(e).startswith('value of "interpolate" must be boolean')
try:
    conf = hiyapyco.HiYaPyCo(
            os.path.join(basepath, 'base.yaml'),
            usedefaultyamlloader='ABC'
            )
    raise Exception('we should newer get here: missing exception')
except hiyapyco.HiYaPyCoInvocationException as e:
    assert str(e).startswith('value of "usedefaultyamlloader" must be boolean')
try:
    conf = hiyapyco.HiYaPyCo(
            os.path.join(basepath, 'base.yaml'),
            failonmissingfiles='ABC'
            )
    raise Exception('we should newer get here: missing exception')
except hiyapyco.HiYaPyCoInvocationException as e:
    assert str(e).startswith('value of "failonmissingfiles" must be boolean')

logger.info('test undef kwarg ...')
try:
    conf = hiyapyco.HiYaPyCo(x=1)
    raise Exception('we should newer get here: missing exception')
except hiyapyco.HiYaPyCoInvocationException as e:
    assert '%s' % e == 'undefined keywords: x'

logger.info('test methods ...')
try:
    conf = hiyapyco.HiYaPyCo(method=666)
    raise Exception('we should newer get here: missing exception')
except hiyapyco.HiYaPyCoInvocationException as e:
    assert '%s' % e == 'undefined method used, must be one of: %s' % ' '.join(hiyapyco.METHODS.keys())

logger.info('test no yaml defined ...')
try:
    conf = hiyapyco.HiYaPyCo()
    raise Exception('we should newer get here: missing exception')
except hiyapyco.HiYaPyCoInvocationException as e:
    assert '%s' % e == 'no yaml files defined'

logger.info('test missing file ...')
try:
    conf = hiyapyco.HiYaPyCo('nosuchfile.yaml')
    raise Exception('we should newer get here: missing exception')
except hiyapyco.HiYaPyCoInvocationException as e:
    assert '%s' % e == 'yaml file not found: \'nosuchfile.yaml\''

logger.info('test normal file list')
conf = hiyapyco.load(
        os.path.join(basepath, 'base.yaml'),
        os.path.join(basepath, 'baseext.yaml'),
        method=hiyapyco.METHOD_SIMPLE,
        failonmissingfiles=True
        )

logger.info('test files as list')
conf = hiyapyco.load(
        [
            os.path.join(basepath, 'base.yaml'),
            os.path.join(basepath, 'baseext.yaml')
        ],
        method=hiyapyco.METHOD_SIMPLE,
        failonmissingfiles=True
        )


print('passed test %s' % __file__)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4 smartindent nu

