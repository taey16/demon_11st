
local app  = require('waffle') {
  autocache = true, debug = true
}
--local async = require 'async'
package.path = '/works/demon_11st/lua/?.lua;' .. package.path
local agent_attribute= require 'agent.agent_attribute'
local downloader = require 'utils.demon_utils'


function download_get_req(imageurl)
  return downloader.download_image(imageurl)
end


function call_feature_demon(image_filename)
  local sentence, sentence_scores = agent_attribute.get_attribute(image_filename)
  return {sentence=sentence, sentence_scores=sentence_scores}
end


function encode_table(_query_url, _sentence, _sentence_scores, _flag_result)
  assert(_query_url, 
    string.format('ERROR check query_url: %s', _query_url)
  )
  local result = {
    url = _query_url,
    sentence = _sentence,
    sentence_scores = _sentence_scores,
    result_sentence = _flag_result,
  }
  return result
end


app.get("/attribute_request_handler", function(req, res)
  local query_url = req.url.args.url or nil
  local filename = req.url.args.local_path or nil
  local result = {}
  if query_url then
    filename = download_get_req(query_url)
  elseif filename then
    query_url = filename
  end
  print('Start caption:')
  local sentence_info = call_feature_demon(filename)
  sentence = sentence_info.sentence
  sentence_scores = sentence_info.sentence_scores
  print(sentence_info)
  --for i,word in pairs(sentence) do
  --  print(string.format('%s %f', word, sentence_scores[i]))
  --end
  result = encode_table(
    query_url, sentence_info.sentence, sentence_info.sentence_scores, true)
  res.json(result)
  --os.execute('rm -f '..filename)
end)


app.error(404, function(description, req, res)
  local url = string.format('%s%s', req.headers.host, req.url.path)
  res.status(404).send('No page found at ' .. url .. 
    'does not support browser_request')
end)


app.error(500, function(description, req, res)
  local url = string.format('%s%s', req.headers.host, req.url.path)
  if app.debug then
    res.status(500).send(description .. ' request: ' .. url)
  else
    res.status(500).send('500 Error')
  end
end)


local options = {}
options.host = 
  '10.202.34.172'
  --'10.202.34.211'
  --'10.202.35.109'
options.port = '8080'
app.listen(options)


