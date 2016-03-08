require 'torch'
require 'nn'
require 'nngraph'
require 'cutorch'
require 'cunn'
require 'cudnn'
cudnn.fastest = true
cudnn.benchmark = true
cudnn.verbose = true
require 'image'
package.path = '/works/vision_language/?.lua;'..package.path
require 'misc.DataLoaderRaw'
require 'models.LanguageModel'
require 'models.FeatExpander'
local net_utils = require 'misc.net_utils'
local demon_utils = require '../utils/demon_utils'

local agent_filename = 
  '/storage/attribute/checkpoints/tshirts_shirts_blous_knit_103607_8000_seq_length-1/_resception_bn_removed_epoch19_bs16_flipfalse_croptrue_lstm_tanh_hidden256_layer2_dropout0.5_lr4.000000e-04_anneal_seed0.50_start50000_every25000_finetune-1_cnnlr4.000000e-04/model_id_resception_bn_removed_epoch19_bs16_flipfalse_croptrue_lstm_tanh_hidden256_layer2_dropout0.5_lr4.000000e-04_anneal_seed0.50_start50000_every25000_finetune-1_cnnlr4.000000e-04.t7'
  --'/storage/attribute/checkpoints/tshirts_shirts_blous_knit_103607_8000/_inception-v3-2015-12-05_bn_removed_epoch33_bs16_lstm_tanh_hidden256_layer2_dropout0.5_lr4.000000e-04_anneal_100000/model_id_inception-v3-2015-12-05_bn_removed_epoch33_bs16_lstm_tanh_hidden256_layer2_dropout0.5_lr4.000000e-04_anneal_100000.t7'
  --'/storage/attribute/checkpoints/tshirts_shirts_blous_knit_103607_8000/_inception-v3-2015-12-05_bn_removed_epoch33_bs16_encode256_layer2_dropout5e-1_lr4.000000e-04/model_id_inception-v3-2015-12-05_bn_removed_epoch33_bs16_encode256_layer2_dropout5e-1_lr4.000000e-04.t7'
  --'/storage/attribute/checkpoints/tshirts_shirts_blous_87844_6000/_inception-v3-2015-12-05_bn_removed_epoch31_bs16_encode256_layer2_lr4.000000e-04/model_id_inception-v3-2015-12-05_bn_removed_epoch31_bs16_encode256_layer2_lr4.000000e-04.t7'
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
local beam_size = 10
local sample_opts = { 
  -- do sampleing from argmzx (1)
  -- or multinomial sampling (0)
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
  local img = image.scale(input, opt.image_size, opt.image_size)
  img = net_utils.preprocess_for_predict(img, opt.crop_size)
  local data= 
    torch.CudaTensor(1, 3, opt.crop_size, opt.crop_size):fill(0)
  data[{{1},{},{},{}}] = img
  return data
end


function agent.predict(input_tensor)
  local input = agent.preprocess(input_tensor)
  local feats = agent.cnn:forward(input)
  if feats:dim() == 1 then
    feats = feats:resize(1, (#feats)[1])
  end
  local seq = agent.lm:sample(feats, sample_opts)
  local sents = net_utils.decode_sequence(vocab, seq)
  return sents
end


function agent.get_attribute(image_filename)
  local img = demon_utils.load_image(image_filename)
  local sentences
  if img then
    sentences = agent.predict(img)
  end
  return sentences
end


agent.model_filename = agent_filename
agent.opts = opts
agent.sample_opts = sample_opts

print '===> Loading agent_attribute success'
io.flush(print(string.format(
  '===> model file: %s', agent_filename
)))
return agent

