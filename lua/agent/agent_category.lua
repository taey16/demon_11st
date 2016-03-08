
require 'cutorch'
require 'cunn'
require 'cudnn'
cudnn.fastest = true
cudnn.benchmark = true
cudnn.verbose = true
local image_utils = require '../utils/image_utils'
local demon_utils = require '../utils/demon_utils'


print '===> Loading agent'
local agent_filename = 
  '/storage/product/det/torch_cache/det_X_gpu2_resception_epoch1_nag_lr0.01125_decay_seed0.500_start37040_every37040/model_15.t7.bn_removed.t7'
local agent = torch.load(agent_filename)
print(agent)
agent:cuda()
agent:evaluate()
collectgarbage()

print '===> Loading mean, std' 
local mean_std = torch.load(
  '/storage/product/det/torch_cache/meanstdCache.t7'
)

print '===> Loading classes' 
local class_filename= 
  ''
  --'/storage/product/det/torch_cache/det_X_gpu2_resception_epoch1_nag_lr0.01125_decay_seed0.500_start37040_every37040/classes.t7'
--local cls_config = torch.load(class_filename)
local cls_config = {'blouse', 'cardigan', 'coat', 'hats', 'jacket', 'jumper', 'neat', 'onepiece', 'pants', 'shirt', 'shoes', 'skirt', 'swimwear', 'T-shirt', 'underwear'}

local loadSize  = {3, 342, 342}
local sampleSize= {3, 299, 299}


function agent.preprocess(input_tensor)
  assert(input)
  local input0 = image_utils.resize_crop(input_tensor, loadSize, 0)
  --local input1 = resize_crop(input, loadSize, 1)
  input0= image_utils.mean_std_norm(input0, mean_std.mean, mean_std.std)
  --input1= mean_std_norm(input1, mean_std.mean, mean_std.std)
  input0= image_utils.augment_image(input0,loadSize, sampleSize )
  --input1= augment_image(input1,loadSize, sampleSize )
  local data = torch.FloatTensor(10, sampleSize[1], sampleSize[2], sampleSize[3])
  --local data = torch.FloatTensor(20, sampleSize[1], sampleSize[2], sampleSize[3])
  data[{{1 ,10},{},{},{}}] = input0
  --data[{{11,20},{},{},{}}] = input1
  return data
end


function agent.predict(input_tensor)
  local data = agent.preprocess(input_tensor)
  local scores,classes
  scores = agent:forward(data:cuda()):float()
  scores, classes = torch.mean(scores,1):view(-1):sort(true)
  local class_name, scores_table = {}, {}
  for i=1,5 do
    table.insert(class_name, cls_config[classes[i]])
    table.insert(scores_table, scores[i])
  end
  return scores_table, classes, class_name
end


function agent.get_category(image_filename)
  local img
  img = demon_utils.load_image(image_filename)
  local scores, classes, class_name
  if img then
    scores, classes, class_name = agent.predict(img)
  end
  return scores, classes, class_name
end


function agent.extract_feature(input, predicted)
  local output = torch.FloatTensor()
  local predicted = predicted or nil
  if not predicted then
    local data = preprocess(input)
    agent:forward(data:cuda())
  end
  output = agent:get(1).output:float():squeeze()
  output = output:view(output:nElement())
  return output
end


print '===> Loading agent success'
return agent

