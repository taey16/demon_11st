
local app  = require('../waffle')
local async= require 'async'
local gm = require 'graphicsmagick'
local model = paths.dofile('../agent/agent.lua')

local input = {}
app.get("/mosaic_request_handler", function(req, res)
  local q_url = req.url.args.query or nil
  local q_cate= req.url.args.cate or nil
  if q_url then
    async.curl.get(q_url, 
      function(res)
        local data = gm.Image():fromString(res) 
        input = data:toTensor('float', 'RGB', 'DHW')
      end
    )
    --print(input:size(1) .. 'x' .. 
    --      input:size(2) .. 'x' .. 
    --      input:size(3))
    print('Start predict:' .. q_url)
    scores, classes, class_name = model.predict(input)
    --print(scores[{{1,5}}])
    local result_scores = scores[{{1,5}}]:totable()
    --print(#result_scores)
    for i=1,5 do
      print(class_name[i] .. ' ' .. result_scores[i])
    end
    result = {
      url = q_url,
      category = q_cate,
      score = result_scores,
      name = class_name,
      result = true} 
    res.json(result)
  else
    app.abort(400, 'request error', req, res)
  end
end)


local options = {}
options.host = '10.202.35.0'
options.port = '8080'
--app.repl({host='10.202.35.0', port='8081'})
app.listen(options)

