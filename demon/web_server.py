
# coding: utf8

import tornado.wsgi
import tornado.httpserver


class web_server:

  port = '15002'

  def __init__(self, app, net_args):
    self.start_tornado(app, self.port)


  def start_tornado(self, app, port=15002):
    http_server = tornado.httpserver.HTTPServer(
      tornado.wsgi.WSGIContainer(app))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()


