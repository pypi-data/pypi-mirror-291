from typing_extensions import TypedDict
from functools import partial
import asyncio
from haskellian import either as E, funcs as F
from pipeteer import GetQueue, Task, WriteQueue
from kv import LocatableKV, KV
from fastapi import FastAPI
from dslog import Logger
import pure_cv as vc
from ._types import Input, Output
from .api import fastapi, SDK

class Params(TypedDict):
  images: LocatableKV
  logger: Logger
  descaled_h: int

def descaled_path(img: str):
  name, _ = img.split('.')
  return f'{name}_rescaled.jpg'

def unrescale_path(img: str):
  name, ext = img.split('.')
  return name.removesuffix('_rescaled') + '.' + ext

def descale_img(img: bytes, descaled_h: int):
  return F.pipe(img, vc.decode, vc.descale_max(target_max=descaled_h), vc.encode(format='.jpg'))

@E.do()
async def pre(input: Input, *, images: KV[bytes], descaled_h: int) -> Input:
  """Descale the images and pass them as inputs"""
  tasks = [images.read(img) for img in input.imgs]
  imgs = E.sequence(await asyncio.gather(*tasks)).unsafe()

  rescaled_urls = [descaled_path(img) for img in input.imgs]
  descaled_imgs = [descale_img(img, descaled_h) for img in imgs]
  tasks = [images.insert(url, img) for url, img in zip(rescaled_urls, descaled_imgs)]
  E.sequence(await asyncio.gather(*tasks)).unsafe()
  return Input(gameId=input.gameId, imgs=rescaled_urls, tournId=input.tournId)
  
def post(output: Output) -> Output:
  """Adjust the output URLs to the original images"""
  return Output(gameId=output.gameId, imgs=[unrescale_path(img) for img in output.imgs])

class InputValidation(Task[Input, Output, Params, FastAPI]):
  Input = Input
  Output = Output
  Queues = Task.Queues[Input, Output]
  Params = Params
  Artifacts = FastAPI

  def __init__(self):
    super().__init__(Input, Output)

  def push_queue(self, get_queue: GetQueue, params: Params, /, *, prefix: tuple[str | int, ...] = ()) -> WriteQueue[Input]:
    return get_queue(prefix, self.Tin).safe_apremap(partial(pre, images=params['images'], descaled_h=params['descaled_h']))

  def run(self, queues: Queues, params: Params) -> FastAPI:
    Qin, Qout = queues['Qin'], queues['Qout']
    sdk = SDK(Qin, Qout.premap(post), images=params['images'])
    return fastapi(sdk, logger=params['logger'])