require 'cutorch'
require 'cunn'
require 'cudnn'
cudnn.fastest = true
cudnn.benchmark = true
cudnn.verbose = true
require 'image'
local gm = require 'graphicsmagick'
package.path = '/works/demon_11st/lua/?.lua'..package.path
local image_utils = require 'utils.image_utils'


local agent_filename = 
  --'/data2/product/det/torch_cache/inception6/det_stnThuDec318:29:322015/agent_29.bn_removed.t7'
  '/storage/product/det/torch_cache/inception6/det_stnThuDec318:29:322015/agent_29.bn_removed.t7'
local agent= torch.load(agent_filename)
print(agent)
agent.cuda()
agent.evaluate()
collectgarbage()

print '===> Loading mean, std' 
local mean_std = 
  torch.load(
    --'/data2/product/det/torch_cache/meanstdCache.t7'
    '/storage/product/det/torch_cache/meanstdCache.t7'
  )

print '===> Loading classes' 
local class_filename= 
  --'/data2/product/det/torch_cache/inception6/det_stnThuDec318:29:322015/classes.t7'
  '/storage/product/det/torch_cache/inception6/det_stnThuDec318:29:322015/classes.t7'
local cls_config = torch.load(class_filename)

local loadSize  = {3, 342, 342}
local sampleSize= {3, 299, 299}


function agent.preprocess(input)
  assert(input)
  local input0 = resize_crop(input, loadSize, 0)
  local input1 = resize_crop(input, loadSize, 1)
  input0= mean_std_norm(input0, mean_std.mean, mean_std.std)
  input1= mean_std_norm(input1, mean_std.mean, mean_std.std)
  input0= augment_image(input0,loadSize, sampleSize )
  input1= augment_image(input1,loadSize, sampleSize )
  local data = torch.FloatTensor(20, sampleSize[1], sampleSize[2], sampleSize[3])
  data[{{1 ,10},{},{},{}}] = input0
  data[{{11,20},{},{},{}}] = input1
  return data
end


function agent.predict(input)
  --print('agent.predict')
  local data = agent.preprocess(input)
  --print('preprocess')
  local scores,classes
  scores = agent.forward(data:cuda()):float()
  scores, classes = torch.mean(scores,1):view(-1):sort(true)
  local class_name = {}
  for i=1,5 do
    table.insert(class_name, cls_config[classes[i]])
  end
  return scores, classes, class_name
end


function agent.extract_feature(input, predicted)
  local output = torch.FloatTensor()
  local predicted = predicted or nil
  if not predicted then
    local data = preprocess(input)
    agent.forward(data:cuda())
  end
  output = agent.get(1).output:float():squeeze()
  output = output:view(output:nElement())
  --print(output:nElement())
  return output
end


print '===> Loading agent success'
return model

