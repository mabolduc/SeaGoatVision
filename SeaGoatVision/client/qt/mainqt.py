#! /usr/bin/env python

#    Copyright (C) 2012  Octets - octets.etsmtl.ca
#
#    This file is part of SeaGoatVision.
#
#    SeaGoatVision is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Description : launch qt client
Authors: Junior Gregoire (junior.gregoire@gmail.com)
Date : November 2012
"""
import sys

from SeaGoatVision.server.core.manager import Manager
from PySide.QtGui import QApplication
import main


def run(local=False, host="localhost", port=8090):
    if local:
        # Directly connected to the vision server
        c = Manager()
    else:
        from SeaGoatVision.client.controller.controllerProtobuf import ControllerProtobuf
        # Protobuf
        c = ControllerProtobuf(host, port)

    if not c.is_connected():
        print("Vision server is not accessible.")
        return

    app = QApplication(sys.argv)
    win = main.WinMain(c, host=host)
    win.show()
    rint = app.exec_()
    # close the server
    win.quit()
    c.close()

    return rint

if __name__ == '__main__':
    # Project path is parent directory
    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    os.sys.path.insert(0, parentdir)
    sys.exit(run(local=True))
