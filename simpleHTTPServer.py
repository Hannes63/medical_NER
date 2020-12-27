import wsgiref.simple_server
import urllib.parse
import predict

PORT = 80
BLANK_RESULT = '%5B%5D' # ==quote('[]')
URLS = ['/',
		'/index.html',
		'/bilstm.html',
		'/bilstm_crf.html',
		'/crf.html',
		'/hmm.html',
		'/css/default.css',
		'/js/ajax.js',
		'/js/buttons.js',
		'/js/jquery.min.js',
       ]

def urldecode(url):
	result = {}
	url = url.split(b'&')
	for i in url:
		i = i.split(b'=')
		result[urllib.parse.unquote(i[0].decode('utf-8'))] = urllib.parse.unquote(str(i[1].decode('utf-8')))
	return result

def application(environ, start_response):
	mode = environ.get('REQUEST_METHOD')

	if mode=='GET':
		url = environ.get('PATH_INFO')
		if url.find('/')<0:
			return [BLANK_RESULT.encode('utf-8')]
		else:
			url = url[url.find('/'):]
		if url=='/':
			url = '/index.html'
		if url in URLS:
			if url[-4:]=='.css':
				start_response('200 OK', [('Content-Type','text/css'),('charset','utf-8')])
			elif url[-3:]=='.js':
				start_response('200 OK', [('Content-Type','application/x-javascript'),('charset','utf-8')])
			else:
				start_response('200 OK', [('Content-Type','text/html'),('charset','utf-8')])
			page = open('./ui'+url,'rb').read()
			return [page]
		start_response('404 NOT FOUND', [('Content-Type','text/html'),('charset','utf-8')])
		return []
		
	try:
		datalen = int(environ.get('CONTENT_LENGTH'))
		data = environ.get('wsgi.input').read(datalen)
		if mode!='POST' or datalen==0:
			raise Exception() 
	except:
		return [BLANK_RESULT.encode('utf-8')]
		
	data = urldecode(data)
	result = predict.predict(data['model'],data['text']) + predict.look_up_dict(data['text'])
	output = urllib.parse.quote(str(result))

	start_response('200 OK', [('Content-Type','text/plain'),('charset','utf-8')])
	return [output.encode('utf-8')]

if __name__ =="__main__":
	port = PORT
	httpd = wsgiref.simple_server.make_server("0.0.0.0", port, application)
	print("serving http on port {0}...".format(str(port)))   
	httpd.serve_forever()