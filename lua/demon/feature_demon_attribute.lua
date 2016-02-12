
local app  = require('../waffle') {
  autocache = true
}
local async= require 'async'
require 'image'
package.path = '/works/demon_11st/lua/?.lua;' .. package.path
local agent = require 'agent.agent_attribute'
local downloader = require 'utils.demon_utils'


function download_get_req(imageurl)
  return downloader.download_image(imageurl)
end


function call_feature_demon(input_data)
  return agent.predict(input_data)
end


app.get("/attribute_request_handler", function(req, res)
  local query_url = req.url.args.url or nil
  local result = {}
  if query_url then
    local filename = download_get_req(query_url)
    local img = image.load(filename)
    print('Start caption:')
    local sentence = call_feature_demon(img)
    print(sentence)
    result = {
      url = query_url,
      sentence = sentence,
      result = true
    }
  else
    result = {
      url = query_url,
      result = false
    } 
  end
  res.json(result)
  os.execute('rm -f '..filename)
end)


app.error(404, function(description, req, res)
  local url = string.format('%s%s', req.headers.host, req.url.path)
  res.status(404).send('No page found at ' .. url)
end)


app.error(500, function(description, req, res)
  local url = string.format('%s%s', req.headers.host, req.url.path)
  res.status(500).send(description .. ' request: ' .. url)
  --[[
  if app.debug then
    res.status(500).send(description)
  else
    res.status(500).send('500 Error')
  end
  --]]
end)


local options = {}
options.host = '10.202.4.219'
options.port = '8080'
app.listen(options)


