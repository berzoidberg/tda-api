from colorama import Fore, Back, Style, init

import difflib
import json
import asynctest
import inspect

def account_principals():
    with open('tests/testdata/principals.json', 'r') as f:
        return json.load(f)


def real_order():
    return {
        'session': 'NORMAL',
        'duration': 'DAY',
        'orderType': 'MARKET',
        'complexOrderStrategyType': 'NONE',
        'quantity': 1.0,
        'filledQuantity': 1.0,
        'remainingQuantity': 0.0,
        'requestedDestination': 'AUTO',
        'destinationLinkName': 'ETMM',
        'price': 58.41,
        'orderLegCollection': [
            {
                'orderLegType': 'EQUITY',
                'legId': 1,
                'instrument': {
                    'assetType': 'EQUITY',
                    'cusip': '126650100',
                    'symbol': 'CVS'
                },
                'instruction': 'BUY',
                'positionEffect': 'OPENING',
                'quantity': 1.0
            }
        ],
        'orderStrategyType': 'SINGLE',
        'orderId': 100001,
        'cancelable': False,
        'editable': False,
        'status': 'FILLED',
        'enteredTime': '2020-03-30T15:36:12+0000',
        'closeTime': '2020-03-30T15:36:12+0000',
        'tag': 'API_TDAM:App',
        'accountId': 100000,
        'orderActivityCollection': [
            {
                'activityType': 'EXECUTION',
                'executionType': 'FILL',
                'quantity': 1.0,
                'orderRemainingQuantity': 0.0,
                'executionLegs': [
                    {
                        'legId': 1,
                        'quantity': 1.0,
                        'mismarkedQuantity': 0.0,
                        'price': 58.1853,
                        'time': '2020-03-30T15:36:12+0000'
                    }
                ]
            }
        ]
    }


class MockResponse:
    def __init__(self, json, ok, headers=None):
        self._json = json
        self.ok = ok
        self.headers = headers if headers is not None else {}

    def json(self):
        return self._json


class AsyncMagicMock:
    """
    Simple mock that returns a asynctest.CoroutineMock instance for every
    attribute. Useful for mocking async libraries
    """
    def __init__(self):
        self.__attr_cache = {}

    def __getattr__(self, key):
        attr_cache = super().__getattribute__('_AsyncMagicMock__attr_cache')
        if key == '_AsyncMagicMock__attr_cache': return attr_cache

        try:
            return super().__getattribute__(key)
        except AttributeError:
            if key not in attr_cache:
                attr_cache[key] = asynctest.CoroutineMock()
            return attr_cache[key]

    def __setattr__(self, key, val):
        if key == '_AsyncMagicMock__attr_cache':
            return super().__setattr__(key, val)
        attr_cache = super().__getattribute__('_AsyncMagicMock__attr_cache')
        attr_cache[key] = val

    def __hasattr__(self, key):
        attr_cache = super().__getattribute__('_AsyncMagicMock__attr_cache')
        return attr_cache.has_key(key)

    def reset_mock(self):
        self.__attr_cache.clear()

def has_diff(old, new):
    old_out = json.dumps(old, indent=4, sort_keys=True).splitlines()
    new_out = json.dumps(new, indent=4, sort_keys=True).splitlines()
    diff = difflib.ndiff(old_out, new_out)
    diff, has_diff = color_diff(diff)

    if has_diff:
        print('\n'.join(diff))
    return has_diff


def color_diff(diff):
    has_diff = False
    output = []
    for line in diff:
        if line.startswith('+'):
            output.append(Fore.GREEN + line + Fore.RESET)
            has_diff = True
        elif line.startswith('-'):
            output.append(Fore.RED + line + Fore.RESET)
            has_diff = True
        elif line.startswith('^'):
            output.append(Fore.BLUE + line + Fore.RESET)
            has_diff = True
        else:
            output.append(line)
    return output, has_diff


__NO_DUPLICATES_DEFINED_NAMES = set()


def no_duplicates(f):
    name = f.__qualname__
    if name in __NO_DUPLICATES_DEFINED_NAMES:
        raise AttributeError('duplicate definition of {}'.format(name))
    __NO_DUPLICATES_DEFINED_NAMES.add(name)
    return f

