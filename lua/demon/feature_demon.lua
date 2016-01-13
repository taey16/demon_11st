
local app  = require('../waffle') {
  autocache = true
}
local async= require 'async'
--local gm = require 'graphicsmagick'
local model = paths.dofile('../agent/agent.lua')
local model_gc = paths.dofile('../agent/agent_gc.lua')
local model_caption = paths.dofile('../agent/agent_caption.lua')
local downloader = paths.dofile('../utils/demon_utils.lua')
require 'image'


app.get("/lua_wrapper_request_handler", function(req, res)
  local query_url = req.url.args.url or nil
  local result = {}
  if query_url then
    local filename = downloader.download_image(query_url)
    print('Start predict:')
    local img = image.load(filename)
    scores, classes, class_name = model.predict(img)
    print('Start extract_feature:')
    feature = model.extract_feature(input, true)
    local table_scores = scores[{{1,5}}]:totable()
    local table_feature= feature:totable()

    print('Start predict:')
    scores_gc, classes_gc, class_name_gc = model_gc.predict(img)
    print('Start extract_feature:')
    feature_gc = model_gc.extract_feature(input, true)
    local table_scores_gc = scores_gc[{{1,5}}]:totable()
    local table_feature_gc= feature_gc:totable()
    print('Start caption:')
    local sentence = model_caption.predict(img)

    result = {
      url = query_url,
      category = class_name,
      score = table_scores,
      feature = table_feature,
      category_gc = class_name_gc,
      score_gc = table_scores_gc,
      feature_gc = table_feature_gc,
      sentence = sentence,
      result = true
    }

    for i=1,5 do
      print(class_name[i] .. ' ' .. table_scores[i])
    end
    io.flush(print(sentence))
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
options.host = '10.202.4.219'
options.port = '8080'
app.listen(options)


