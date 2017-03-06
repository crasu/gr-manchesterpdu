#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2017 <+YOU OR YOUR COMPANY+>.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from gnuradio import gr
import pmt

class manchester_pdu_decoder(gr.sync_block):
    """
    docstring for block manchester_pdu_decoder
    """
    def __init__(self):
        gr.sync_block.__init__(self,
            name="manchester_pdu_decoder",
            in_sig=None,
            out_sig=None)
        self.message_port_register_in(pmt.intern('in'))
        self.set_msg_handler(pmt.intern('in'), self.handle_msg)

    def handle_msg(self, msg):
        msg = pmt.to_python(msg)[1]
        msg_str = ''.join(chr(c) for c in msg)
        try:
            print("\nmanchester decode:{} ".format(manchester_decode(msg_str)))
        except IOError as e:
            print("\nCannot manchester decode {}".format(msg_str))

def manchester_decode(pulseStream):
    i = 1
    bits = ''

    # here pulseStream[i] is "guaranteed" to be the beginning of a bit
    while i < len(pulseStream):
        if pulseStream[i] == pulseStream[i-1]:
            i = i - 1
            raise(IOError("Cannot manchester decode {}".format(pulseStream)))
        if pulseStream[i] == '1':
            bits += '1'
        else:
            bits += '0'
        i = i + 2

    return bits

