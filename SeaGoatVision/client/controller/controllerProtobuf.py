#!/usr/bin/env python

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
Description : This controller use protobuf to communicate to the vision server
"""

# Import required RPC modules
from SeaGoatVision.proto import server_pb2
import logging
import json
import numpy as np
from thirdparty.public.protobuf.socketrpc import RpcService
import socket
import threading
import exceptions
from SeaGoatVision.commons.param import Param
log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# The callback is for asynchronous call to RpcService
def callback(request, response):
    """Define a simple async callback."""
    log.info('Asynchronous response :' + response.__str__())

class ControllerProtobuf():
    def __init__(self, host, port, quiet=False):
        # Server details
        self.hostname = host
        self.port = int(port)
        self.quiet = quiet
        self.lst_port = []

        # Create a new service instance
        self.service = RpcService(server_pb2.CommandService_Stub, self.port, self.hostname)

        self.observer = []

    def close(self):
        for observer in self.observer:
            observer.stop()
        print("Closed connection.")

    ##########################################################################
    ################################ CLIENT ##################################
    ##########################################################################
    def is_connected(self):
        if not self.quiet:
            print("Try connection")
        request = server_pb2.IsConnectedRequest()
        # Make an synchronous call
        response = None
        try:
            response = self.service.is_connected(request, timeout=10000) is not None
            if response and not self.quiet:
                print("Connection successful")
        except Exception as ex:
            log.exception(ex)

        return response

    ##########################################################################
    ######################## EXECUTION FILTER ################################
    ##########################################################################
    def start_filterchain_execution(self, execution_name, media_name, filterchain_name, file_name=None):
        """
            Start a filterchain on the server.
            Param : str - The unique execution name
                    str - The unique media name
                    str - The unique filterchain name
        """
        request = server_pb2.StartFilterchainExecutionRequest()
        request.execution_name = execution_name
        request.media_name = media_name
        request.filterchain_name = filterchain_name
        if file_name:
            request.file_name = file_name

        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.start_filterchain_execution(request, timeout=10000)
            if response:
                returnValue = not response.status
                if not returnValue:
                    if response.HasField("message"):
                        print("Error with start_filterchain_execution : %s" % response.message)
                    else:
                        print("Error with start_filterchain_execution.")
            else:
                returnValue = False

        except Exception as ex:
            log.exception(ex)

        return returnValue

    def stop_filterchain_execution(self, execution_name):
        """
            Stop a filterchain on the server.
            Param : str - The unique execution name
        """
        request = server_pb2.StopFilterchainExecutionRequest()
        request.execution_name = execution_name
        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.stop_filterchain_execution(request, timeout=10000)

            if response:
                returnValue = not response.status
                if not returnValue:
                    if response.HasField("message"):
                        print("Error with stop_filterchain_execution : %s" % response.message)
                    else:
                        print("Error with stop_filterchain_execution.")
            else:
                returnValue = False

        except Exception as ex:
            log.exception(ex)

        return returnValue

    def get_params_filterchain(self, execution_name, filter_name):
        request = server_pb2.GetParamsFilterchainRequest()
        request.execution_name = execution_name
        request.filter_name = filter_name
        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.get_params_filterchain(request, timeout=10000)

            if response:
                returnValue = []
                for param in response.params:
                    if param.HasField("value_int"):
                        returnValue.append(Param(param.name, param.value_int, min_v=param.min_v, max_v=param.max_v))
                    if param.HasField("value_bool"):
                        returnValue.append(Param(param.name, param.value_bool))
                    if param.HasField("value_str"):
                        returnValue.append(Param(param.name, param.value_str))
                    if param.HasField("value_float"):
                        returnValue.append(Param(param.name, param.value_float, min_v=param.min_float_v, max_v=param.max_float_v))
                    # TODO complete with other param restriction
            else:
                returnValue = False

        except Exception as ex:
            log.exception(ex)

        return returnValue

    def get_execution_list(self):
        request = server_pb2.GetExecutionRequest()
        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.get_execution_list(request, timeout=10000)

            if response:
                return response.execution
        except Exception as ex:
            log.exception(ex)

        return []

    def get_execution_info(self, execution_name):
        request = server_pb2.GetExecutionInfoRequest()
        request.execution = execution_name
        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.get_execution_info(request, timeout=10000)
            if response:
                return response
        except Exception as ex:
            log.exception(ex)

        return None

    ##########################################################################
    ################################ MEDIA ##################################
    ##########################################################################
    def get_media_list(self):
        """
            Get the list for image provider.
        """
        request = server_pb2.GetMediaListRequest()
        # Make an synchronous call
        returnResponse = {}
        try:
            response = self.service.get_media_list(request, timeout=10000)
            if response:
                i = 0
                for key in response.media:
                    returnResponse[key] = response.type[i]
                    i += 1
            else:
                print("No answer on get_media_list")
        except Exception as ex:
            log.exception(ex)

        return returnResponse

    def start_record(self, media_name, path=None):
        request = server_pb2.StartRecordRequest()
        request.media = media_name
        if path:
            request.path = path
        # Make an synchronous call
        try:
            response = self.service.start_record(request, timeout=10000)
            if response:
                returnValue = not response.status
                if not returnValue:
                    if response.HasField("message"):
                        print("Error with start_record : %s" % response.message)
                    else:
                        print("Error with start_record.")
            else:
                returnValue = False
        except Exception as ex:
            log.exception(ex)

        return returnValue

    def stop_record(self, media_name):
        request = server_pb2.StopRecordRequest()
        request.media = media_name
        # Make an synchronous call
        try:
            response = self.service.stop_record(request, timeout=10000)
            if response:
                returnValue = not response.status
                if not returnValue:
                    if response.HasField("message"):
                        print("Error with stop_record : %s" % response.message)
                    else:
                        print("Error with stop_record.")
            else:
                returnValue = False
        except Exception as ex:
            log.exception(ex)

        return returnValue

    def cmd_to_media(self, media_name, cmd):
        request = server_pb2.CmdMediaRequest()
        request.media_name = media_name
        request.cmd = cmd
        # Make an synchronous call
        try:
            response = self.service.cmd_to_media(request, timeout=10000)
            if response:
                returnValue = not response.status
                if not returnValue:
                    if response.HasField("message"):
                        print("Error with cmd_to_media : %s" % response.message)
                    else:
                        print("Error with cmd_to_media.")
            else:
                returnValue = False
        except Exception as ex:
            log.exception(ex)

        return returnValue

    def get_info_media(self, media_name):
        request = server_pb2.GetInfoMediaRequest()
        request.media_name = media_name
        # Make an synchronous call
        dct_message = {}
        try:
            response = self.service.get_info_media(request, timeout=10000)
            if response:
                message = response.message
                if message:
                    dct_message = json.loads(message)
        except Exception as ex:
            log.exception(ex)

        return dct_message

    def get_params_media(self, media_name):
        request = server_pb2.GetParamsMediaRequest()
        request.media_name = media_name
        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.get_params_media(request, timeout=10000)

            if response:
                returnValue = []
                for param in response.params:
                    if param.HasField("value_int"):
                        returnValue.append(Param(param.name, param.value_int, min_v=int(param.min_v), max_v=int(param.max_v)))
                    if param.HasField("value_bool"):
                        returnValue.append(Param(param.name, param.value_bool))
                    if param.HasField("value_str"):
                        returnValue.append(Param(param.name, param.value_str))
                    if param.HasField("value_float"):
                        returnValue.append(Param(param.name, param.value_float, min_v=param.min_float_v, max_v=param.max_float_v))
                    # TODO complete with other param restriction
            else:
                returnValue = False

        except Exception as ex:
            log.exception(ex)

        return returnValue

    def update_param_media(self, media_name, param_name, value):
        request = server_pb2.UpdateParamMediaRequest()
        request.media_name = media_name
        request.param.name = param_name
        if type(value) is int:
            request.param.value_int = value
        if type(value) is bool:
            request.param.value_bool = value
        if type(value) is float:
            request.param.value_float = value
        if type(value) is str:
            request.param.value_str = value

        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.update_param_media(request, timeout=10000)
            if response:
                returnValue = not response.status
                if not returnValue:
                    if response.HasField("message"):
                        print("Error with update_param_media : %s with value %s" % (response.message, returnValue))
                    else:
                        print("Error with update_param_media value %s." % returnValue)
            else:
                returnValue = False

        except Exception as ex:
            log.exception(ex)

        return returnValue

    ##########################################################################
    ##########################  CONFIGURATION  ###############################
    ##########################################################################

    ##########################################################################
    #############################  OBSERVER  #################################
    ##########################################################################
    def add_image_observer(self, observer, execution_name, filter_name):
        """
            Inform the server what filter we want to observe
            Param :
                - ref, observer is a reference on method for callback
                - string, execution_name to select an execution
                - string, filter_name to select the filter
        """
        port = self._get_port_streaming()
        local_observer = Observer(observer, self.hostname, port)

        request = server_pb2.AddImageObserverRequest()
        request.execution_name = execution_name
        request.filter_name = filter_name
        request.port = port

        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.add_image_observer(request, timeout=10000)
            if response:
                returnValue = not response.status
                if not returnValue:
                    if response.HasField("message"):
                        print("Error with add_image_observer : %s" % response.message)
                    else:
                        print("Error with add_image_observer.")
            else:
                returnValue = False

        except Exception as ex:
            log.exception(ex)

        if not returnValue:
            local_observer.stop()
        else:
            self.observer.append(local_observer)
            local_observer.start()

        return returnValue

    def set_image_observer(self, observer, execution_name, filter_name_old, filter_name_new):
        """
            Inform the server what filter we want to observe
            Param :
                - ref, observer is a reference on method for callback
                - string, execution_name to select an execution
                - string, filter_name_old , filter to replace
                - string, filter_name_new , filter to use
        """
        find = False
        for o_observer in self.observer:
            if observer == o_observer.observer:
                 find = True
                 break
        if not find:
            print("Error: This observer doesn't exist.")
            return False

        request = server_pb2.SetImageObserverRequest()
        request.execution_name = execution_name
        request.filter_name_old = filter_name_old
        request.filter_name_new = filter_name_new

        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.set_image_observer(request, timeout=10000)
            if response:
                returnValue = not response.status
                if not returnValue:
                    if response.HasField("message"):
                        print("Error with set_image_observer : %s" % response.message)
                    else:
                        print("Error with set_image_observer.")
            else:
                returnValue = False

        except Exception as ex:
            log.exception(ex)

        return returnValue

    def remove_image_observer(self, observer, execution_name, filter_name):
        """
            Inform the server what filter we want to observe
            Param :
                - ref, observer is a reference on method for callback
                - string, execution_name to select an execution
                - string, filter_name , filter to remove
        """
        find = False
        for o_observer in self.observer:
            if observer == o_observer.observer:
                 find = True
                 break
        if not find:
            print("Error: This observer doesn't exist.")
            return False

        o_observer.stop()
        self.observer.remove(o_observer)

        request = server_pb2.RemoveImageObserverRequest()
        request.execution_name = execution_name
        request.filter_name = filter_name

        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.remove_image_observer(request, timeout=10000)
            if response:
                returnValue = not response.status
                if not returnValue:
                    if response.HasField("message"):
                        print("Error with remove_image_observer : %s" % response.message)
                    else:
                        print("Error with remove_image_observer.")
            else:
                returnValue = False

        except Exception as ex:
            log.exception(ex)

        return returnValue

    def add_output_observer(self, execution_name):
        """
            attach the output information of execution to tcp_server
            supported only one observer. Add observer to tcp_server
        """
        request = server_pb2.AddOutputObserverRequest()
        request.execution_name = execution_name

        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.add_output_observer(request, timeout=10000)
            if response:
                returnValue = not response.status
                if not returnValue:
                    if response.HasField("message"):
                        print("Error with add_output_observer : %s" % response.message)
                    else:
                        print("Error with add_output_observer.")
            else:
                returnValue = False

        except Exception as ex:
            log.exception(ex)

        return returnValue

    def remove_output_observer(self, execution_name):
        """
            remove the output information of execution to tcp_server
            supported only one observer. remove observer to tcp_server
        """
        request = server_pb2.RemoveOutputObserverRequest()
        request.execution_name = execution_name

        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.remove_output_observer(request, timeout=10000)
            if response:
                returnValue = not response.status
                if not returnValue:
                    if response.HasField("message"):
                        print("Error with remove_output_observer : %s" % response.message)
                    else:
                        print("Error with remove_output_observer.")
            else:
                returnValue = False

        except Exception as ex:
            log.exception(ex)

        return returnValue

    ##########################################################################
    ############################ FILTERCHAIN  ################################
    ##########################################################################
    def get_filterchain_list(self):
        """
            Return list of filter from filterchain.
        """
        request = server_pb2.GetFilterChainListRequest()
        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.get_filterchain_list(request, timeout=10000)
            if response:
                returnValue = response.filterchains
            else:
                print("Error : protobuf, get_filterchain_list response is None")

        except Exception as ex:
            log.exception(ex)

        return returnValue

    def get_filter_list_from_filterchain(self, filterchain_name):
        """
            Return list of filter from filterchain.
        """
        request = server_pb2.GetFilterListFromFilterChainRequest()
        request.filterchain_name = filterchain_name
        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.get_filter_list_from_filterchain(request, timeout=10000)
            if response:
                returnValue = response.filters
            else:
                print("Error : protobuf, get_filterchain_list response is None")

        except Exception as ex:
            log.exception(ex)

        return returnValue

    def delete_filterchain(self, filterchain_name):
        """
            deleter a filterchain
            Param : str - filterchain name
        """
        request = server_pb2.DeleteFilterChainRequest()
        request.filterchain_name = filterchain_name
        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.delete_filterchain(request, timeout=10000)

            if response:
                returnValue = not response.status
                if not returnValue:
                    if response.HasField("message"):
                        print("Error with delete_filterchain : %s" % response.message)
                    else:
                        print("Error with delete_filterchain.")
            else:
                returnValue = False


        except Exception as ex:
            log.exception(ex)

        return returnValue

    def upload_filterchain(self, filterchain_name, s_file_contain):
        """
            upload a filterchain
            Param : str - filterchain name
                    str - the filterchain file
        """
        request = server_pb2.UploadFilterChainRequest()
        request.filterchain_name = filterchain_name
        request.s_file_contain = s_file_contain
        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.upload_filterchain(request, timeout=10000)
            if response:
                returnValue = not response.status
                if not returnValue:
                    if response.HasField("message"):
                        print("Error with upload_filterchain : %s" % response.message)
                    else:
                        print("Error with upload_filterchain.")
            else:
                returnValue = False


        except Exception as ex:
            log.exception(ex)

        return returnValue


    def modify_filterchain(self, old_filterchain_name, new_filterchain_name, lst_str_filters):
        """
            Edit or create a new filterchain
            Param : str - old_filterchain name
                    str - new_filterchain name
                    list - the list in string of filters
        """
        request = server_pb2.ModifyFilterChainRequest()
        request.old_filterchain_name = old_filterchain_name
        request.new_filterchain_name = new_filterchain_name
        for filter_name in lst_str_filters:
            request.lst_str_filters.add().name = filter_name

        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.modify_filterchain(request, timeout=10000)
            if response:
                returnValue = not response.status
                if not returnValue:
                    if response.HasField("message"):
                        print("Error with modify_filterchain : %s" % response.message)
                    else:
                        print("Error with modify_filterchain.")
            else:
                returnValue = False


        except Exception as ex:
            log.exception(ex)

        return returnValue

    def update_param(self, execution_name, filter_name, param_name, value):
        request = server_pb2.UpdateParamRequest()
        request.execution_name = execution_name
        request.filter_name = filter_name;
        request.param.name = param_name
        if type(value) is int:
            request.param.value_int = value
        if type(value) is bool:
            request.param.value_bool = value
        if type(value) is float:
            request.param.value_float = value
        if type(value) is str:
            request.param.value_str = value

        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.update_param(request, timeout=10000)
            if response:
                returnValue = not response.status
                if not returnValue:
                    if response.HasField("message"):
                        print("Error with update_param : %s" % response.message)
                    else:
                        print("Error with update_param.")
            else:
                returnValue = False

        except Exception as ex:
            log.exception(ex)

        return returnValue

    def save_params(self, execution_name):
        request = server_pb2.SaveParamsRequest()
        request.execution_name = execution_name

        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.save_params(request, timeout=10000)
            if response:
                returnValue = not response.status
                if not returnValue:
                    if response.HasField("message"):
                        print("Error with save_params : %s" % response.message)
                    else:
                        print("Error with save_params.")
            else:
                returnValue = False

        except Exception as ex:
            log.exception(ex)

        return returnValue

    ##########################################################################
    ############################### FILTER  ##################################
    ##########################################################################
    def reload_filter(self, filtre=None):
        """
            Reload Filter.
            Param : filtre - if None, reload all filter, else reload filter name
        """
        request = server_pb2.ReloadFilterRequest()
        if type(filtre) is list:
            for item in filtre:
                request.filterName.append(item)
        elif type(filtre) is str or type(filtre) is unicode:
            request.filterName.append(filtre)
        elif filtre is not None:
            raise Exception("filtre is wrong type : %s" % type(filtre))

        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.reload_filter(request, timeout=10000)
            if response:
                returnValue = not response.status
                if not returnValue:
                    if response.HasField("message"):
                        print("Error with reload_filter : %s" % response.message)
                    else:
                        print("Error with reload_filter.")
            else:
                returnValue = False


        except Exception as ex:
            log.exception(ex)

        return returnValue

    def get_filter_list(self):
        """
            Return list of filter
        """
        request = server_pb2.GetFilterListRequest()
        # Make an synchronous call
        returnValue = None
        try:
            response = self.service.get_filter_list(request, timeout=10000)
            returnValue = {response.filters[i]:response.doc[i] for i in range(len(response.filters))}

        except Exception as ex:
            log.exception(ex)

        return returnValue

    def _get_port_streaming(self):
        port = 5051
        while port in self.lst_port:
            port += 1
        self.lst_port.append(port)
        return port

class Observer(threading.Thread):
    def __init__(self, observer, hostname, port):
        threading.Thread.__init__(self)
        self.observer = observer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.add = (hostname, port)
        self.close = False
        self.buffer = 65507

    def run(self):
        if self.observer:
            self.socket.sendto("I can see you.", self.add)
            while not self.close:
                sData = ""
                try:
                    data = self.socket.recv(self.buffer)
                    if not data:
                        continue

                    if data[0] != "b":
                        #print("wrong type index.")
                        continue

                    i = 1
                    while i < self.buffer and data[i] != "_":
                        i += 1

                    nb_packet_string = data[1:i]
                    if nb_packet_string.isdigit():
                        nb_packet = int(nb_packet_string)
                    else:
                        #print("wrong index.")
                        continue

                    sData += data[i + 1:]
                    for packet in range(1, nb_packet):
                        data, _ = self.socket.recvfrom(self.buffer)  # 262144 # 8192
                        if data[0] != "c":
                            #print("wrong type index continue")
                            continue

                        i = 1
                        while i < self.buffer and data[i] != "_":
                            i += 1

                        no_packet_string = data[1:i]
                        if no_packet_string.isdigit():
                            no_packet = int(no_packet_string)
                            #if no_packet != packet:
                                #print("Wrong no packet : %d" % packet)
                        else:
                            #print("wrong index continue.")
                            continue

                        sData += data[i + 1:]

                    self.observer(np.loads(sData))
                except Exception as e:
                    if type(e) is not exceptions.EOFError:
                        if not self.close:
                            print("Error udp observer : %s" % e)
        else:
            print("Error, self.observer is None.")

    def stop(self):
        self.close = True
        if self.socket:
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
            except:
                pass
            self.socket.close()
            self.socket = None
        print("Close client")
