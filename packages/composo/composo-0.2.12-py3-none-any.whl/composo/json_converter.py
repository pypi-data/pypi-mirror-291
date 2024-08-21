from http import client
import json
import datetime
from decimal import Decimal
from collections import OrderedDict, namedtuple
from dataclasses import dataclass


def anything_to_python(obj):
    """
    Converts any object to a native Python object (dict, list, str, etc.)
    """
    def default_serializer(x):
        if isinstance(x, datetime.datetime):
            return x.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(x, Decimal):
            return float(x)
        elif isinstance(x, complex):
            return {"real": x.real, "imag": x.imag}
        elif isinstance(x, (set, frozenset)):
            return list(x)
        elif isinstance(x, bytes):
            return x.decode('utf-8')
        elif isinstance(x, tuple) and hasattr(x, '_fields'):  # Check if it's a namedtuple
            return dict(zip(x._fields, x))
        elif hasattr(x, '__dict__'):
            return {k: v for k, v in x.__dict__.items() if not k.startswith('_')}
        elif hasattr(x, '__slots__'):
            return {slot: getattr(x, slot) for slot in x.__slots__ if hasattr(x, slot)}
        elif callable(x):
            return str(x)
        return str(x)

    def recursive_convert(item):
        if isinstance(item, (dict, OrderedDict)):
            return {str(k): recursive_convert(v) for k, v in item.items()}
        elif isinstance(item, (list, tuple, set, frozenset)):
            return [recursive_convert(i) for i in item]
        elif hasattr(item, '__dict__') or hasattr(item, '__slots__'):
            return recursive_convert(default_serializer(item))
        else:
            try:
                json.dumps(item)
                return item
            except TypeError:
                return default_serializer(item)

    if isinstance(obj, bytes):
        obj = obj.decode('utf-8')
    
    return recursive_convert(obj)

def assert_casting(cast, compare):
    casted = anything_to_python(cast)
    
    if casted != compare:
        print(f"ERROR: {casted} is not equal to {compare}")
    else:
        print(f"{casted} is equal to {compare}")

def flexible_assert_casting(cast, compare):
    casted = anything_to_python(cast)
    
    if isinstance(compare, dict):
        if not all(key in casted and casted[key] == value for key, value in compare.items()):
            print(f"ERROR: Not all required fields from {compare} are present in {casted}")
        else:
            print(f"All required fields from {compare} are present in {casted}")
    elif isinstance(compare, list):
        if not all(item in casted for item in compare):
            print(f"ERROR: Not all required items from {compare} are present in {casted}")
        else:
            print(f"All required items from {compare} are present in {casted}")
    else:
        if casted != compare:
            print(f"ERROR: {casted} is not equal to {compare}")
        else:
            print(f"{casted} is equal to {compare}")


# TESTS
if __name__ == "__main__":
    
    #####
    # assert_casting tests strictly
    #####
    assert_casting("hello", "hello")
    
    assert_casting(1, 1)
    
    assert_casting([1, 2, 3], [1, 2, 3])
    
    assert_casting({"a": 1, "b": 2}, {"a": 1, "b": 2})
    
    assert_casting({"a": 1, "b": [1, 2, 3]}, {"a": 1, "b": [1, 2, 3]})
    
    @dataclass
    class Test:
        a: int
        b: str
        
    assert_casting(Test(1, "hello"), {"a": 1, "b": "hello"})
    
    # Test with datetime object
    assert_casting(datetime.datetime(2023, 5, 17), "2023-05-17 00:00:00")

    # Test with Decimal
    assert_casting(Decimal('3.14'), 3.14)
    
    # Test with OrderedDict
    od = OrderedDict([('a', 1), ('b', 2), ('c', 3)])
    assert_casting(od, {"a": 1, "b": 2, "c": 3})
    
    # Test with bytes
    assert_casting(b'hello', "hello")

    ##### 
    # flexible_assert_casting tests that the fields are simply present in the casted object
    #####
    # Test with complex number
    flexible_assert_casting(complex(1, 2), {"real": 1, "imag": 2})

    # Test with custom object without __dict__
    class CustomObj:
        def __init__(self):
            self.attr = 'value'
    flexible_assert_casting(CustomObj(), {"attr": "value"})

    # Test with namedtuple
    Point = namedtuple('Point', ['x', 'y'])
    p = Point(11, y=22)
    flexible_assert_casting(p, [11, 22])

    # Test with nested custom objects
    class Outer:
        def __init__(self):
            self.inner = Inner()
    class Inner:
        def __init__(self):
            self.value = 42
    flexible_assert_casting(Outer(), {"inner": {"value": 42}})

    # Test with set
    flexible_assert_casting({1, 2, 3}, [1, 2, 3])
    
    import openai
    client = openai.Client(api_key="sk-123", project="project-123")
    flexible_assert_casting(client, {"api_key": "sk-123", "project": "project-123"})