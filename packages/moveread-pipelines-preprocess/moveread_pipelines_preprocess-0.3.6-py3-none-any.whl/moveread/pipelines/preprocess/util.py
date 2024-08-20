from haskellian import either as E
from kv import KV, ReadError
import pure_cv as vc

@E.do[ReadError]()
async def insert_rescaled(url: str, images: KV[bytes], descaled_h: int):
  img = (await images.read(url)).unsafe()
  img = vc.decode(img)
  img = vc.descale_h(img, descaled_h)
  img = vc.encode(img, '.jpg')
  name = url.split('.')[0]
  rescaled_url = f'{name}-rescaled{descaled_h}.jpg'
  (await images.insert(rescaled_url, img)).unsafe()
  return rescaled_url