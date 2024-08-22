use core::str;
use std::{collections::HashMap, io::Read};

use pyo3::prelude::*;
use pyo3::types::PyBytes;
use reqwest::{
    self,
    blocking::{multipart, Client},
};
use serde_json::{self, Value};

use crate::exceptions::{RequestAlreadyInitiated, RequestFinished};
use crate::utils::recurse_value;
use crate::StatusError;

const BUFFER_SIZE: usize = 128;

#[pyclass]
pub struct ResponseLines {
    response: Option<reqwest::blocking::Response>,
    buffer: [u8; BUFFER_SIZE],
}

impl ResponseLines {
    fn new(response: reqwest::blocking::Response) -> ResponseLines {
        ResponseLines {
            response: Some(response),
            buffer: [0; BUFFER_SIZE],
        }
    }
}

#[pymethods]
impl ResponseLines {
    pub fn next(&mut self) -> PyResult<String> {
        if let Some(ref mut r) = self.response {
            let mut line = String::with_capacity(BUFFER_SIZE);

            let mut has_full_line = false;
            while !has_full_line {
                // Read up to self.buffer.len() bytes from socket
                let bytes = r.read(&mut self.buffer).unwrap();
                if bytes == 0 {
                    // If no bytes left to read, set
                    // response to None and stop iteration
                    self.response = None;
                    break;
                }

                // Verify if last byte is a newline indicating
                // that a full line was processed
                has_full_line = self.buffer[bytes - 1] == b'\n';

                // Build UTF-8 string and add to line
                let str = String::from_utf8_lossy(&self.buffer[..(bytes - has_full_line as usize)]);
                line.push_str(&str);
            }

            Ok(line.trim_end().to_string())
        } else {
            // If the response is None it means that all bytes were
            // read from the socket
            Err(RequestFinished::new_err("Request already finished"))
        }
    }
}

#[pyclass]
pub struct Request {
    client: Client,
    request: Option<reqwest::blocking::Request>,
    initiated: bool,
}

impl Request {
    pub(crate) fn new(client: Client, request: reqwest::blocking::Request) -> Request {
        Request {
            client,
            request: Some(request),
            initiated: false,
        }
    }
}

#[pymethods]
impl Request {
    pub fn send(&mut self) -> PyResult<Response> {
        match self.initiated {
            true => Err(RequestAlreadyInitiated::new_err(
                "Request already initiated",
            )),
            false => {
                let req = self.request.take().unwrap();
                let result = self.client.execute(req);
                if let Ok(r) = result {
                    let status_code: u16 = r.status().into();

                    let res_headers = r.headers();
                    let mut headers = HashMap::with_capacity(res_headers.len());
                    for (k, v) in res_headers {
                        headers
                            .insert(k.as_str().to_string(), v.to_str().unwrap_or("").to_string());
                    }

                    Ok(Response::new(r, status_code, headers))
                } else {
                    let e = result.unwrap_err();
                    Err(pyo3::exceptions::PyException::new_err(format!(
                        "Error occurred when sending request: {e}"
                    )))
                }
            }
        }
    }
}

#[pyclass]
pub struct Response {
    response: Option<reqwest::blocking::Response>,

    #[pyo3(get)]
    status_code: u16,

    #[pyo3(get)]
    headers: HashMap<String, String>,
}

impl Response {
    fn new(
        response: reqwest::blocking::Response,
        status_code: u16,
        headers: HashMap<String, String>,
    ) -> Self {
        Response {
            response: Some(response),
            status_code,
            headers,
        }
    }

    fn take_response(&mut self) -> PyResult<reqwest::blocking::Response> {
        match self.response.take() {
            Some(r) => Ok(r),
            None => Err(RequestAlreadyInitiated::new_err(
                "Request already initiated",
            )),
        }
    }
}

#[pymethods]
impl Response {
    pub fn raise_for_status(&mut self) -> PyResult<()> {
        match self.status_code {
            s @ 400.. => Err(StatusError::new_err(s)),
            _ => Ok(()),
        }
    }

    pub fn json(&mut self) -> PyResult<Py<PyAny>> {
        let r = self.take_response()?;
        let v = match r.json::<Value>() {
            Ok(r) => r,
            Err(e) => {
                return Err(pyo3::exceptions::PyException::new_err(format!(
                    "Invalid JSON schema {e}"
                )))
            }
        };

        Ok(Python::with_gil(|py| recurse_value(py, v)))
    }

    pub fn text(&mut self) -> PyResult<String> {
        let r = self.take_response()?;
        match r.text() {
            Ok(r) => Ok(r),
            Err(e) => Err(pyo3::exceptions::PyException::new_err(format!(
                "Error retrieving response text {e}"
            ))),
        }
    }

    pub fn bytes<'p>(&mut self, py: Python<'p>) -> PyResult<&'p PyBytes> {
        let r = self.take_response()?;
        match r.bytes() {
            Ok(r) => Ok(PyBytes::new(py, &r.to_vec())),
            Err(e) => Err(pyo3::exceptions::PyException::new_err(format!(
                "Error retrieving response text {e}"
            ))),
        }
    }

    pub fn iter_lines(&mut self) -> PyResult<ResponseLines> {
        let r = self.take_response()?;
        Ok(ResponseLines::new(r))
    }
}

#[pyclass]
pub struct FormData {
    form: Option<multipart::Form>,
}

#[pymethods]
impl FormData {
    pub fn add_text(&mut self, keyword: String, value: String) -> PyResult<()> {
        let f = match self.form.take() {
            Some(f) => f,
            None => multipart::Form::new(),
        };

        self.form = Some(f.text(keyword, value));

        Ok(())
    }

    pub fn add_file(
        &mut self,
        keyword: String,
        path: String,
        mimetype: String,
        buffer: Vec<u8>,
    ) -> PyResult<()> {
        let mut f = match self.form.take() {
            Some(f) => f,
            None => multipart::Form::new(),
        };

        let part = multipart::Part::bytes(buffer)
            .file_name(path)
            .mime_str(&mimetype);

        if let Ok(part) = part {
            f = f.part(keyword, part);
            self.form = Some(f);

            Ok(())
        } else {
            Err(pyo3::exceptions::PyException::new_err(format!(
                "Error loading file: {}",
                part.err().unwrap()
            )))
        }
    }
}
