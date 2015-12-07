
# coding: utf8

import tornado.wsgi
import tornado.httpserver


class web_server:

  # for real demon
  #port = '8080'
  # for dev.
  #port = '15002'

  def __init__(self, app, port=8080):
    print('Start tornado server port: %d' % port)
    self.start_tornado(app, port)


  def start_tornado(self, app, port):
    http_server = tornado.httpserver.HTTPServer(
      tornado.wsgi.WSGIContainer(app))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()


