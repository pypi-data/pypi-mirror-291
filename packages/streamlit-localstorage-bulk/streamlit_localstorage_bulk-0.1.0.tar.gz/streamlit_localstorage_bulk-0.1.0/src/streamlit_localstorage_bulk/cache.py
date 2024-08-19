import streamlit as st


class Cache:
    def __init__(self, session_state_cache_key: str = None) -> None:
        if session_state_cache_key not in st.session_state:
            st.session_state[session_state_cache_key] = {}
        self.session_state_cache_key = session_state_cache_key

    def get(self, key: str) -> str:
        if key in st.session_state[self.session_state_cache_key]:
            return st.session_state[self.session_state_cache_key][key]
        return None

    def set(self, key: str, value: str) -> None:
        st.session_state[self.session_state_cache_key][key] = value

    def contains(self, key: str) -> None:
        return key in st.session_state[self.session_state_cache_key]
