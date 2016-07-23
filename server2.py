#-*- coding:utf-8 -*-

import sys, os, BaseHTTPServer

class ServerException(Exception):
	'''服务器内部错误'''
	pass

class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):

	Error_Page = """\
    <html>
    <body>
    <h1>Error accessing {path}</h1>
    <p>{msg}</p>
    </body>
    </html>
    """

	def do_GET(self):
		try:

			#文件完整路径
			full_path = os.getcwd() + self.path

			#如果该路径不存在
			if not os.path.exists(full_path):
				#抛出异常：文件未找到
				raise ServerException("'{0}' not found".format(self.path))

			#如果该路径是一个文件
			elif os.path.isfile(full_path):
				#调用 handler_file处理该文件
				self.handle_file(full_path)

			else:
				#抛出异常：该路径为不知名对象
				raise ServerException("Unknown object '{0}'".format(self.path))

		except Exception as msg:
			self.handle_error(msg)

	def handle_error(self, msg):
		content = self.Error_Page.format(path=self.path, msg=msg)
		self.send_content(content, 404)

	def handle_file(self, full_path):
		try:
			with open(full_path, 'rb') as reader:
				content = reader.read()
			self.send_content(content)
		except IOError as msg:
			msg = "'{0}' cannot be read: {1}".format(self.path, msf)
			self.handle_error(msg)

	def send_content(self, content, status=200):
		self.send_response(status)
		self.send_header("Content-Type", "text/html")
		self.send_header("Content-Length", str(len(content)))
		self.end_headers()
		self.wfile.write(content)



#-----------------------------------------------------

if __name__ == '__main__':
	serverAddress = ('', 8080)
	server = BaseHTTPServer.HTTPServer(serverAddress, RequestHandler)
	server.serve_forever()























