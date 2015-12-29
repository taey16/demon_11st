
local app  = require('../waffle') {
  autocache = true
}
local async= require 'async'
--local gm = require 'graphicsmagick'
local model = paths.dofile('../agent/agent.lua')
local model_gc = paths.dofile('../agent/agent_gc.lua')
require 'image'

app.get("/lua_wrapper_request_handler", function(req, res)
  local query_url = req.url.args.url or nil
  local filename = paths.concat(
    '/tmp/' .. tostring(torch.uniform())..'.jpg'
  )
  local result = {}
  if query_url then
    local wget_cmd = 'wget '..query_url..' -O '..filename.. ' -q'
    os.execute(wget_cmd)
    print('Start predict:'..query_url..' '..filename)
    local img = image.load(filename)
    scores, classes, class_name = model.predict(img)
    print('Start extract_feature:' .. query_url)
    feature = model.extract_feature(input, true)
    local table_scores = scores[{{1,5}}]:totable()
    local table_feature= feature:totable()

    print('Start predict:'..query_url..' '..filename)
    scores_gc, classes_gc, class_name_gc = model_gc.predict(img)
    print('Start extract_feature:' .. query_url)
    feature_gc = model_gc.extract_feature(input, true)
    local table_scores_gc = scores_gc[{{1,5}}]:totable()
    local table_feature_gc= feature_gc:totable()
    result = {
      url = query_url,
      category = class_name,
      score = table_scores,
      feature = table_feature,
      category_gc = class_name_gc,
      score_gc = table_scores_gc,
      feature_gc = table_feature_gc,
      result = true} 

    for i=1,5 do
      print(class_name[i] .. ' ' .. table_scores[i])
    end
  else
    --app.abort(400, 'request error', req, res)
    result = {
      url = query_url,
      category = nil,
      name = nil,
      score = nil,
      feature = nil,
      result = false} 
  end
  res.json(result)
  os.execute('rm -f '..filename)
end)


local options = {}
options.host = '10.202.35.109'
options.port = '8080'
app.listen(options)


