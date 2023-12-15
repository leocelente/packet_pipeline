#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Radiosonde RF Multiplexer
# Author: leocelente
# Description: Turns a single 960ksps BW RTL-SDR signal to multiple 48ksps in UDP ports for processing using rs41mod
# GNU Radio version: 3.10.1.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
from gnuradio.filter import firdes
import sip
from gnuradio import filter
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import network
import osmosdr
import time



from gnuradio import qtgui

class options_0(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Radiosonde RF Multiplexer", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Radiosonde RF Multiplexer")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "options_0")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 960000
        self.decimation = decimation = 20
        self.xlating_offset_2 = xlating_offset_2 = .300E6
        self.xlating_offset_1 = xlating_offset_1 = -.300E6
        self.xlating_offset_0 = xlating_offset_0 = 0E6
        self.samp_rate_decimated = samp_rate_decimated = samp_rate/decimation
        self.center_freq = center_freq = 403E6

        ##################################################
        # Blocks
        ##################################################
        self.rtlsdr_source_0 = osmosdr.source(
            args="numchan=" + str(1) + " " + ""
        )
        self.rtlsdr_source_0.set_clock_source('external', 0)
        self.rtlsdr_source_0.set_time_unknown_pps(osmosdr.time_spec_t())
        self.rtlsdr_source_0.set_sample_rate(samp_rate)
        self.rtlsdr_source_0.set_center_freq(center_freq, 0)
        self.rtlsdr_source_0.set_freq_corr(0, 0)
        self.rtlsdr_source_0.set_dc_offset_mode(0, 0)
        self.rtlsdr_source_0.set_iq_balance_mode(0, 0)
        self.rtlsdr_source_0.set_gain_mode(True, 0)
        self.rtlsdr_source_0.set_gain(10, 0)
        self.rtlsdr_source_0.set_if_gain(20, 0)
        self.rtlsdr_source_0.set_bb_gain(20, 0)
        self.rtlsdr_source_0.set_antenna('', 0)
        self.rtlsdr_source_0.set_bandwidth(samp_rate, 0)
        self.qtgui_freq_sink_x_1 = qtgui.freq_sink_c(
            1024, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            center_freq, #fc
            samp_rate, #bw
            "", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_1.set_update_time(0.11)
        self.qtgui_freq_sink_x_1.set_y_axis(-100, 20)
        self.qtgui_freq_sink_x_1.set_y_label('', '')
        self.qtgui_freq_sink_x_1.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_1.enable_autoscale(False)
        self.qtgui_freq_sink_x_1.enable_grid(True)
        self.qtgui_freq_sink_x_1.set_fft_average(1.0)
        self.qtgui_freq_sink_x_1.enable_axis_labels(True)
        self.qtgui_freq_sink_x_1.enable_control_panel(False)
        self.qtgui_freq_sink_x_1.set_fft_window_normalized(False)

        self.qtgui_freq_sink_x_1.disable_legend()


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_1.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_1.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_1.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_1.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_1.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_1_win = sip.wrapinstance(self.qtgui_freq_sink_x_1.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_1_win, 0, 0, 1, 3)
        for r in range(0, 1):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0_0_0 = qtgui.freq_sink_c(
            256, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            center_freq + xlating_offset_2, #fc
            samp_rate_decimated, #bw
            "403.3MHz", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0_0.set_update_time(0.13)
        self.qtgui_freq_sink_x_0_0_0.set_y_axis(-100, 20)
        self.qtgui_freq_sink_x_0_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0_0.enable_grid(True)
        self.qtgui_freq_sink_x_0_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0_0.enable_axis_labels(False)
        self.qtgui_freq_sink_x_0_0_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0_0.set_fft_window_normalized(False)

        self.qtgui_freq_sink_x_0_0_0.disable_legend()


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_0_0_win, 1, 2, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(2, 3):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0_0 = qtgui.freq_sink_c(
            256, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            center_freq + xlating_offset_1, #fc
            samp_rate_decimated, #bw
            "402.7MHz", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0_0.set_update_time(0.12)
        self.qtgui_freq_sink_x_0_0.set_y_axis(-100, 20)
        self.qtgui_freq_sink_x_0_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0, 0, "")
        self.qtgui_freq_sink_x_0_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0_0.enable_grid(True)
        self.qtgui_freq_sink_x_0_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0_0.enable_axis_labels(False)
        self.qtgui_freq_sink_x_0_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0_0.set_fft_window_normalized(False)

        self.qtgui_freq_sink_x_0_0.disable_legend()


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_0_win, 1, 0, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(0, 1):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.qtgui_freq_sink_x_0 = qtgui.freq_sink_c(
            256, #size
            window.WIN_BLACKMAN_hARRIS, #wintype
            center_freq - xlating_offset_0, #fc
            samp_rate_decimated, #bw
            "403MHz", #name
            1,
            None # parent
        )
        self.qtgui_freq_sink_x_0.set_update_time(0.10)
        self.qtgui_freq_sink_x_0.set_y_axis(-100, 20)
        self.qtgui_freq_sink_x_0.set_y_label('Relative Gain', 'dB')
        self.qtgui_freq_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, 0.0, 0, "")
        self.qtgui_freq_sink_x_0.enable_autoscale(False)
        self.qtgui_freq_sink_x_0.enable_grid(True)
        self.qtgui_freq_sink_x_0.set_fft_average(1.0)
        self.qtgui_freq_sink_x_0.enable_axis_labels(False)
        self.qtgui_freq_sink_x_0.enable_control_panel(False)
        self.qtgui_freq_sink_x_0.set_fft_window_normalized(False)

        self.qtgui_freq_sink_x_0.disable_legend()


        labels = ['', '', '', '', '',
            '', '', '', '', '']
        widths = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
            "magenta", "yellow", "dark red", "dark green", "dark blue"]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
            1.0, 1.0, 1.0, 1.0, 1.0]

        for i in range(1):
            if len(labels[i]) == 0:
                self.qtgui_freq_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_freq_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_freq_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_freq_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_freq_sink_x_0.set_line_alpha(i, alphas[i])

        self._qtgui_freq_sink_x_0_win = sip.wrapinstance(self.qtgui_freq_sink_x_0.qwidget(), Qt.QWidget)
        self.top_grid_layout.addWidget(self._qtgui_freq_sink_x_0_win, 1, 1, 1, 1)
        for r in range(1, 2):
            self.top_grid_layout.setRowStretch(r, 1)
        for c in range(1, 2):
            self.top_grid_layout.setColumnStretch(c, 1)
        self.network_udp_sink_0_0_0 = network.udp_sink(gr.sizeof_gr_complex, 1, '127.0.0.1', 4033, 0, 1472, False)
        self.network_udp_sink_0_0 = network.udp_sink(gr.sizeof_gr_complex, 1, '127.0.0.1', 4027, 0, 1472, False)
        self.network_udp_sink_0 = network.udp_sink(gr.sizeof_gr_complex, 1, '127.0.0.1', 4030, 0, 1472, False)
        self.freq_xlating_fft_filter_ccc_0_0_0 = filter.freq_xlating_fft_filter_ccc(decimation,  firdes.complex_band_pass(1, samp_rate, -samp_rate/(2*decimation), samp_rate/(2*decimation), 1e3), xlating_offset_2, samp_rate)
        self.freq_xlating_fft_filter_ccc_0_0_0.set_nthreads(1)
        self.freq_xlating_fft_filter_ccc_0_0_0.declare_sample_delay(0)
        self.freq_xlating_fft_filter_ccc_0_0 = filter.freq_xlating_fft_filter_ccc(decimation,  firdes.complex_band_pass(1, samp_rate, -samp_rate/(2*decimation), samp_rate/(2*decimation), 1e3), xlating_offset_1, samp_rate)
        self.freq_xlating_fft_filter_ccc_0_0.set_nthreads(1)
        self.freq_xlating_fft_filter_ccc_0_0.declare_sample_delay(0)
        self.freq_xlating_fft_filter_ccc_0 = filter.freq_xlating_fft_filter_ccc(decimation,  firdes.complex_band_pass(1, samp_rate, -samp_rate/(2*decimation), samp_rate/(2*decimation), 1e3), xlating_offset_0, samp_rate)
        self.freq_xlating_fft_filter_ccc_0.set_nthreads(1)
        self.freq_xlating_fft_filter_ccc_0.declare_sample_delay(0)


        ##################################################
        # Connections
        ##################################################
        self.connect((self.freq_xlating_fft_filter_ccc_0, 0), (self.network_udp_sink_0, 0))
        self.connect((self.freq_xlating_fft_filter_ccc_0, 0), (self.qtgui_freq_sink_x_0, 0))
        self.connect((self.freq_xlating_fft_filter_ccc_0_0, 0), (self.network_udp_sink_0_0, 0))
        self.connect((self.freq_xlating_fft_filter_ccc_0_0, 0), (self.qtgui_freq_sink_x_0_0, 0))
        self.connect((self.freq_xlating_fft_filter_ccc_0_0_0, 0), (self.network_udp_sink_0_0_0, 0))
        self.connect((self.freq_xlating_fft_filter_ccc_0_0_0, 0), (self.qtgui_freq_sink_x_0_0_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.freq_xlating_fft_filter_ccc_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.freq_xlating_fft_filter_ccc_0_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.freq_xlating_fft_filter_ccc_0_0_0, 0))
        self.connect((self.rtlsdr_source_0, 0), (self.qtgui_freq_sink_x_1, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "options_0")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_samp_rate_decimated(self.samp_rate/self.decimation)
        self.freq_xlating_fft_filter_ccc_0.set_taps( firdes.complex_band_pass(1, self.samp_rate, -self.samp_rate/(2*self.decimation), self.samp_rate/(2*self.decimation), 1e3))
        self.freq_xlating_fft_filter_ccc_0_0.set_taps( firdes.complex_band_pass(1, self.samp_rate, -self.samp_rate/(2*self.decimation), self.samp_rate/(2*self.decimation), 1e3))
        self.freq_xlating_fft_filter_ccc_0_0_0.set_taps( firdes.complex_band_pass(1, self.samp_rate, -self.samp_rate/(2*self.decimation), self.samp_rate/(2*self.decimation), 1e3))
        self.qtgui_freq_sink_x_1.set_frequency_range(self.center_freq, self.samp_rate)
        self.rtlsdr_source_0.set_sample_rate(self.samp_rate)
        self.rtlsdr_source_0.set_bandwidth(self.samp_rate, 0)

    def get_decimation(self):
        return self.decimation

    def set_decimation(self, decimation):
        self.decimation = decimation
        self.set_samp_rate_decimated(self.samp_rate/self.decimation)
        self.freq_xlating_fft_filter_ccc_0.set_taps( firdes.complex_band_pass(1, self.samp_rate, -self.samp_rate/(2*self.decimation), self.samp_rate/(2*self.decimation), 1e3))
        self.freq_xlating_fft_filter_ccc_0_0.set_taps( firdes.complex_band_pass(1, self.samp_rate, -self.samp_rate/(2*self.decimation), self.samp_rate/(2*self.decimation), 1e3))
        self.freq_xlating_fft_filter_ccc_0_0_0.set_taps( firdes.complex_band_pass(1, self.samp_rate, -self.samp_rate/(2*self.decimation), self.samp_rate/(2*self.decimation), 1e3))

    def get_xlating_offset_2(self):
        return self.xlating_offset_2

    def set_xlating_offset_2(self, xlating_offset_2):
        self.xlating_offset_2 = xlating_offset_2
        self.freq_xlating_fft_filter_ccc_0_0_0.set_center_freq(self.xlating_offset_2)
        self.qtgui_freq_sink_x_0_0_0.set_frequency_range(self.center_freq + self.xlating_offset_2, self.samp_rate_decimated)

    def get_xlating_offset_1(self):
        return self.xlating_offset_1

    def set_xlating_offset_1(self, xlating_offset_1):
        self.xlating_offset_1 = xlating_offset_1
        self.freq_xlating_fft_filter_ccc_0_0.set_center_freq(self.xlating_offset_1)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(self.center_freq + self.xlating_offset_1, self.samp_rate_decimated)

    def get_xlating_offset_0(self):
        return self.xlating_offset_0

    def set_xlating_offset_0(self, xlating_offset_0):
        self.xlating_offset_0 = xlating_offset_0
        self.freq_xlating_fft_filter_ccc_0.set_center_freq(self.xlating_offset_0)
        self.qtgui_freq_sink_x_0.set_frequency_range(self.center_freq - self.xlating_offset_0, self.samp_rate_decimated)

    def get_samp_rate_decimated(self):
        return self.samp_rate_decimated

    def set_samp_rate_decimated(self, samp_rate_decimated):
        self.samp_rate_decimated = samp_rate_decimated
        self.qtgui_freq_sink_x_0.set_frequency_range(self.center_freq - self.xlating_offset_0, self.samp_rate_decimated)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(self.center_freq + self.xlating_offset_1, self.samp_rate_decimated)
        self.qtgui_freq_sink_x_0_0_0.set_frequency_range(self.center_freq + self.xlating_offset_2, self.samp_rate_decimated)

    def get_center_freq(self):
        return self.center_freq

    def set_center_freq(self, center_freq):
        self.center_freq = center_freq
        self.qtgui_freq_sink_x_0.set_frequency_range(self.center_freq - self.xlating_offset_0, self.samp_rate_decimated)
        self.qtgui_freq_sink_x_0_0.set_frequency_range(self.center_freq + self.xlating_offset_1, self.samp_rate_decimated)
        self.qtgui_freq_sink_x_0_0_0.set_frequency_range(self.center_freq + self.xlating_offset_2, self.samp_rate_decimated)
        self.qtgui_freq_sink_x_1.set_frequency_range(self.center_freq, self.samp_rate)
        self.rtlsdr_source_0.set_center_freq(self.center_freq, 0)




def main(top_block_cls=options_0, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
