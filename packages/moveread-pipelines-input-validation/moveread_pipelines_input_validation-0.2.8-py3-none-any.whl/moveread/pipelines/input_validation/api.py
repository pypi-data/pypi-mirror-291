from dataclasses import dataclass
from fastapi import FastAPI, Request, Response, status
from haskellian import either as E
from kv import LocatableKV
from pipeteer.queues import ReadQueue, WriteQueue, ReadError
from dslog import Logger
from dslog.uvicorn import setup_loggers_lifespan, DEFAULT_FORMATTER, ACCESS_FORMATTER
from ._types import Input, Item, Result, Output

@dataclass
class SDK:
  Qin: ReadQueue[Input]
  Qout: WriteQueue[Output]
  images: LocatableKV[bytes]

  def tasks(self):
    return self.Qin.items().map(lambda e: e.fmap(Item.of(self.images)))
  
  @E.do[ReadError]()
  async def validate(self, taskId: str, out: Output):
    (await self.Qin.read(taskId)).unsafe()
    (await self.Qout.push(taskId, out)).unsafe()
    (await self.Qin.pop(taskId)).unsafe()

def fastapi(
  sdk: SDK, *, logger = Logger.click().prefix('[INPUT VALIDATION]')
):

  app = FastAPI(
    generate_unique_id_function=lambda route: route.name,
    lifespan=setup_loggers_lifespan(
      access=logger.format(ACCESS_FORMATTER),
      uvicorn=logger.format(DEFAULT_FORMATTER),
    )
  )

  @app.get('/tasks')
  async def get_tasks(req: Request) -> list[Item]:
    tasks = await sdk.tasks().sync()
    errs = list(E.filter_lefts(tasks))
    if errs != []:
      logger('Errors reading tasks:', *errs, level='ERROR')
    return list(E.filter(tasks))

  @app.post('/validate')
  async def validate(id: str, result: Result, res: Response):
    r = await sdk.validate(id, Output.of(result))
    if r.tag == 'left':
      logger(f'Error validating out for task "{id}":', r.value, level='ERROR')
      if r.value.reason == 'inexistent-item':
        res.status_code = status.HTTP_404_NOT_FOUND
      else:
        res.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

  return app