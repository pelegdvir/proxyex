## Linx Security Home Task - Peleg Dvir

#### Dependencies
```
pip install cachetools
pip install pytest
```

#### Tests
```
pytest
```

#### Example
In 4 tabs run
```
python example_http_server.py
python example_proxy_server.py
python example_flood.py
python example_deny_list.py
```
Check the console logs.

* The first file is simple HTTP server (POST and GET)
* The second file is a very simple HTTP proxy server - that calls the classifier (the interesting bit)
* The third file calls for an actual case - flooding with packets - after some time the response would change from 200 -> 403
* The third file calls for another case - checking for bad body

### Code structure

#### Proxy server
A very simple HTTP proxy server that will call the classification area. The proxy will either pass the request with an added header or deny it. The server can easily be replaced and is decoupled from the rest of the code.

#### Classification
Most of the code allows you to define a `suite` - a couple of `detectors` on a packet. Every `detector` results in a `DetectorResult` with a suggestion for what to do with the tested packet. After a `suite` runs all relevant `detectors`, it can decide what to do with the packet - pass it or not.

The component that manage this process is `Classifier`, it can also have
other utilities such as `Reporter`

##### Detectors
Some `Detectors` are extremely opinionated and can mark that the packet is so problematic that it must be dropped right away without running any other detectors. Other detectors can result in the opposite ("I trust this") or give a "danger grade" - to score with the rest of the detectors in order to decide what to do with it. `Detectors` can have shared memory, but most of the time, every detector would use its own memory. (Most of the time, shared memory is useful in order to dynamically mark that an IP is problematic).

##### Suites
Suites are a collection of Detectors with relevant configuration. In some cases, we would want to avoid running all detectors.

#### Content Folder
Most of the time, we would want to edit detector/suites that are defined in the content folder and avoid touching anything else. The rest of the code is infra/definitions.

## Next steps:
0. More tests
1. Suites - better config (json files), currently its config in python code
2. Runner and detectors.detect - use async
3. Detectors - allow to call "sub detectors", for example - detector A figures its a POST call, and because of it, we want to run 20 additional detectors that are not relevant to GET calls.
4. Memory and Reporter - have a better interface
5. ids - we already have UUID to mark identifiers - we should log and use them
6. Better proxy
