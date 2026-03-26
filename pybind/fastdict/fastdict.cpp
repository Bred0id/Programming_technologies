#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "splay_tree.hpp"

namespace py = pybind11;

template <class T>
class ParametrizeKey {
  T data;

 public:
  ParametrizeKey() = default;

  explicit ParametrizeKey(const T& obj) : data(obj) {
  }

  T GetObject() const {
    return data;
  }

  bool operator<(const ParametrizeKey& other) const {
    try {
      return data < other.data;
    } catch (const py::error_already_set&) {
      throw std::runtime_error("Objects cannot be compared with < operator");
    }
  }
};

class FastDict : public SplayTree<ParametrizeKey<py::object>, py::object> {
 public:
  void __setitem__(py::object key, py::object value) {
    Add(ParametrizeKey<py::object>(key), value);
  }

  py::object __getitem__(py::object key) {
    try {
      return Find(ParametrizeKey<py::object>(key));
    } catch (const std::out_of_range&) {
      throw py::key_error("Key not found");
    }
  }

  void __delitem__(py::object key) {
    if (!Remove(ParametrizeKey<py::object>(key))) {
      throw py::key_error("Key not found");
    }
  }

  bool __contains__(py::object key) {
    return Contains(ParametrizeKey<py::object>(key));
  }

  py::int_ __len__() {
    return py::int_(Size());
  }

  std::vector<py::object> keys() {
    std::vector<py::object> result;
    for (const auto& key : GetKeys()) {
      result.push_back(key.GetObject());
    }
    return result;
  }

  std::vector<py::object> values() {
    return GetValues();
  }

  std::vector<std::pair<py::object, py::object>> items() {
    std::vector<std::pair<py::object, py::object>> result;
    for (const auto& item : GetItems()) {
      result.push_back({item.first.GetObject(), item.second});
    }
    return result;
  }

  py::object __iter__() {
    py::list result;
    for (const auto& key : GetKeys()) {
      result.append(key);
    }
    return py::iter(result);
  }
};

PYBIND11_MODULE(fastdict_core, m) {
  py::class_<ParametrizeKey<py::object>>(m, "Key")
      .def(py::init<>())
      .def(py::init<const py::object&>())
      .def("get_object", &ParametrizeKey<py::object>::GetObject)
      .def("__lt__", &ParametrizeKey<py::object>::operator<);

  py::class_<FastDict>(m, "FastDict")
      .def(py::init<>())
      .def("__setitem__", &FastDict::__setitem__)
      .def("__getitem__", &FastDict::__getitem__)
      .def("__delitem__", &FastDict::__delitem__)
      .def("__contains__", &FastDict::__contains__)
      .def("__len__", &FastDict::__len__)
      .def("__iter__", &FastDict::__iter__)
      .def("keys", &FastDict::keys)
      .def("values", &FastDict::values)
      .def("items", &FastDict::items);
}