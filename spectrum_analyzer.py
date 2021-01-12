#!/usr/bin/env python2
# -*- coding: utf-8 -*-
##################################################
# GNU Radio Python Flow Graph
# Title: Spectrum Analyzer
# Author: Leandro Aurelio
# Description: spec.analyzer
# Generated: Tue Jan 12 18:13:26 2021
##################################################


if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from gnuradio import analog
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import fftsink2
from gnuradio.wxgui import forms
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import osmosdr
import time
import wx


class spectrum_analyzer(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Spectrum Analyzer")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.rf_gain = rf_gain = 0
        self.frequency = frequency = 40e6
        self.bandwidth = bandwidth = 3e6

        ##################################################
        # Blocks
        ##################################################
        self._rf_gain_chooser = forms.drop_down(
        	parent=self.GetWin(),
        	value=self.rf_gain,
        	callback=self.set_rf_gain,
        	label='rf_gain',
        	choices=[0, 20, 40],
        	labels=[],
        )
        self.Add(self._rf_gain_chooser)
        _frequency_sizer = wx.BoxSizer(wx.VERTICAL)
        self._frequency_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_frequency_sizer,
        	value=self.frequency,
        	callback=self.set_frequency,
        	label='frequency',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._frequency_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_frequency_sizer,
        	value=self.frequency,
        	callback=self.set_frequency,
        	minimum=25e6,
        	maximum=1750e6,
        	num_steps=1000,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_frequency_sizer)
        _bandwidth_sizer = wx.BoxSizer(wx.VERTICAL)
        self._bandwidth_text_box = forms.text_box(
        	parent=self.GetWin(),
        	sizer=_bandwidth_sizer,
        	value=self.bandwidth,
        	callback=self.set_bandwidth,
        	label='bandwidth',
        	converter=forms.float_converter(),
        	proportion=0,
        )
        self._bandwidth_slider = forms.slider(
        	parent=self.GetWin(),
        	sizer=_bandwidth_sizer,
        	value=self.bandwidth,
        	callback=self.set_bandwidth,
        	minimum=1e6,
        	maximum=3e6,
        	num_steps=100,
        	style=wx.SL_HORIZONTAL,
        	cast=float,
        	proportion=1,
        )
        self.Add(_bandwidth_sizer)
        self.wxgui_waterfallsink2_0 = waterfallsink2.waterfall_sink_c(
        	self.GetWin(),
        	baseband_freq=frequency,
        	dynamic_range=100,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=bandwidth,
        	fft_size=1024,
        	fft_rate=15,
        	average=True,
        	avg_alpha=None,
        	title='Waterfall Plot',
        )
        self.Add(self.wxgui_waterfallsink2_0.win)
        self.wxgui_fftsink2_0 = fftsink2.fft_sink_c(
        	self.GetWin(),
        	baseband_freq=frequency,
        	y_per_div=10,
        	y_divs=10,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=bandwidth,
        	fft_size=1024,
        	fft_rate=15,
        	average=True,
        	avg_alpha=None,
        	title='FFT Plot',
        	peak_hold=False,
        )
        self.Add(self.wxgui_fftsink2_0.win)
        self.osmosdr_source_0 = osmosdr.source( args="numchan=" + str(1) + " " + '' )
        self.osmosdr_source_0.set_sample_rate(bandwidth)
        self.osmosdr_source_0.set_center_freq(frequency, 0)
        self.osmosdr_source_0.set_freq_corr(0, 0)
        self.osmosdr_source_0.set_dc_offset_mode(2, 0)
        self.osmosdr_source_0.set_iq_balance_mode(2, 0)
        self.osmosdr_source_0.set_gain_mode(False, 0)
        self.osmosdr_source_0.set_gain(rf_gain, 0)
        self.osmosdr_source_0.set_if_gain(20, 0)
        self.osmosdr_source_0.set_bb_gain(20, 0)
        self.osmosdr_source_0.set_antenna('', 0)
        self.osmosdr_source_0.set_bandwidth(0, 0)

        self.blocks_threshold_ff_0_0 = blocks.threshold_ff(21, 32, 0)
        self.blocks_threshold_ff_0 = blocks.threshold_ff(5, 18, 0)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vcc((7.1, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vcc((15.75, ))
        self.blocks_float_to_complex_0_0 = blocks.float_to_complex(1)
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_divide_xx_0 = blocks.divide_cc(1)
        self.blocks_add_const_vxx_0_0 = blocks.add_const_vcc((1, ))
        self.blocks_add_const_vxx_0 = blocks.add_const_vcc((1, ))
        self.analog_const_source_x_1 = analog.sig_source_c(0, analog.GR_CONST_WAVE, 0, 0, 2.278)
        self.analog_const_source_x_0_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, rf_gain)
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, rf_gain)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_threshold_ff_0, 0))
        self.connect((self.analog_const_source_x_0_0, 0), (self.blocks_threshold_ff_0_0, 0))
        self.connect((self.analog_const_source_x_1, 0), (self.blocks_divide_xx_0, 1))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_divide_xx_0, 2))
        self.connect((self.blocks_add_const_vxx_0_0, 0), (self.blocks_divide_xx_0, 3))
        self.connect((self.blocks_divide_xx_0, 0), (self.wxgui_fftsink2_0, 0))
        self.connect((self.blocks_divide_xx_0, 0), (self.wxgui_waterfallsink2_0, 0))
        self.connect((self.blocks_float_to_complex_0, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.blocks_float_to_complex_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_add_const_vxx_0_0, 0))
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_float_to_complex_0, 1))
        self.connect((self.blocks_threshold_ff_0, 0), (self.blocks_float_to_complex_0, 0))
        self.connect((self.blocks_threshold_ff_0_0, 0), (self.blocks_float_to_complex_0_0, 1))
        self.connect((self.blocks_threshold_ff_0_0, 0), (self.blocks_float_to_complex_0_0, 0))
        self.connect((self.osmosdr_source_0, 0), (self.blocks_divide_xx_0, 0))

    def get_rf_gain(self):
        return self.rf_gain

    def set_rf_gain(self, rf_gain):
        self.rf_gain = rf_gain
        self._rf_gain_chooser.set_value(self.rf_gain)
        self.osmosdr_source_0.set_gain(self.rf_gain, 0)
        self.analog_const_source_x_0_0.set_offset(self.rf_gain)
        self.analog_const_source_x_0.set_offset(self.rf_gain)

    def get_frequency(self):
        return self.frequency

    def set_frequency(self, frequency):
        self.frequency = frequency
        self._frequency_slider.set_value(self.frequency)
        self._frequency_text_box.set_value(self.frequency)
        self.wxgui_waterfallsink2_0.set_baseband_freq(self.frequency)
        self.wxgui_fftsink2_0.set_baseband_freq(self.frequency)
        self.osmosdr_source_0.set_center_freq(self.frequency, 0)

    def get_bandwidth(self):
        return self.bandwidth

    def set_bandwidth(self, bandwidth):
        self.bandwidth = bandwidth
        self._bandwidth_slider.set_value(self.bandwidth)
        self._bandwidth_text_box.set_value(self.bandwidth)
        self.wxgui_waterfallsink2_0.set_sample_rate(self.bandwidth)
        self.wxgui_fftsink2_0.set_sample_rate(self.bandwidth)
        self.osmosdr_source_0.set_sample_rate(self.bandwidth)


def main(top_block_cls=spectrum_analyzer, options=None):

    tb = top_block_cls()
    tb.Start(True)
    tb.Wait()


if __name__ == '__main__':
    main()
