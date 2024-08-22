use std::{collections::HashMap, time::Duration};

use reqwest::{
    self,
    blocking::{Client, RequestBuilder},
    redirect::Policy,
    Error,
};
use serde_json::Value;

pub(crate) fn build_client(
    follow_redirects: Option<bool>,
    timeout: Option<u64>,
) -> Result<Client, Error> {
    let mut builder = Client::builder();
    if let Some(follow) = follow_redirects {
        if !follow {
            builder = builder.redirect(Policy::none());
        }
    }

    builder = match timeout {
        Some(t) => builder.timeout(Duration::from_secs(t)),
        None => builder.timeout(Duration::from_secs(15)),
    };

    builder.build()
}

pub(crate) fn build_headers(
    mut builder: RequestBuilder,
    headers: Option<HashMap<String, String>>,
) -> RequestBuilder {
    if let Some(h) = headers {
        for (k, v) in h.into_iter() {
            builder = builder.header(k, v);
        }
    }

    builder
}

pub(crate) fn build_query(
    mut builder: RequestBuilder,
    query_params: Option<HashMap<String, String>>,
) -> RequestBuilder {
    if let Some(p) = query_params {
        builder = builder.query(&p.into_iter().collect::<Vec<_>>())
    }
    builder
}

pub(crate) fn build_json_body(builder: RequestBuilder, json: Value) -> RequestBuilder {
    builder.json(&json)
}

pub(crate) fn build_urlencoded_body(
    builder: RequestBuilder,
    form: HashMap<String, String>,
) -> RequestBuilder {
    builder.form(&form)
}
