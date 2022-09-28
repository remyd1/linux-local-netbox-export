# Linux Local Netbox exporter

Netbox may be quite annoying if you have many devices to add. There is an ansible moule to do it, but that is not really easy either (see [this thread](https://github.com/netbox-community/ansible_modules/issues/25) for more informations).

Nevertheless, that is doable; see an example [here](https://netbox-ansible-collection.readthedocs.io/en/latest/getting_started/how-to-use/advanced.html).

In this repository, you will find a basic python script to export list of interfaces from a linux host device into a compatible CSV file for netbox.

## Installation

Just clone this repository. You will need a python3 interpreter.

## Usage

```bash
python3 interfaces.py
cat interfaces.csv
```

Now, you can import the CSV file into netbox device interfaces.
