from typing import Callable, TypeVar
from uuid import uuid4
from haskellian import either as E
from kv import KV
from dslog import Logger
from pipeteer import WriteQueue
from moveread.core import Core, Game
from moveread.pipelines.input_validation import Input, GameId

def gameId(game: Game) -> GameId:
  if game.meta is None or game.meta.tournament is None:
    return GameId(group='a', round='1', board='1')
  return game.meta.tournament

S = TypeVar('S')

async def input_core(
  core: Core, Qin: WriteQueue[Input],
  *, images: KV[bytes], tournId: str,
  gameId_fn: Callable[[Game], GameId] = gameId,
  num_games: int | None = None, shuffle: bool = True,
  logger = Logger.rich().prefix('[CORE INPUT]')
):
  """Input all images from `core` into `Qin` tasks
  - Actually, only images with `version == 0`
  - `model_fn`: determines the scoresheet model of each task
  - `state_fn`: determines an arbitrary tuple of JSON-serializable data to attach to each task
  """
  games = await core.games.keys().map(E.unsafe).sync()
  if shuffle:
    import random
    random.shuffle(games)
  for gameId in games[:num_games]:
    game = (await core.games.read(gameId)).unsafe()
    imgs = []
    for imgId, image in game.images:
      id = '/'.join([gameId, *map(str, imgId)])
      url = f'{id}/original_{uuid4()}.jpg'
      img = (await core.blobs.read(image.url)).unsafe()
      (await images.insert(url, img)).unsafe()
      imgs.append(url)
      break

    task = Input(gameId=gameId_fn(game), imgs=imgs, tournId=tournId)
    await Qin.push(gameId, task)
    logger(f'Inputted task "{gameId}". Task:', task)