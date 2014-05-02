#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) 2014 Julian Metzler
# See the LICENSE file for the full license.

"""
Setting:
- Music event
- You are in charge of the music
- You have an IBIS display on the stage
- You want it to display the current playing artist / track name

That's what this script is for.
"""

import argparse
import ibis
import thread
import time

class DisplayManager(object):
	BUFFER = ("No text here yet!", )
	INTERVAL = 3.0
	
	def __init__(self, master):
		self.master = master
	
	def process_buffer(self):
		cur_index = 0
		
		while True:
			cur_text = self.BUFFER[cur_index]
			self.master.send_next_stop__003c(cur_text)
			time.sleep(self.INTERVAL)
			
			if cur_index == len(self.BUFFER) - 1:
				cur_index = 0
			else:
				cur_index += 1
		
		return True
	
	def input_loop(self):
		fb2 = ibis.simulation.DisplayFont("../simulation-font/bold/.fontmap", spacing = 2)
		fb1 = ibis.simulation.DisplayFont("../simulation-font/bold/.fontmap", spacing = 1)
		fn2 = ibis.simulation.DisplayFont("../simulation-font/narrow/.fontmap", spacing = 2)
		fn1 = ibis.simulation.DisplayFont("../simulation-font/narrow/.fontmap", spacing = 1)
		while True:
			artist = raw_input("Artist: ")
			title = raw_input("Title: ")
			
			one_line = "%s - %s" % (artist, title)
			
			fits_in_one_line = False
			for font in (fb2, fb1, fn2, fn1):
				if font.get_width(one_line) <= 120:
					fits_in_one_line = True
					break
			
			if fits_in_one_line:
				self.BUFFER = (one_line, )
			else:
				self.BUFFER = (artist, title)
			
			print "\n"
		return True

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('-d', '--device', type = str, default = "/dev/ttyUSB0", help = "The serial device to use for IBIS communication")
	parser.add_argument('-i', '--interval', type = float, default = 3.0, help = "The interval between artist and title display (in seconds)")
	args = parser.parse_args()
	
	master = ibis.IBISMaster(args.device)
	mgr = DisplayManager(master)
	mgr.INTERVAL = args.interval
	
	thread.start_new_thread(mgr.process_buffer, ())
	try:
		mgr.input_loop()
	except KeyboardInterrupt:
		pass

if __name__ == "__main__":
	main()