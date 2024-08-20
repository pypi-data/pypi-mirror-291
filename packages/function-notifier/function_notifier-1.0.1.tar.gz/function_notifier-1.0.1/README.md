# Function Notifier

This simple package contains the notify decorator, used to notify users when the function  it wraps has finished execution.

![PyPI Version](https://img.shields.io/pypi/v/function_notifier)
![License](https://img.shields.io/badge/license-MIT-blue)

## Installation

To install Function Notifier, navigate to a command-line with your Python environment set up (e.g. Anaconda Prompt) and enter,

```bash
$ pip install function_notifier
```

### Dependencies

Note that plyer is also installed by pip for creating the notification messages themselves.

## Usage

```python
import time
from  function_notifier import notify


@notify()
def foo():

  time.sleep(60)

  return None


if __name__ == "__main__":
  foo()

```

The code above offers an example of how to use the Function Notifier package. The imported notify decorator is added to any function you suspect will take a while, which results in an operating system notification upon that function's completion. The time import here is only used to simulate a function with a long runtime.
