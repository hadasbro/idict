import unittest
import copy
import pickle

from lib.exceptions import KeyNotAllowedException, MandatoryKeyValueException, ValueNotAllowedException
from lib.idict import Idict


class TestReleaseRegressions(unittest.TestCase):
    def test_throw_mode_rejects_update_setdefault_and_ior(self):
        for mode_call in ("update", "setdefault", "ior"):
            with self.subTest(mode_call=mode_call):
                obj = Idict({"a": 1}, {"missing_keys": Idict.OPT.THROW})

                if mode_call == "update":
                    with self.assertRaises(KeyNotAllowedException):
                        obj.update({"forbidden": 7})
                elif mode_call == "setdefault":
                    with self.assertRaises(KeyNotAllowedException):
                        obj.setdefault("forbidden", 7)
                else:
                    with self.assertRaises(KeyNotAllowedException):
                        obj |= {"forbidden": 7}

    def test_throw_mode_rejects_plain_dict_overwrite_for_nested_schema(self):
        obj = Idict({"nested": {"b": 2}}, {"missing_keys": Idict.OPT.THROW})
        with self.assertRaises(ValueNotAllowedException):
            obj["nested"] = {"forbidden": 7}

    def test_validate_fails_when_mandatory_key_is_deleted(self):
        obj = Idict({"a": ..., "b": 1}, {"missing_keys": Idict.OPT.THROW})
        obj["a"] = 2
        del obj["a"]
        with self.assertRaises(MandatoryKeyValueException):
            obj.validate()

    def test_mutable_defaults_are_not_shared_between_instances(self):
        pattern = {"a": []}
        obj1 = Idict(pattern)
        obj2 = Idict(pattern)
        obj1["a"].append(1)

        self.assertEqual(obj1["a"], [1])
        self.assertEqual(obj2["a"], [])
        self.assertEqual(pattern["a"], [])

    def test_internal_maps_are_isolated_per_root_instance(self):
        obj1 = Idict({"x": 1})
        obj2 = Idict({"y": 2})

        self.assertIsNot(obj1.dependencies, obj2.dependencies)
        self.assertIsNot(obj1.locked_keys, obj2.locked_keys)
        self.assertIsNot(obj1.id_key, obj2.id_key)

    def test_throw_mode_rejects_or_operator_for_forbidden_keys(self):
        obj = Idict({"a": 1}, {"missing_keys": Idict.OPT.THROW})
        with self.assertRaises(KeyNotAllowedException):
            _ = obj | {"forbidden": 7}

    def test_copy_copy_returns_equivalent_idict(self):
        obj = Idict({"a": 1, "nested": {"b": 2}}, {"missing_keys": Idict.OPT.THROW})
        obj["a"] = 10
        copied = copy.copy(obj)

        self.assertIsInstance(copied, Idict)
        self.assertIsNot(copied, obj)
        self.assertEqual(dict(copied), dict(obj))

    def test_pickle_raises_clear_error(self):
        obj = Idict({"a": 1})
        with self.assertRaises(TypeError) as ex:
            pickle.dumps(obj)
        self.assertIn("does not support pickle serialization", str(ex.exception))


if __name__ == "__main__":
    unittest.main()
