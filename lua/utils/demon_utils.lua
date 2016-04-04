
local gm = require 'graphicsmagick'
local demon_utils = {}

function demon_utils.download_image(query_url)
  local filename = paths.concat(
    --'/tmp/' .. tostring(torch.uniform())..'.jpg'
    '/storage/enroll/' .. tostring(torch.uniform())..'.jpg'
  )
  local wget_cmd = 'wget '..query_url..' -O '..filename.. ' -q'
  os.execute(wget_cmd)
  --print(wget_cmd)
  return filename
end


function demon_utils.load_image(image_filename)
  local info = gm.info(image_filename)
  local img
  --print(info.format)
  if info.format == 'JPEG' or info.format == 'PNG' then
    img = gm.load(image_filename)
    --local img = image.load(image_filename)
  end
  return img
end


function demon_utils.load_list(filename)
  assert(filename)
  local file = io.open(filename)
  local data_list = {}
  while true do
    local line = file:read()
    if not line then break end
    local url = string.gsub(line, "\n", "")
    table.insert(data_list, url)
  end
  file:close()
  return data_list
end

return demon_utils

