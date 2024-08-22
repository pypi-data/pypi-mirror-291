use std::collections::HashMap;

use pyo3::prelude::*;
use pyo3::types::{PyBool, PyDict, PyFloat, PyInt, PyList, PyString};
use pyo3::Python;
use serde_json::Value;

pub(crate) fn recurse_value(py: Python, value: Value) -> Py<PyAny> {
    match value {
        Value::Null => None::<()>.to_object(py),
        Value::Bool(v) => v.to_object(py),
        Value::Number(v) => {
            if v.is_f64() {
                v.as_f64().to_object(py)
            } else {
                v.as_i64().to_object(py)
            }
        }
        Value::String(v) => v.to_object(py),
        Value::Array(v) => {
            let mut array = Vec::with_capacity(v.len());
            for inner in v {
                array.push(recurse_value(py, inner));
            }
            array.to_object(py)
        }
        Value::Object(v) => {
            let mut map = HashMap::with_capacity(v.len());
            for (k, inner) in v {
                map.insert(k, recurse_value(py, inner));
            }
            map.to_object(py)
        }
    }
}

pub(crate) fn object_to_value(obj: &PyAny) -> PyResult<Value> {
    if let Ok(dict) = obj.downcast::<PyDict>() {
        let mut map = serde_json::Map::new();
        for (key, value) in dict.iter() {
            let key: String = key.extract()?;
            let value = object_to_value(&value)?;
            map.insert(key, value);
        }
        Ok(Value::Object(map))
    } else if let Ok(list) = obj.downcast::<PyList>() {
        let mut vec = Vec::new();
        for item in list.iter() {
            vec.push(object_to_value(item)?);
        }
        Ok(Value::Array(vec))
    } else if let Ok(py_str) = obj.downcast::<PyString>() {
        Ok(Value::String(py_str.to_str()?.to_string()))
    } else if let Ok(py_int) = obj.downcast::<PyInt>() {
        Ok(Value::Number(py_int.extract::<i64>()?.into()))
    } else if let Ok(py_float) = obj.downcast::<PyFloat>() {
        let float = py_float.extract::<f64>()?;
        Ok(Value::Number(serde_json::Number::from_f64(float).unwrap()))
    } else if let Ok(py_bool) = obj.downcast::<PyBool>() {
        Ok(Value::Bool(py_bool.is_true()))
    } else {
        Err(PyErr::new::<pyo3::exceptions::PyTypeError, _>(
            "Unsupported Python object type",
        ))
    }
}
