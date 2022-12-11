#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2016 <+YOU OR YOUR COMPANY+>.
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
import pmt
import time
from gnuradio import gr, gr_unittest
from gnuradio import blocks
from manchesterpdu import manchester_pdu_decoder
from manchesterpdu.manchester_pdu_decoder import ManchesterMode

class ManchesterFlowgraph(object):
    def __init__(self, mode):
        self.tb=gr.top_block()
        self.mode=mode
        self.setup_flow_graph()

    def setup_flow_graph(self):
        self.tb=gr.top_block()
        self.decoder=manchester_pdu_decoder(self.mode)
        self.dbg=blocks.message_debug()
        self.tb.msg_connect(self.decoder, "out", self.dbg, "store")

    def run_flow_graph(self):
        self.tb.start()
        time.sleep(0.2)
        self.tb.stop()
        self.tb.wait()
    
    def post_str(self, input):
        msg = create_msg(input)
        self.decoder.to_basic_block()._post(pmt.intern("in"), msg)
        self.run_flow_graph()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.tb = None
        self.src = None
        self.decoder = None


def message_to_str(msg):
    data = pmt.u8vector_elements(pmt.cdr(msg))
    return "".join([chr(i) for i in data])

def str_to_array(binstr):
    return [int(x) for x in list (binstr)]

def create_msg(input):
    send_pmt = pmt.make_u8vector(len(input), ord(' '))
    for i in range(len(input)):
        pmt.u8vector_set(send_pmt, i, ord(input[i]))
    msg = pmt.cons(pmt.PMT_NIL, send_pmt)
    return msg


class manchesterpdu (gr_unittest.TestCase):
    def test_msg_decodes(self):
        modes = {
            ManchesterMode.NORMAL: "0100",
            ManchesterMode.IEEE: "1011",
        }

        for mode, result in modes.items():
            with ManchesterFlowgraph(mode) as fg:
                fg.post_str("10011010")
                self.assertEqual(fg.dbg.num_messages(), 1)
                msg = fg.dbg.get_message(0)
                self.assertEqual(message_to_str(msg), result)

    def test_differential_decode(self):
        modes = {
            ManchesterMode.DIFFERENTIAL_BPM: "0101",
            ManchesterMode.DIFFERENTIAL_BPS: "1010",
        }

        for mode, result in modes.items():
            with ManchesterFlowgraph(mode) as fg:
                fg.post_str("00101101")
                self.assertEqual(fg.dbg.num_messages(), 1)
                msg = fg.dbg.get_message(0)
                self.assertEqual(message_to_str(msg), result)

    
    def test_msg_all_zero(self):
        modes = [
            ManchesterMode.NORMAL,
            ManchesterMode.DIFFERENTIAL_BPS,
        ]

        for mode in modes:
            with ManchesterFlowgraph(mode) as fg:
                fg.post_str("000")
                self.assertEqual(fg.dbg.num_messages(), 0)

    
    def test_ignore_msg_cut_off(self):
        with ManchesterFlowgraph(ManchesterMode.NORMAL) as fg:
            fg.post_str("010")
            self.assertEqual(fg.dbg.num_messages(), 1)
            msg = fg.dbg.get_message(0)
            self.assertEqual(message_to_str(msg), "1")


    def test_ignore_msg_cut_off_diffential(self):
        with ManchesterFlowgraph(ManchesterMode.DIFFERENTIAL_BPM) as fg:
            fg.post_str("001")
            self.assertEqual(fg.dbg.num_messages(), 1)
            msg = fg.dbg.get_message(0)
            self.assertEqual(message_to_str(msg), "0")


if __name__ == '__main__':
    gr_unittest.run(manchesterpdu)
