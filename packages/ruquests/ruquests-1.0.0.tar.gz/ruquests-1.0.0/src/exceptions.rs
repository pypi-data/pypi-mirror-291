use pyo3::create_exception;
use pyo3::exceptions::PyException;

create_exception!(rrequests, StatusError, PyException);
create_exception!(rrequests, RequestNotInitiated, PyException);
create_exception!(rrequests, RequestAlreadyInitiated, PyException);
create_exception!(rrequests, RequestFinished, PyException);
