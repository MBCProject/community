# Copyright (C) 2015 Kevin Ross, Updated 2016 for Cuckoo 2.0
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from lib.cuckoo.common.abstracts import Signature

class SunbeltDetectFiles(Signature):
    name = "antisandbox_sunbelt_files"
    description = "Detects Sunbelt Sandbox through the presence of a file"
    severity = 3
    categories = ["anti-sandbox"]
    authors = ["Kevin Ross"]
    minimum = "2.0"
    ttp = ["M0007"]

    file_indicators = [
        ".*\\\\SandboxStarter\\.exe$",
        "C\\:\\\\analysis\\\\.*",
    ]

    def on_complete(self):
        for indicator in self.file_indicators:
            for match in self.check_file(pattern=indicator, regex=True, all=True):
                self.mark_ioc("file", match)

        return self.has_marks()
