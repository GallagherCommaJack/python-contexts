from typing import Dict, Any, List, Optional, Callable


class Context:
    def __init__(self, **kwargs: Any) -> None:
        self.inner = {k: [v] for k, v in kwargs.items()}

    def __getitem__(self, key: str) -> Any:
        return self.inner[key][-1]

    def __setitem__(self, key: str, value: Any) -> None:
        if key not in self.inner:
            self.inner[key] = [value]
        else:
            self.inner[key][-1] = value

    def keys(self) -> List[str]:
        return list(self.inner.keys())

    def vals(self) -> List[Any]:
        return [self[k] for k in self.keys()]

    def items(self) -> List[Tuple[str, Any]]:
        return [(k, self[k]) for k in self.keys()]


default = Context()


def push(
    __ctx=default,
    **kwargs,
):
    for k, v in kwargs.items():
        if k not in __ctx.inner:
            __ctx.inner[k] = [v]
        else:
            __ctx.inner[k].append(v)


def get_dict(
    *keys: str,
    __ctx=default,
    default_fn: Optional[Callable[[str], Any]] = None,
) -> Dict[str, Any]:
    results = {}
    for key in keys:
        if key in __ctx.inner:
            results[key] = __ctx.inner[key][-1]
        elif default_fn:
            results[key] = default_fn(key)
    return results


def pop_many(
    *keys: str,
    __ctx=default,
    strict: bool = False,
    default_fn: Optional[Callable[[str], Any]] = None,
) -> Dict[str, Any]:
    if strict:
        for key in keys:
            if key not in __ctx.inner:
                raise KeyError(f"Key {key} not in context")
    results = {}
    for key in keys:
        if key in __ctx.inner:
            results[key] = __ctx.inner[key].pop()
            if __ctx.inner[key] == []:
                del __ctx.inner[key]
        elif default_fn:
            results[key] = default_fn(key)
    return results


class Override:
    """
    helper object for pushing and popping context in a scope
    """

    def __init__(self, __ctx=default, **kwargs):
        self.inner = __ctx
        self.overrides = kwargs

    def __enter__(self):
        push(self.inner, **self.overrides)

    def __exit__(self, exc_type, exc_value, traceback):
        pop_many(self.inner, *self.overrides.keys())


def override(__ctx=default, **kwargs):
    return Override(__ctx, **kwargs)
