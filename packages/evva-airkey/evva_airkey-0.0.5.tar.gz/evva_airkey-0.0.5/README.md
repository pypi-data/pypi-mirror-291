# Python EVVA Airkey communication module

Communication module for EVVA Airkey cloud integration  
(see [EVVA Airkey Cloud Interface Documentation](<https://integration.api.airkey.evva.com/docs/>) for more informations).

## IMPORTANT

**Experimental**  
**Not an official project of EVVA Sicherheitstechnologie GmbH**

## Install

To install from [Pypi](https://www.pypi.org/) using `pip`:
```sh
pip install evva-airkey
```

Or to install directly from git sources:
```bash
git clone https://gitlab.com/geusebi/evva_airkey.git
cd evva_airkey
python setup.py install --user
```

To install `evva_airkey` system-wide, remove `--user` from the last 
line and use `sudo` or other subsystems to run the command as a 
privileged user.

## Usage example

```python
from evva_airkey import Session, fapi

key = "..."
conn = Session(fapi, key)

people = conn.send(fapi.persons_get()).json()
print(people)
```

## Session

### EvvaAuth

The `requests.AuthBase` implementation is used by `evva_airkey.Session` to
update requests' headers. It is created upon session creation via `evva_airkey.Session`
itself.

## License

This software is released under the
[LGPLv3](https://www.gnu.org/licenses/lgpl-3.0.html)  
GNU Lesser General Public License Version 3, 29 June 2007.
