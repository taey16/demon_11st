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
  -- attribute 18 
  '/storage/attribute/checkpoints/tshirts_shirts_blous_knit_jacket_onepiece_skirts_coat_cardigan_vest_pants_leggings_shoes_bags_swimwears_hat_panties_bra_801544_40000_seq_length14/resception_ep29_bs16_flipfalse_croptrue_original_init_gamma0.100000_lstm_tanh_hid512_lay2_drop2.000000e-01_adam_lr1.000000e-03_seed0.90_start541152_every45096_finetune0_cnnlr1.000000e-03_cnnwc1.000000e-05_retrain_iter0/model_idresception_ep29_bs16_flipfalse_croptrue_original_init_gamma0.100000_lstm_tanh_hid512_lay2_drop2.000000e-01_adam_lr1.000000e-03_seed0.90_start541152_every45096_finetune0_cnnlr1.000000e-03_cnnwc1.000000e-05_retrain_iter0.t7'
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
print(agent.cnn)
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
  local seq, seqLogprobs
  seq, seqLogprobs = agent.lm:sample(feats, sample_opts)
  local sents = net_utils.decode_sequence(vocab, seq)
  print(sents[1])  
  local words = string.split(sents[1], ' ')
  return sents, seqLogprobs:squeeze()[{{1,#words}}], feats
end


function agent.get_attribute(image_filename)
  local img = demon_utils.load_image(image_filename)
  local sentences, logprob, feature_vector
  if img then
    sentences, logprob, feature_vector = agent.predict(img)
  end
  if logprob then
    logprob = torch.exp(logprob):totable()
  end
  return sentences, logprob, feature_vector
end


agent.model_filename = agent_filename
agent.opts = opts
agent.sample_opts = sample_opts
agent.vocab = vocab

print '===> Loading agent_attribute success'
io.flush(print(string.format(
  '===> model file: %s', agent_filename
)))
return agent

