
require 'cutorch'
require 'cunn'
require 'cudnn'
paths.dofile('../utils/image_utils.lua')

local model = {}
local gpu_id = 1

print('===> setDevice:' .. gpu_id)
cutorch.setDevice(gpu_id)

print '===> Loading model'
local model_filename = 
  --'/data2/product/det/torch_cache/inception6/det_stnThuDec318:29:322015/model_29.bn_removed.t7'
  '/storage/product/det/torch_cache/inception6/det_stnThuDec318:29:322015/model_29.bn_removed.t7'
local model = torch.load(model_filename)
--[[
model:get(2).modules[#model:get(2).modules] = nil
model:get(2):add(cudnn.SoftMax())
--]]
print(model)
model:cuda()
model:evaluate()
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

local loadSize  = {3, 256, 256}
local sampleSize= {3, 224, 224}


function model.preprocess(input)
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


function model.predict(input)
  --print('model.predict')
  local data = model.preprocess(input)
  --print('preprocess')
  local scores,classes
  scores = model:forward(data:cuda()):float()
  scores, classes = torch.mean(scores,1):view(-1):sort(true)
  local class_name = {}
  for i=1,5 do
    table.insert(class_name, cls_config[classes[i]])
  end
  return scores, classes, class_name
end


function model.extract_feature(input, predicted)
  local output = torch.FloatTensor()
  local predicted = predicted or nil
  if not predicted then
    local data = preprocess(input)
    model:forward(data:cuda())
  end
  output = model:get(1).output:float():squeeze()
  output = output:view(output:nElement())
  --print(output:nElement())
  return output
end


print '===> Loading agent success'
return model

