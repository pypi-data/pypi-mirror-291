# streamlit-localstorage-bulk

[![PyPI version](https://badge.fury.io/py/streamlit-localstorage-bulk.svg)](https://badge.fury.io/py/streamlit-localstorage-bulk)
[![Build Status](https://github.com/toyama0919/streamlit-localstorage-bulk/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/toyama0919/streamlit-localstorage-bulk/actions/workflows/ci.yml)

Handles localstorage with Streamlit.

Significant performance improvements can be expected due to batch javascript execution.

Support python3 only.

## Examples

```python
import streamlit as st
from streamlit_localstorage_bulk import StreamlitLocalstorageBulk


def main():
    sl = StreamlitLocalstorageBulk(
        prefix="st_localstorage_",
    )
    v = sl.get_items(keys=["ability", "goals", "a"])
    st.write(v)

    # update or create
    if st.button("setitem"):
        sl.setitems(data={"a": "A"})

    # delete
    if st.button("delitem"):
        sl.delitems(keys=["a"])


if __name__ == "__main__":
    main()
```

## Installation

```sh
pip install streamlit-localstorage-bulk
```

## CI

### install test package

```
$ ./scripts/ci.sh install
```

### test

```
$ ./scripts/ci.sh run-test
```

flake8 and black and pytest.

### release pypi

```
$ ./scripts/ci.sh release
```

git tag and pypi release.
