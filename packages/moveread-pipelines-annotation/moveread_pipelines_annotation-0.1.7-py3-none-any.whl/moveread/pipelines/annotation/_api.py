from haskellian import either as E
from kv import LocatableKV
from fastapi import FastAPI, Request, Response
from dslog import Logger
from dslog.uvicorn import setup_loggers_lifespan, ACCESS_FORMATTER, DEFAULT_FORMATTER
from .sdk import AnnotationSDK
from .spec import Item, Output


def api(
  sdk: AnnotationSDK, *,
  images: LocatableKV[bytes],
  logger: Logger = Logger.click().prefix('[ANNOTATION API]')
):

  app = FastAPI(
    generate_unique_id_function=lambda route: route.name,
    lifespan=setup_loggers_lifespan(
      access=logger.format(ACCESS_FORMATTER),
      uvicorn=logger.format(DEFAULT_FORMATTER)
    )
  )

  @app.get('/items')
  async def items(req: Request) -> list[Item]:
    eithers = await sdk.items().map(lambda e: e.fmap(Item.at(images))).sync()
    errs = list(E.filter_lefts(eithers))
    if errs != []:
      logger('Errors reading tasks:', *errs, level='ERROR')
    return list(E.filter(eithers))
  

  @app.post('/annotate')
  async def annotate(id: str, ann: Output, res: Response) -> bool:
    x = await sdk.annotate(id, ann)
    ok = x.tag == 'right'
    if not ok:
      logger(f'Error correcting item {id}', x.value, level='ERROR')
      res.status_code = 404 if x.value.reason == 'inexistent-item' else 500
    return ok
  
  return app