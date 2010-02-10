from pyinotify import WatchManager, Notifier, ThreadedNotifier, ProcessEvent, EventsCodes
import os
import sys
#import signal


class FileChangeHandler(ProcessEvent):
	'''Callback for the pyinotify library. 
Accepts events from the library if a file changes and sets the lastevent time and sets the untracked_changes flag to True'''

	def process_IN_MODIFY(self, event):
		self.check(event, "IN_MODIFY")

	def process_IN_DELETE_SELF(self, event):
		self.check(event, "IN_DELETE_SELF")

	def process_IN_DELETE(self, event):
		self.check(event, "IN_DELETE")

	def process_IN_CREATE(self, event):
		self.check(event, "IN_CREATE")

	def process_IN_CLOSE_WRITE(self, event):
		self.check(event, "IN_CLOSE_WRITE")

	def process_IN_MOVE_SELF(self, event):
		self.check(event, "IN_MOVE_SELF")

	def process_IN_MOVED_TO(self, event):
		self.check(event, "IN_MOVED_TO")

	def process_IN_MOVED_FROM(self, event):
		self.check(event, "IN_MOVED_FROM")

	def check(self, event, typ="undefined"):
		print "event: %s" %typ



#def discontinue_processing(signl, frme):
#	print "bye"
#	global notifier
#	try:
#		notifier.stop()
#	except RuntimeError:
#		pass
#	except OSError:
#		pass
#	except KeyError:
#		pass
#	return 0




if __name__ == '__main__':
	watch = "."
	if len(sys.argv)>1 and sys.argv[1]:
		if os.path.exists(sys.argv[1]):
			watch = sys.argv[1]
		else:
			print "%s does not exist!" % sys.argv[1]
			sys.exit(1)
	else:
		print "reminder: you can add a folder to watch!"

	FLAGS=EventsCodes.ALL_FLAGS
	mask = FLAGS['IN_MODIFY'] | FLAGS['IN_DELETE_SELF']|FLAGS['IN_DELETE'] | FLAGS['IN_CREATE'] | FLAGS['IN_CLOSE_WRITE'] | FLAGS['IN_MOVE_SELF'] | FLAGS['IN_MOVED_TO'] | FLAGS['IN_MOVED_FROM'] # watched events

	wm = WatchManager()
	#addin the watched directories
	wm.add_watch(watch, mask, rec=True)
	global notifier
	notifier = ThreadedNotifier(wm, FileChangeHandler())
	notifier.start()

#	signal.signal( signal.SIGINT, discontinue_processing )

	print "do something in %s to fire events" % watch

