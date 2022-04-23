from typing import Dict, Any, List, Optional, Callable


class Context:
    def __init__(self, **kwargs: Any) -> None:
        self.inner = {k: [v] for k, v in kwargs.items()}


default_ctx = Context()


def push(
    __ctx=default_ctx,
    **kwargs,
):
    for k, v in kwargs.items():
        if k not in __ctx.inner:
            __ctx.inner[k] = [v]
        else:
            __ctx.inner[k].append(v)


def get_dict(
    *keys: str,
    __ctx=default_ctx,
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
    __ctx=default_ctx,
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

    def __init__(self, __ctx=default_ctx, **kwargs):
        self.inner = __ctx
        self.overrides = kwargs

    def __enter__(self):
        push(self.inner, **self.overrides)

    def __exit__(self, exc_type, exc_value, traceback):
        pop_many(self.inner, *self.overrides.keys())


def override(__ctx=default_ctx, **kwargs):
    return Override(__ctx, **kwargs)


class EnterContext:
    def __init__(self, __ctx=default_ctx, **kwargs):
        self.ctx = ctx
        self.overrides = kwargs

    def __enter__(self):
        push(self.ctx, **self.overrides)
        for k, v in self.ctx.inner.items():
            globals()[k] = v[-1]

    def __exit__(self, exc_type, exc_value, traceback):
        for k in self.ctx.inner.keys():
            del globals()[k]
        pop_many(self.ctx, *self.overrides.keys())


def enter(__ctx=default_ctx, **kwargs):
    return EnterContext(__ctx, **kwargs)
