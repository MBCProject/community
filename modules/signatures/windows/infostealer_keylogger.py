# Copyright (C) 2012 Thomas "stacks" Birn (@stacksth)
# Copyright (C) 2014 Claudio "nex" Guarnieri (@botherder)
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

class Keylogger(Signature):
    name = "infostealer_keylogger"
    description = "Creates a windows hook that monitors keyboard input (keylogger)"
    severity = 3
    categories = ["generic"]
    authors = ["Thomas Birn", "nex"]
    minimum = "2.0"
    ttp = ["T1056", "E1179"]

    filter_apinames = "SetWindowsHookExA", "SetWindowsHookExW"

    def on_call(self, call, process):
        if call["arguments"]["hook_identifier"] in [2, 13]:
            if not call["arguments"]["thread_identifier"]:
                self.mark_call()
                return True
