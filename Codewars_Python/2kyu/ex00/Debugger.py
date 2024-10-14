from typing import Any, Tuple, Dict, List


class Accessor:
    def __getitem__(self, key: str):
        attribute = 'class' if key == '_class' else key
        return getattr(self, attribute)


class MethodInvocation(Accessor):
    def __init__(self, cls: type, method_name: str, arguments: Tuple, keyword_arguments: Dict):
        self._class = cls
        self.method = method_name
        self.args = arguments
        self.kwargs = keyword_arguments

    def __repr__(self):
        return f'<class: {self._class}, method: {self.method}, args: {self.args}, kwargs: {self.kwargs}>'


class AttributeOperation(Accessor):
    def __init__(self, operation: str, cls: type, attribute_name: str, value: Any):
        self.action = operation
        self._class = cls
        self.attribute = attribute_name
        self.value = value

    def __repr__(self):
        return f'<class: {self._class}, action: {self.action}, attribute: {self.attribute}, value: {self.value}>'


class Debugger:
    method_invocations: List[MethodInvocation] = []
    attribute_operations: List[AttributeOperation] = []


def wrap_function(func_name, func):
    def wrapped_function(*args, **kwargs):
        instance, *_ = args
        Debugger.method_invocations.append(MethodInvocation(cls=type(instance),
                                                            method_name=func.__name__,
                                                            arguments=args,
                                                            keyword_arguments=kwargs))
        return func(*args, **kwargs)

    return wrapped_function


class autocreate_class(type):
    def __new__(cls, name, bases, namespace):
        def get_attr(instance, attr):
            result = object.__getattribute__(instance, attr)
            Debugger.attribute_operations.append(AttributeOperation(operation='get',
                                                                    cls=type(instance),
                                                                    attribute_name=attr,
                                                                    value=result))
            return result

        def set_attr(instance, attr, value):
            Debugger.attribute_operations.append(AttributeOperation(operation='set',
                                                                    cls=type(instance),
                                                                    attribute_name=attr,
                                                                    value=value))
            object.__setattr__(instance, attr, value)

        callable_methods = {name: method for name, method in namespace.items() if not name.startswith('__') or name == '__init__'}
        for name, method in callable_methods.items():
            namespace[name] = wrap_function(name, method)
        
        new_class = super().__new__(cls, name, bases, namespace)
        new_class.__getattribute__ = get_attr
        new_class.__setattr__ = set_attr
        return new_class


class Foo(object, metaclass = autocreate_class):
    def __init__(self, x):
        self.x = x

    def bar(self, v):
        return (self.x, v)

a = Foo(1)
a.bar(2)

calls = Debugger.method_calls

test.assert_equals(len(calls), 2)

test.describe("Test collected method calls")

test.it("Call to init should be collected")
test.assert_equals(calls[0]['args'], (a, 1))

test.it("Call to bar should be collected")
test.assert_equals(calls[1]['args'], (a, 2))

test.describe("Test collected attribute accesses")
accesses = Debugger.attribute_accesses

test.assert_equals(len(accesses), 3)

test.it("Attribute set in init should be collected")
test.assert_equals(accesses[0]['action'], 'set')
test.assert_equals(accesses[0]['attribute'], 'x')
test.assert_equals(accesses[0]['value'], 1)

test.it("Method get should be collected too")
test.assert_equals(accesses[1]['action'], 'get')
test.assert_equals(accesses[1]['attribute'], 'bar')

test.it("Attribute get should be collected")
test.assert_equals(accesses[2]['action'], 'get')
test.assert_equals(accesses[2]['attribute'], 'x')