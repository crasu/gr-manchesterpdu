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
import sys
import time

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
        self.message_port_register_out(pmt.intern('out'))

    def handle_msg(self, msg):
        print("Handle msg called")
        msg_str = manchester_pdu_decoder.str_from_msg(msg)
        try:
            print("manchester decode:{}\n".format(msg_str))
            decode = manchester_pdu_decoder.manchester_decode(msg_str)
            pdu = pmt.cons(pmt.PMT_NIL, manchester_pdu_decoder.vector_from_str(decode))
            self.message_port_pub(pmt.intern('out'), pdu)
        except IOError as e:
            print("Cannot manchester decode {}\n".format(msg_str))
        sys.stdout.flush()

    @staticmethod
    def str_from_msg(msg):
        msg = pmt.to_python(msg)[1]
        msg_str = ''.join(chr(c) for c in msg)
        return msg_str

    @staticmethod
    def vector_from_str(value_str):
        send_pmt = pmt.make_u8vector(len(value_str), ord(' '))

        for i in range(len(value_str)):
            pmt.u8vector_set(send_pmt, i, ord(value_str[i]))

        return send_pmt

    @staticmethod
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

