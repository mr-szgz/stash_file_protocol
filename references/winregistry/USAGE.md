## WinRegistry Usage

### Creating and Deleting Registry Keys

import winreg
from winregistry import open\_key

\# Create a registry key
with open\_key(
  "HKLM\\\\SOFTWARE\\\\MyApp",
  sub\_key\_ensure\=True,
  sub\_key\_access\=winreg.KEY\_WRITE,
) as key:
  print("Registry key created")

\# Delete a registry key
with open\_key(
  "HKLM\\\\SOFTWARE",
  sub\_key\_access\=winreg.KEY\_WRITE,
) as key:
  key.delete\_key("MyApp")
  print("Registry key deleted")

### Setting and Reading Registry Values

import winreg
from winregistry import open\_key, open\_value

\# Set a registry value
with open\_key(
  "HKLM\\\\SOFTWARE\\\\MyApp",
  sub\_key\_ensure\=True,
  sub\_key\_access\=winreg.KEY\_WRITE,
) as key:
  key.set\_value(
    "MyValue",
    winreg.REG\_SZ,
    "Sample Data",
  )
  print("Registry value set")

\# Read a registry value
with open\_value(
  "HKLM\\\\SOFTWARE\\\\MyApp",
  value\_name\="MyValue",
) as value:
  print(f"Registry value: {value.data}")

### Enumerating Subkeys and Values

import winreg
from winregistry import open\_key

\# Enumerate subkeys
with open\_key(
  "HKLM\\\\SOFTWARE",
  sub\_key\_access\=winreg.KEY\_READ,
) as key:
  subkeys \= list(key.child\_keys\_names)
  print(f"Subkeys: {subkeys}")

\# Enumerate values
with open\_key(
  "HKLM\\\\SOFTWARE\\\\MyApp",
  sub\_key\_access\=winreg.KEY\_READ,
) as key:
  values \= \[(v.name, v.data) for v in key.values\]
  print(f"Values: {values}")
