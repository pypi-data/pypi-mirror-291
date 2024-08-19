from streamlit_localstorage_bulk.util import Util


class TestUtil(object):
    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    def test_remove_quote(self):
        assert Util.remove_quote({"a": '"1"'}) == {"a": "1"}
