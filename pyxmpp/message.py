
import libxml2
from stanza import Stanza,StanzaError,common_ns
from utils import to_utf8,from_utf8

message_types=("normal","chat","headline")

class Message(Stanza):
	stanza_type="message"
	def __init__(self,node=None,**kw):
		self.node=None
		if isinstance(node,Message):
			pass
		elif isinstance(node,Stanza):
			raise TypeError,"Couldn't make Message from other Stanza"
		elif isinstance(node,libxml2.xmlNode):
			pass
		elif node is not None:
			raise TypeError,"Couldn't make Message from %r" % (type(node),)
	
		if kw.has_key("type") and kw["type"] not in message_types:
			raise StanzaError,"Invalid message type: %r" % (type,)

		if kw.has_key("body"):
			body=kw["body"]
			del kw["body"]
		else:
			body=None
		if kw.has_key("subject"):
			subject=kw["subject"]
			del kw["subject"]
		else:
			subject=None
	
		if node is None:
			node="message"
		apply(Stanza.__init__,[self,node],kw)
		if subject:
			self.node.newChild(common_ns,"subject",to_utf8(subject))
		if body:
			self.node.newChild(common_ns,"body",to_utf8(body))

	def get_subject(self):
		n=self.xpath_eval("common:subject")
		if n:
			return from_utf8(n[0].getContent())
		else:
			return None
	
	def get_body(self):
		n=self.xpath_eval("common:body")
		if n:
			return from_utf8(n[0].getContent())
		else:
			return None
