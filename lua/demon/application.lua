
local app  = require('../waffle') {
  autocache = true
}
local async= require 'async'
local gm = require 'graphicsmagick'
local model = paths.dofile('../agent/agent.lua')
require 'image'

app.get("/mosaic_request_handler", function(req, res)
  local query_url = req.url.args.query or nil
  local q_cate = req.url.args.cate or nil
  local filename = paths.concat(
    '/tmp/' .. tostring(torch.uniform())..'.jpg'
  )
  local result = {}
  if query_url then
    local wget_cmd = 'wget '..query_url..' -O '..filename.. ' -q'
    os.execute(wget_cmd)
    --print(wget_cmd)
    --[[
    async.curl.get(query_url, 
      function(res)
        local data = gm.Image():fromString(res) 
        input = data:toTensor('float', 'RGB', 'DHW')
      end
    )
    --]]
    print('Start predict:'..query_url..' '..filename)
    scores, classes, class_name = model.predict(image.load(filename))
    print('Start extract_feature:' .. query_url)
    feature = model.extract_feature(input, true)
    local table_scores = scores[{{1,5}}]:totable()
    local table_feature= feature:totable()
    result = {
      url = query_url,
      category = q_cate,
      name = class_name,
      score = table_scores,
      feature = table_feature,
      result = true} 

    for i=1,5 do
      print(class_name[i] .. ' ' .. table_scores[i])
    end
  else
    --app.abort(400, 'request error', req, res)
    result = {
      url = query_url,
      category = q_cate,
      name = nil,
      score = nil,
      feature = nil,
      result = false} 
  end
  res.json(result)
  os.execute('rm -f '..filename)
end)


local options = {}
options.host = '10.202.35.0'
options.port = '8080'
--app.repl({host='10.202.35.0', port='8081'})
app.listen(options)


