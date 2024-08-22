# ruquests

## Usage

Calling HTTP methods (get, post, put, patch, delete) creates a request to be sent. When user wants to actually send it, it should call "send()" and it will return a response object which has the headers and the body of the response.

---

Simple usage example:

```python
import ruquests

r = ruquests.get("http://google.com", headers={"accept": "text/html"}).send()
print(r.text())
```

---

Raising for invalid status code

```python
import ruquests

r = ruquests.post("http://google.com").send()
r.raise_for_status()
```

---

Checking response headers

```python
import ruquests

r = ruquests.get("http://google.com").send()
print(r.headers)
```

---

Checking status code

```python
import ruquests

r = ruquests.get("http://google.com").send()
print(r.status_code)
```
