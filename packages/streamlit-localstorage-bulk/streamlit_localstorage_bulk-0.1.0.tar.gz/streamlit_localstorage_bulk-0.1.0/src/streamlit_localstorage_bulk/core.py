from .logger import get_logger


import json
from typing import Any
import uuid
import streamlit as st
from streamlit_js import st_js
from .util import Util
from .cache import Cache


class Core:
    def __init__(
        self,
        prefix: str = "st_localstorage_",
        session_state_cache_key: str = "st_localstorage_cache",
    ) -> None:
        # Hide the JS iframes
        self._container = st.container()
        with self._container:
            st.html(
                """
                <style>
                    .element-container:has(iframe[height="0"]) {
                        display: none;
                    }
                </style>
            """
            )

        self.logger = get_logger(__name__)
        self.prefix = prefix
        self.session_state_cache_key = session_state_cache_key

        if "_ls_unique_keys" not in st.session_state:
            st.session_state["_ls_unique_keys"] = {}
        self.cache = Cache(session_state_cache_key=session_state_cache_key)
        self.ls_keys = Cache(session_state_cache_key="_ls_keys")

    def get_all_items(self) -> Any:
        st_js_key = "get_all_items"
        if self.cache.get(st_js_key):
            return self.cache.get(st_js_key)

        if not self.ls_keys.contains(st_js_key):
            self.ls_keys.set(st_js_key, str(uuid.uuid4()))

        code = """
            var ls = localStorage, items = {};
            for (var i = 0, k; i < ls.length; ++i)
              items[k = ls.key(i)] = ls.getItem(k);
            return items;
        """
        with self._container:
            js_result = st_js(code, key=self.ls_keys.get(st_js_key))
        if js_result and js_result[0]:
            result = Util.remove_quote(js_result[0])
            self.cache.set(st_js_key, result)
            return result
        return {}

    def get_items(self, keys: list) -> Any:
        st_js_key = f"get_items_{'_'.join(keys)}"
        if self.cache.get(st_js_key):
            return self.cache.get(st_js_key)

        if not self.ls_keys.contains(st_js_key):
            self.ls_keys.set(st_js_key, str(uuid.uuid4()))

        codes = ["m = {};"]
        for key in keys:
            codes.append(f"m['{key}'] = localStorage.getItem('{self.prefix + key}');")
        codes.append("return m;")

        with self._container:
            js_result = st_js("\n".join(codes), key=self.ls_keys.get(st_js_key))
        if js_result and js_result[0]:
            result = Util.remove_quote(js_result[0])
            self.cache.set(st_js_key, result)
            return Util.remove_quote(result)
        return {}

    def setitems(self, data: dict) -> None:
        st_js_key = f"setitems_{'_'.join(data.keys())}"
        self.ls_keys.set(st_js_key, str(uuid.uuid4()))
        codes = []
        for key, value in data.items():
            value = json.dumps(value, ensure_ascii=False)
            code = f"""
            localStorage.setItem('{self.prefix + key}', '{value}');
            """
            codes.append(code)

        with self._container:
            self.logger.debug(f"setitems: {codes}")
            return st_js(
                "\n".join(codes),
                key=self.ls_keys.get(st_js_key),
            )

    def delitems(self, keys: list) -> None:
        st_js_key = f"delitems_{'_'.join(keys)}"
        self.ls_keys.set(st_js_key, str(uuid.uuid4()))
        codes = []
        for key in keys:
            code = f"localStorage.removeItem('{self.prefix + key}');"
            codes.append(code)

        with self._container:
            self.logger.debug(f"delitems: {codes}")
            return st_js(
                "\n".join(codes),
                key=self.ls_keys.get(st_js_key),
            )

    def __contains__(self, key: str) -> bool:
        return self.__getitem__(key) is not None
