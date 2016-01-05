
local downloader = {}

function downloader.download_image(query_url)
  local filename = paths.concat(
    '/tmp/' .. tostring(torch.uniform())..'.jpg'
  )
  local wget_cmd = 'wget '..query_url..' -O '..filename.. ' -q'
  os.execute(wget_cmd)
  print(wget_cmd)
  return filename
end

return downloader

