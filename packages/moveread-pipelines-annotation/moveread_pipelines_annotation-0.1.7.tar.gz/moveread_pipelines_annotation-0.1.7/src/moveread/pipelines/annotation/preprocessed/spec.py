from typing import Sequence, TypedDict, TypeVar, Generic
from dataclasses import dataclass
from pipeteer import Wrapped, Workflow
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from haskellian import iter as I
from dslog import Logger
from dslog.uvicorn import setup_loggers_lifespan, ACCESS_FORMATTER, DEFAULT_FORMATTER
from moveread.core import Player
import robust_extraction2 as re
import moveread.pipelines.game_preprocess as gamepre
import moveread.pipelines.annotation as ann

T = TypeVar('T')

@dataclass
class Base(Generic[T]):
  pgn: Sequence[str]
  title: str
  imgs: Sequence[str]
  model: re.ExtendedModel
  state: T

@dataclass
class Input(Base[T], Generic[T]):
  annotate: bool = True

@dataclass
class Preprocessed(Base):
  preprocessed: gamepre.Output

@dataclass
class Output(Base[T], Generic[T]):
  preprocessed: gamepre.Output
  state: T
  annotations: Player.Meta | None = None

class Preprocess(Wrapped[Input, Preprocessed|Output, gamepre.Input, gamepre.Output, gamepre.GamePreprocess.Queues, gamepre.Params, gamepre.GamePreprocess.Artifacts]):
  def __init__(self):
    super().__init__(Input, gamepre.GamePreprocess())

  def pre(self, inp: Input):
    return gamepre.Input(imgs=inp.imgs, model=inp.model)
  
  def post(self, inp: Input, out: gamepre.Output):
    if inp.annotate:
      return Preprocessed(preprocessed=out, title=inp.title, pgn=inp.pgn, imgs=inp.imgs, model=inp.model, state=inp.state)
    else:
      return Output(annotations=None, preprocessed=out, title=inp.title, pgn=inp.pgn, imgs=inp.imgs, model=inp.model, state=inp.state)
  
  
class Annotate(Wrapped[Preprocessed, Output|Input, ann.Input, ann.Output, ann.Annotation.Queues, ann.Params, ann.Annotation.Artifacts]):
  def __init__(self):
    super().__init__(Preprocessed, ann.Annotation())

  def pre(self, inp: Preprocessed):
    boxes = I.flatmap(lambda x: x.boxes, inp.preprocessed).sync()
    return ann.Input(title=inp.title, boxes=boxes, pgn=inp.pgn)
  
  def post(self, inp: Preprocessed, out: ann.Output):
    if out.tag == 'ok':
      return Output(annotations=out.meta, preprocessed=inp.preprocessed, title=inp.title, pgn=inp.pgn, imgs=inp.imgs, model=inp.model, state=inp.state)
    else:
      imgs = [p.original.img for p in inp.preprocessed] # rotation
      return Input(title=inp.title, imgs=imgs, model=inp.model, pgn=inp.pgn, state=inp.state)

class Queues(TypedDict):
  preprocess: Wrapped.Queues[Input, gamepre.GamePreprocess.Queues]
  annotation: Wrapped.Queues[Preprocessed, ann.Annotation.Queues]

class Pipelines(TypedDict):
  preprocess: Preprocess
  annotation: Annotate


class PreprocessedAnnotation(Workflow[Input, Output, Queues, gamepre.Params, gamepre.GamePreprocess.Artifacts, Pipelines]): # type: ignore
  Input = Input
  Output = Output
  Queues = Queues
  Pipelines = Pipelines
  Params = gamepre.Params
  Artifacts = gamepre.GamePreprocess.Artifacts
  
  def __init__(self):
    super().__init__({
      'preprocess': Preprocess(),
      'annotation': Annotate()
    }, Tin=Input, Tout=Output)

  def run(self, queues: Queues, params: gamepre.Params) -> gamepre.GamePreprocess.Artifacts:

    logger = params.get('logger') or Logger.click().prefix('[PREPROC. ANNOTATION]')
    images = params['images']
    params['logger'] = logger.prefix('[PREPROCESS]')
    artifs = self.pipelines['preprocess'].run(queues['preprocess'], params)
    ann_params = ann.Params(logger=logger.prefix('[ANNOTATION]'), images=images)
    ann_api = self.pipelines['annotation'].run(queues['annotation'], ann_params)

    api = FastAPI(
      generate_unique_id_function=lambda route: route.name,
      lifespan=setup_loggers_lifespan(
        access=logger.format(ACCESS_FORMATTER),
        uvicorn=logger.format(DEFAULT_FORMATTER)
      )
    )
    api.mount('/preprocess', artifs.api)
    api.mount('/annotation', ann_api)

    artifs.api = api
    return artifs