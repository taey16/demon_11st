require 'torch'
require 'nn'
require 'nngraph'
require 'cutorch'
require 'cunn'
require 'cudnn'
--local cjson = require 'cjson'
require 'image'
package.path = '/works/nt2/?.lua;'..package.path
require 'misc.DataLoaderRaw'
require 'models.LanguageModel'
local net_utils = require 'misc.net_utils'

local model_filename = 
  '/storage/coco/checkpoints/_ReCept_bn_removed_epoch35_bs16_embedding2048_encode384_layer2_lr4e-4/model_id_ReCept_bn_removed_epoch35_bs16_embedding2048_encode384_layer2_lr4e-4.t7'
  --'/storage/coco/checkpoints/_inception7_bs16_encode256_layer2/model_id_inception7_bs16_encode256_layer2.t7'
print('===> Loading model: '..model_filename)
local checkpoint = torch.load(model_filename)
local batch_size = checkpoint.opt.batch_size
local opt = {
  'rnn_size', 
  'input_encoding_size', 
  'drop_prob_lm', 
  'cnn_proto', 
  'cnn_model', 
  'seq_per_img', 
  'image_size', 
  'crop_size'
}
for k,v in pairs(opt) do 
  opt[v] = checkpoint.opt[v]
end
local vocab = checkpoint.vocab
local beam_size = 4
local sample_opts = { 
  sample_max = opt.sample_max, 
  beam_size = beam_size, 
  temperature = opt.temperature 
}

local model = checkpoint.protos
model.expander = nn.FeatExpander(opt.seq_per_img)
model.lm:createClones()
for k,v in pairs(model) do v:cuda() end
model.cnn:evaluate()
model.lm:evaluate()
collectgarbage()


function model.preprocess(input)
  local img = 
    net_utils.preprocess_inception7_predict(input, opt.crop_size, false, 1)
  local data= 
    torch.CudaTensor(2, 3, opt.crop_size, opt.crop_size):fill(0)
  data[{{1},{},{},{}}] = img
  return data
end


function model.predict(input)
  local input = image.scale(input, 292, 292)
  input = model.preprocess(input)
  local feats = model.cnn:forward(input)
  local seq = model.lm:sample(feats, sample_opts)
  local sents = net_utils.decode_sequence(vocab, seq)
  return sents[1]
end


print '===> Loading agent_caption success'
return model

