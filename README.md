# PythonSimpleSettings
This is a simple module to wrap ConfigParser and check if the settings exists

To use it you need to call the get_instance as it's implemented from a singleton

Small example below :

```python

from <submodule>.setting import Settings

Settings.get_instance().loadSettings(<file path or absolute>)
print(Settings.get_instance().get(<section>, <key>, <defaultValue>))
```
