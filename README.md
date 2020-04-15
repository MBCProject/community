# <a name="mbc"></a>Cuckoo Community Signature-MBC Mappings #

The MBC team has mapped [Cuckoo community signatures](https://github.com/cuckoosandbox/community) into MBC. Of the 560+ signatures available, approximately 275 are appropriate for mapping into MBC (the others are anti-virus related signatures that identify specific threats). 

Approximately 140 of the signatures were already mapped into ATT&CK. We added new signatures, which was possible because MBC includes malware-related behaviors that ATT&CK doesn't. We also used MBC's malware-focused content to revise 80 of the existing ATT&CK mappings.

Below, we explain how these signatures are used. We begin with an example Python signature and then show example Cuckoo report output. We conclude with information on using the signature repository.

Example Cuckoo Signature
------------------------

This signature example (antisandbox_sleep.py) was not mapped to an ATT&CK technique. We map it to **Dynamic Analysis Evasion [M0003]** as shown below (see the ttp variable).

```python
from lib.cuckoo.common.abstracts import Signature

class AntiSandboxSleep(Signature):
    name = "antisandbox_sleep"
    description = "A process attempted to delay the analysis task."
    severity = 2
    categories = ["anti-sandbox"]
    authors = ["KillerInstinct"]
    minimum = "2.0"
    ttp = ["M0003"]

    filter_apinames = "NtDelayExecution",

    whitelist = [
        "dwm.exe",
        "adobearm.exe",
        "iexplore.exe",
        "acrord32.exe",
        "winword.exe",
        "excel.exe",
    ]

    def init(self):
        self.sleeps = {}

    def on_call(self, call, process):
        procname = process["process_name"]
        if procname not in self.sleeps:
            self.sleeps[procname] = {
                "attempt": 0,
                "actual": 0,
            }

        milliseconds = call["arguments"]["milliseconds"]

        self.sleeps[procname]["attempt"] += milliseconds

        if not call["arguments"]["skipped"]:
            self.sleeps[procname]["actual"] += milliseconds

    def on_complete(self):
        for process_name, info in self.sleeps.items():
            if process_name.lower() in self.whitelist:
                continue

            if info["attempt"] >= 120000:
                attempted = info["attempt"] / 1000
                actual = info["actual"] / 1000
                self.mark(description="%s tried to sleep %s seconds, actually delayed analysis time by %s seconds" % (process_name, attempted, actual))

            if info["attempt"] >= 1200000:
                self.severity = 3

        return self.has_marks()
```

Cuckoo Reports
--------------

The signature section of a Cuckoo report specifies associated MBC behavior as shown in the example below (Dynamic Analysis Evasion [M0003] behavior is shown).

```json
"signatures": [
  {
      "families": [],
      "description": "A process attempted to delay the analysis task.",
      "severity": 1,
      "ttp": {
        "M0003": {
          "short": "Dynamic Analysis Evasion",
          "long": "Malware may obstruct dynamic analysis in a sandbox, emulator, or virtual <snip>"
        }
      },
      "markcount": 1,
      "references": "...",
      "marks": "...",
      "name": "antisandbox_sleep"
  }
]
```

How to Use the Repository
-------------------------

The [Cuckoo community repository](https://github.com/cuckoosandbox/community) is open and dedicated to contributions from the commmunity.
Users can submit custom modules for sharing with the rest of the community.

All the directories here share the same structure as the
latest Cuckoo Sandbox release. While it's possible to download the whole
repository and extract it in Cuckoo's root directory, it is suggested that only the modules of interest are copied.

Cuckoo also provides an utility to automatically download and install
latest modules. You can do so by running the `cuckoo community` command.