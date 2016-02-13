require 'torch'
require 'nn'
require 'nngraph'
require 'cutorch'
require 'cunn'
require 'cudnn'
require 'image'
package.path = '/works/vision_language/?.lua;'..package.path
require 'misc.DataLoaderRaw'
require 'models.LanguageModel'
require 'models.FeatExpander'
local net_utils = require 'misc.net_utils'

local agent_filename = 
  '/storage/attribute/checkpoints/tshirts_shirts_blous_87844_6000/_inception-v3-2015-12-05_bn_removed_epoch31_bs16_encode256_layer2_lr4.000000e-04/model_id_inception-v3-2015-12-05_bn_removed_epoch31_bs16_encode256_layer2_lr4.000000e-04.t7'
  --'/storage/attribute/checkpoints/tshirts_shirts/_inception-v3-2015-12-05_bn_removed_epoch16_bs16_embedding2048_encode128_layer3_lr4e-4/model_id_inception-v3-2015-12-05_bn_removed_epoch16_bs16_embedding2048_encode128_layer3_lr4e-4.t7'
  --'/storage/attribute/checkpoints/_inception-v3-2015-12-05_bn_removed_epoch10_mean_std_modified_bs16_embedding2048_encode256_layer2_lr4e-4/model_id_inception-v3-2015-12-05_bn_removed_epoch10_mean_std_modified_bs16_embedding2048_encode256_layer2_lr4e-4.t7'
print('===> Loading agent: '..agent_filename)
local checkpoint = torch.load(agent_filename)
local batch_size = checkpoint.opt.batch_size
local opt = {
  'rnn_size', 
  'input_encoding_size', 
  'drop_prob_lm', 
  'cnn_proto', 
  'cnn_agent', 
  'seq_per_img', 
  'image_size', 
  'crop_size'
}
for k,v in pairs(opt) do opt[v] = checkpoint.opt[v] end
local vocab = checkpoint.vocab
local beam_size = 1 
local sample_opts = { 
  sample_max = opt.sample_max, 
  beam_size = beam_size, 
  temperature = opt.temperature 
}

local agent = checkpoint.protos
agent.expander = nn.FeatExpander(opt.seq_per_img)
agent.lm:createClones()
for k,v in pairs(agent) do v:cuda() end
agent.cnn:evaluate()
agent.lm:evaluate()
collectgarbage()


function agent.preprocess(input)
  local img = 
    net_utils.preprocess_inception7_predict(input, opt.crop_size, false, 1)
  local data= 
    torch.CudaTensor(2, 3, opt.crop_size, opt.crop_size):fill(0)
  data[{{1},{},{},{}}] = img
  return data
end


function agent.predict(input)
  local input = image.scale(input, opt.image_size, opt.image_size)
  input = agent.preprocess(input)
  local feats = agent.cnn:forward(input)
  local seq = agent.lm:sample(feats, sample_opts)
  local sents = net_utils.decode_sequence(vocab, seq)
  return sents[1]
end


print '===> Loading agent_attribute success'
io.flush(print(string.format(
  '===> model file: %s', agent_filename
)))
return agent

