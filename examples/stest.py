#!/usr/bin/python -u

import libxml2
import time
import sys
import traceback
import socket

from pyxmpp import ClientStream,JID,Iq,Presence,Message

class Disconnected(Exception):
	pass

class Stream(ClientStream):
	def post_in_auth(self):
		print ":-)"
		self.write(Presence())
	def idle(self):
		if self.peer_authenticated():
			target=JID("jajcus",s.jid.domain)
			self.write(Message(to=target,body="Test"))
	def post_disconnect(self):
		raise Disconnected
	
	def get_password(self,username,realm=None,acceptable_formats=("plain",)):
		if "plain" in acceptable_formats:
			if username==u"test":
				return "123","plain"
			elif username==unicode("��tek","iso-8859-2"):
				return unicode("ziele�","iso-8859-2"),"plain"
		return None,None

libxml2.debugMemory(1)

print "creating socket..."
sock=socket.socket()
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sock.bind(("127.0.0.1",5222))
sock.listen(1)

print "creating stream..."
s=Stream(JID("localhost"))

while 1:
	print "accepting..."
	s.accept(sock)

	print "processing..."
	try:
		try:
			s.loop(1)
		finally:
			print "closing..."
			s.close()
	except KeyboardInterrupt:
		traceback.print_exc(file=sys.stderr)
		break
	except (stream.StreamError,Disconnected),e:
		traceback.print_exc(file=sys.stderr)

libxml2.cleanupParser()
if libxml2.debugMemory(1) == 0:
    print "OK"
else:
    print "Memory leak %d bytes" % (libxml2.debugMemory(1))
    libxml2.dumpMemory()
