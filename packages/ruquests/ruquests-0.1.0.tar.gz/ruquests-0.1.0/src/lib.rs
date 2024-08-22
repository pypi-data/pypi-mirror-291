use std::collections::HashMap;

use pyo3::prelude::*;

mod builders;
mod exceptions;
mod types;
mod utils;

use builders::*;
pub use exceptions::{RequestAlreadyInitiated, RequestFinished, RequestNotInitiated, StatusError};
pub use types::{FormData, Request, ResponseLines};
use utils::object_to_value;

#[pyfunction]
fn head(
    url: String,
    headers: Option<HashMap<String, String>>,
    timeout: Option<u64>,
) -> PyResult<Request> {
    let client = build_client(Some(false), timeout).map_err(|e| {
        PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("Failed to build client: {}", e))
    })?;

    let builder = client.head(url);
    let builder = build_headers(builder, headers);
    Ok(Request::new(client, builder.build().unwrap()))
}

#[pyfunction]
fn get(
    url: String,
    query_params: Option<HashMap<String, String>>,
    headers: Option<HashMap<String, String>>,
    follow_redirects: Option<bool>,
    timeout: Option<u64>,
) -> PyResult<Request> {
    let client = build_client(follow_redirects, timeout).map_err(|e| {
        PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("Failed to build client: {}", e))
    })?;

    let builder = client.get(url);
    let builder = build_headers(builder, headers);
    let builder = build_query(builder, query_params);
    Ok(Request::new(client, builder.build().unwrap()))
}

#[pyfunction]
fn post(
    url: String,
    query_params: Option<HashMap<String, String>>,
    headers: Option<HashMap<String, String>>,
    json: Option<PyObject>,
    data: Option<HashMap<String, String>>,
    form: Option<&FormData>,
    follow_redirects: Option<bool>,
    timeout: Option<u64>,
) -> PyResult<Request> {
    let client = build_client(follow_redirects, timeout).map_err(|e| {
        PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("Failed to build client: {}", e))
    })?;

    let mut builder = client.post(url);
    builder = build_headers(builder, headers);
    builder = build_query(builder, query_params);

    if let Some(json) = json {
        let value = Python::with_gil(|py| object_to_value(json.as_ref(py)))?;
        builder = build_json_body(builder, value);
    } else if let Some(data) = data {
        builder = build_urlencoded_body(builder, data);
    } else if let Some(_form) = form {
        return Err(pyo3::exceptions::PyNotImplementedError::new_err(
            "Multipart not yet implemented",
        ));
    }

    Ok(Request::new(client, builder.build().unwrap()))
}

#[pyfunction]
fn put(
    url: String,
    query_params: Option<HashMap<String, String>>,
    headers: Option<HashMap<String, String>>,
    json: Option<PyObject>,
    data: Option<HashMap<String, String>>,
    form: Option<&FormData>,
    follow_redirects: Option<bool>,
    timeout: Option<u64>,
) -> PyResult<Request> {
    let client = build_client(follow_redirects, timeout).map_err(|e| {
        PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("Failed to build client: {}", e))
    })?;

    let mut builder = client.put(url);
    builder = build_headers(builder, headers);
    builder = build_query(builder, query_params);

    if let Some(json) = json {
        let value = Python::with_gil(|py| object_to_value(json.as_ref(py)))?;
        builder = build_json_body(builder, value);
    } else if let Some(data) = data {
        builder = build_urlencoded_body(builder, data);
    } else if let Some(_form) = form {
        return Err(pyo3::exceptions::PyNotImplementedError::new_err(
            "Multipart not yet implemented",
        ));
    }

    Ok(Request::new(client, builder.build().unwrap()))
}

#[pyfunction]
fn patch(
    url: String,
    query_params: Option<HashMap<String, String>>,
    headers: Option<HashMap<String, String>>,
    json: Option<PyObject>,
    data: Option<HashMap<String, String>>,
    form: Option<&FormData>,
    follow_redirects: Option<bool>,
    timeout: Option<u64>,
) -> PyResult<Request> {
    let client = build_client(follow_redirects, timeout).map_err(|e| {
        PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("Failed to build client: {}", e))
    })?;

    let mut builder = client.patch(url);
    builder = build_headers(builder, headers);
    builder = build_query(builder, query_params);

    if let Some(json) = json {
        let value = Python::with_gil(|py| object_to_value(json.as_ref(py)))?;
        builder = build_json_body(builder, value);
    } else if let Some(data) = data {
        builder = build_urlencoded_body(builder, data);
    } else if let Some(_form) = form {
        return Err(pyo3::exceptions::PyNotImplementedError::new_err(
            "Multipart not yet implemented",
        ));
    }

    Ok(Request::new(client, builder.build().unwrap()))
}

#[pyfunction]
fn delete(
    url: String,
    query_params: Option<HashMap<String, String>>,
    headers: Option<HashMap<String, String>>,
    json: Option<PyObject>,
    data: Option<HashMap<String, String>>,
    form: Option<&FormData>,
    follow_redirects: Option<bool>,
    timeout: Option<u64>,
) -> PyResult<Request> {
    let client = build_client(follow_redirects, timeout).map_err(|e| {
        PyErr::new::<pyo3::exceptions::PyRuntimeError, _>(format!("Failed to build client: {}", e))
    })?;

    let mut builder = client.delete(url);
    builder = build_headers(builder, headers);
    builder = build_query(builder, query_params);

    if let Some(json) = json {
        let value = Python::with_gil(|py| object_to_value(json.as_ref(py)))?;
        builder = build_json_body(builder, value);
    } else if let Some(data) = data {
        builder = build_urlencoded_body(builder, data);
    } else if let Some(_form) = form {
        return Err(pyo3::exceptions::PyNotImplementedError::new_err(
            "Multipart not yet implemented",
        ));
    }

    Ok(Request::new(client, builder.build().unwrap()))
}

#[pymodule]
fn bindings(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(head, m)?)?;
    m.add_function(wrap_pyfunction!(get, m)?)?;
    m.add_function(wrap_pyfunction!(post, m)?)?;
    m.add_function(wrap_pyfunction!(put, m)?)?;
    m.add_function(wrap_pyfunction!(patch, m)?)?;
    m.add_function(wrap_pyfunction!(delete, m)?)?;

    m.add_class::<FormData>()?;
    m.add_class::<Request>()?;
    m.add_class::<ResponseLines>()?;
    m.add("StatusError", py.get_type::<StatusError>())?;
    m.add("RequestNotInitiated", py.get_type::<RequestNotInitiated>())?;
    m.add(
        "RequestAlreadyInitiated",
        py.get_type::<RequestAlreadyInitiated>(),
    )?;
    m.add("RequestFinished", py.get_type::<RequestFinished>())?;

    Ok(())
}
