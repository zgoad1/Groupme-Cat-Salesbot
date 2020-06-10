import re
import urllib.parse


#
# Methods for converting an IRI (International Resource Identifier) to a URI,
# which uses only ASCII characters, which is what requests.get takes.
#
# Source:
# https://stackoverflow.com/questions/4389572/how-to-fetch-a-non-ascii-url-with-python-urlopen
#


def urlEncodeNonAscii(b):
	return re.sub('[\x80-\xFF]', lambda c: '%%%02x' % ord(c.group(0)), b.decode('utf-8'))


def iriToUri(iri):
	parts= urllib.parse.urlparse(iri)
	return urllib.parse.urlunparse(
		urlEncodeNonAscii(part.encode('utf-8')) for part in parts)
