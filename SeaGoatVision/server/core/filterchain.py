#! /usr/bin/env python

#    Copyright (C) 2012  Club Capra - capra.etsmtl.ca
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

"""Contains the FilterChain class and helper functions to work with the filter chain."""

import SeaGoatVision.server.filters
from SeaGoatVision.server.filters.dataextract import DataExtractor
from SeaGoatVision.server.filters.parameter import Parameter
import ConfigParser
import numpy as np

def my_import(name):
    mod = __import__(name)
    components = name.split('.')
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod

def params_list(chain):
    flist = []
    for filtre in chain.filters:
        fname = filtre.__class__.__name__
        params = []
        for name in dir(filtre):
            parameter = getattr(filtre, name)
            if not isinstance(parameter, Parameter):
                continue
            params.append((name, parameter.get_current_value()))
        flist.append((fname, params))
    return flist

def isnumeric(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def read(file_name):
    """Open a filtre chain file and load its content in a new filtre chain."""
    filterchain_name = file_name[file_name.rfind("/") + 1:file_name.rfind(".")]
    new_chain = FilterChain(filterchain_name)
    cfg = ConfigParser.ConfigParser()
    cfg.read(file_name)
    for section in cfg.sections():
        filtre = SeaGoatVision.server.filters.create_filter(section)
        if not filtre:
            print("Error : The filter %s doesn't exist on filterchain." % (section, filterchain_name))
            continue
        for member in filtre.__dict__:
            parameter = getattr(filtre, member)
            if not isinstance(parameter, Parameter):
                continue
            val = cfg.get(section, member)
            if val == "True" or val == "False":
                parameter.set_current_value(cfg.getboolean(section, member))
            elif isnumeric(val):
                parameter.set_current_value(cfg.getfloat(section, member))
            else:
                if isinstance(val, str):
                    val = '\n'.join([line[1:-1] for line in str.splitlines(val)])
                parameter.set_current_value(val)
        if hasattr(filtre, 'configure'):
            filtre.configure()
        new_chain.add_filter(filtre)
    return new_chain

def write(file_name, chain):
    """Save the content of the filter chain in a file."""
    cfg = ConfigParser.ConfigParser()
    for fname, params in params_list(chain):
        cfg.add_section(fname)
        for name, value in params:
            if isinstance(value, str):
                value = '\n'.join(['"%s"' % line for line in str.splitlines(value)])
            cfg.set(fname, name, value)
    cfg.write(open(file_name, 'w'))

class FilterChain:
    """ Observable.  Contains the chain of filters to execute on an image.

    The observer must be a method that receive a filter and an image as parameter.
    The observer method is called after each execution of a filter in the filter chain.
    """
    def __init__(self, filterchain_name):
        self.filters = []
        self.image_observers = {}
        self.filter_output_observers = []
        self.filterchain_name = filterchain_name

    def count(self):
        return len(self.filters)

    def get_name(self):
        return self.filterchain_name

    def get_filter_output_observers(self):
        return self.filter_output_observers

    def get_filter_list(self):
        class Filter: pass
        retValue = []
        for item in self.filters:
            filter = Filter()
            setattr(filter, "name", item.__class__.__name__)
            setattr(filter, "doc", item.__doc__)
            retValue.append(filter)
        return retValue

    def __getitem__(self, index):
        return self.filters[index]

    def get_filter(self, index=None, name=None):
        if index is not None:
            return self.filters[index]
        elif name is not None:
            lst_filter = [o_filter for o_filter in self.filters if o_filter.__class__.__name__ == name]
            if lst_filter:
                return lst_filter[0]
        return None

    def add_filter(self, filtre):
        self.filters.append(filtre)

    def remove_filter(self, filtre):
        self.filters.remove(filtre)

    def reload_filter(self, filtre):
        # example of __module__:
        index = 0
        for item in self.filters:
            if item.__class__.__name__ == filtre:
                # remote observer
                filter_output_obs_copy = self.filter_output_observers[:]
                for output in filter_output_obs_copy:
                    self.remove_filter_output_observer(output)
                # reload the module
                module = my_import(item.__module__)
                reload(module)
                # recreate the instance
                self.filters[index] = getattr(module, item.__class__.__name__)()
                # re-add observer
                for output in filter_output_obs_copy:
                    self.add_filter_output_observer(output)
            index += 1

    def add_image_observer(self, observer, filter_name):
        lstObserver = self.image_observers.get(filter_name, [])
        if lstObserver:
            if observer in lstObserver:
                print("This observer already observer the filter %s" % filter_name)
                return False
            else:
                lstObserver.append(observer)
        else:
            self.image_observers[filter_name] = [observer]
        return True

    def remove_image_observer(self, observer, filter_name):
        lstObserver = self.image_observers.get(filter_name, [])
        if lstObserver:
            if observer in lstObserver:
                lstObserver.remove(observer)
                if not lstObserver:
                    del self.image_observers[filter_name]
                return True

        print("This observer is not in observation list for filter %s" % filter_name)
        return False

    def add_filter_output_observer(self, output):
        self.filter_output_observers.append(output)
        for f in self.filters:
            if isinstance(f, DataExtractor):
                f.add_output_observer(output)
        return True

    def remove_filter_output_observer(self, output):
        self.filter_output_observers.remove(output)
        for f in self.filters:
            if isinstance(f, DataExtractor):
                f.remove_output_observer(output)
        return True

    def execute(self, image):
        for f in self.filters:
            image = f.execute(image)
            lst_observer = self.image_observers.get(f.__class__.__name__, [])
            for observer in lst_observer:
                # copy the picture because the next filter will modify him
                observer(np.copy(image))
        return image
