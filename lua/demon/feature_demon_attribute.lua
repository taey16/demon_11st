
local app  = require('waffle') {
  autocache = true
}
local async = require 'async'
--require 'image'
package.path = '/works/demon_11st/lua/?.lua;' .. package.path
local agent = require 'agent.agent_attribute'
local downloader = require 'utils.demon_utils'


function download_get_req(imageurl)
  return downloader.download_image(imageurl)
end


function call_feature_demon(image_filename)
  --return agent.predict(input_data)
  return agent.get_attribute(image_filename)
end


function encode_table(_query_url, _sentence, _flag_result)
  assert(_query_url, 
    string.format('ERROR check query_url: %s', _query_url)
  )
  local result = {
    url = _query_url,
    sentence = _sentence,
    result_sentence = _flag_result,
  }
  return result
end


app.get("/attribute_request_handler", function(req, res)
  local query_url = req.url.args.url or nil
  local result = {}
  if query_url then
    local filename = download_get_req(query_url)
    --local img = image.load(filename)
    print('Start caption:')
    local sentence = call_feature_demon(filename)
    for i,sent in pairs(sentence) do
      print(sent)
    end
    result = encode_table(query_url, sentence, true)
  else
    result = encode_table(query_url, '', false)
  end
  res.json(result)
  os.execute('rm -f '..filename)
end)


app.error(404, function(description, req, res)
  local url = string.format('%s%s', req.headers.host, req.url.path)
  res.status(404).send('No page found at ' .. url .. 
    'does not support browser_request')
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
options.host = 
  '10.202.34.172'
  --'10.202.35.109'
options.port = '8080'
app.listen(options)


