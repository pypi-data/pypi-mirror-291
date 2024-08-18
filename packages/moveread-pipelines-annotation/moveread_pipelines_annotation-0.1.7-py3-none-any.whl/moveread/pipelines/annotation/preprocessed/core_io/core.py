from typing_extensions import TypedDict, NamedTuple, Sequence, Any, NotRequired
from uuid import uuid4
from haskellian import Either, Left, Right, either as E
from kv import KV
from pipeteer import ReadQueue, WriteQueue
import chess_pairings as cp
from moveread.core import Core, Game, Player, Image
from moveread.pipelines.annotation.preprocessed import Input, Output

class PlayerId(TypedDict):
  id: str
  player: int

class State(TypedDict):
  playerId: PlayerId
  meta: NotRequired[Player.Meta | None]

def unpack(id: str, player: int):
  return id, player

class NewInput(NamedTuple):
  uuid: str
  input: Input[State]
  from_urls: Sequence[str]
  to_urls: Sequence[str]

def new_input(
  player: Player, playerId: PlayerId, *,
  pgn: Sequence[str], model: str, meta: Player.Meta | None = None
) -> NewInput:

  id, player_idx = unpack(**playerId)
  state = State(playerId=playerId, meta=meta)
  uuid = f'{id}/{player_idx}-{uuid4()}'

  empty_sheets = [s for s in player.sheets if len(s.images) == 0]
  assert len(empty_sheets) == 0, f'Empty sheets for player {player_idx} in "{id}"'
  
  from_urls = [sheet.images[0].url for sheet in player.sheets]
  to_urls = [f'{uuid}-{j}.jpg' for j in range(len(from_urls))]
  inp = Input(pgn=pgn, model=model, state=state, imgs=to_urls, title=f'{id}/{player_idx}', annotate=state.get('meta') is None)
  return NewInput(uuid=uuid, input=inp, from_urls=from_urls, to_urls=to_urls)

# def new_inputs(id: str, game: Game, *, model: str) -> list[Either[Any, NewInput]]:
#   if not (pgn := game.meta.pgn):
#     return [Left(f'No PGN for "{id}"')]
#   if not (gameId := game.meta.tournament):
#     return [Left(f'No tournament annotation for "{id}"')]
  
#   gid = cp.stringifyId(**gameId)
#   uuid = f'{gid}-{uuid4()}'
#   inputs = []
#   for i, player in enumerate(game.players):

#     empty_sheets = [s for s in player.sheets if len(s.images) == 0]
#     if empty_sheets:
#       inputs.append(Left(f'Empty sheets for player {i} in "{id}"'))
#       continue

#     from_urls = [sheet.images[0].url for sheet in player.sheets]
#     to_urls = [f'{uuid}/{i}-{j}.jpg' for j in range(len(from_urls))]
#     playerId = f'{gid}/{i}'
#     state = State(playerId=PlayerId(id=id, player=i), meta=nondefault_meta(player.meta))
#     inp = Input(pgn=pgn, model=model, state=state, imgs=to_urls, title=playerId, annotate=state.get('meta') is None)
#     inputs.append(Right(NewInput(uuid=f'{uuid}/{i}', input=inp, from_urls=from_urls, to_urls=to_urls)))

#   return inputs

@E.do()
async def input(input: NewInput, core: Core, Qin: WriteQueue[Input], blobs: KV[bytes]):
  for from_, to in zip(input.from_urls, input.to_urls):
    (await core.blobs.copy(from_, blobs, to)).unsafe()
  (await Qin.push(input.uuid, input.input)).unsafe()

# async def input_all(core: Core, Qin: WriteQueue[Input], blobs: KV[bytes], *, model: str, max_games: int | None = None):

#   games = await core.games.items().enumerate().sync()
#   for i, either in games:
#     if either.tag == 'left':
#       print('\nError reading game:', either.value)
#       continue

#     id, game = either.value
#     print(f'\r{i+1}/{len(games)}: {id}', end='', flush=True)
#     for x in new_inputs(id, game, model=model):
#       if x.tag == 'left':
#         print('\nInput error:', x.value)
#         continue
      
#       for from_, to in zip(x.value.from_urls, x.value.to_urls):
#         (await core.blobs.copy(from_, blobs, to)).unsafe()
#       (await Qin.push(x.value.uuid, x.value.input)).unsafe()


class NewOutput(NamedTuple):
  game: Game
  from_urls: Sequence[str]
  to_urls: Sequence[str]
  delete_urls: Sequence[str]

def parse_output(out: Output[State], game: Game, *, preserve_images: bool = True) -> NewOutput:
  game = game.model_copy()
  player = game.players[out.state['playerId']['player']]
  if out.annotations:
    player.meta = out.annotations
  from_urls = []
  to_urls = []
  delete_urls = []

  for sheet, preproc in zip(player.sheets, out.preprocessed):
    corr = preproc.corrected
    if preserve_images:
      from_urls.append(corr.img)
      to_urls.append(corr.img)
      sheet.images.append(Image(url=corr.img, meta=corr.meta))
    else:
      og = preproc.original
      from_urls.extend([og.img, corr.img])
      to_urls.extend([og.img, corr.img])
      delete_urls = [img.url for img in sheet.images]
      sheet.images = [
        Image(url=corr.img, meta=corr.meta),
        Image(url=og.img, meta=og.meta)
      ]

  return NewOutput(game=game, from_urls=from_urls, to_urls=to_urls, delete_urls=delete_urls)

@E.do()
async def output_one(
  core: Core, Qout: ReadQueue[Output[State]], blobs: KV[bytes],
  *, preserve_images: bool = True
):
  """`preserve_images`: wheter to append to the player's images. If false, overrides them."""
  uuid, out = (await Qout.read()).unsafe()
  id = out.state['playerId']['id']
  game = (await core.games.read(id)).unsafe()
  new_game, from_urls, to_urls, delete_urls = parse_output(out, game, preserve_images=preserve_images)
  for from_, to in zip(from_urls, to_urls):
    (await blobs.copy(from_, core.blobs, to)).unsafe()
  (await core.games.insert(id, new_game)).unsafe()
  (await Qout.pop(uuid)).unsafe()
  for url in delete_urls:
    (await core.blobs.delete(url)).unsafe()
  return new_game, out.state['playerId']['player']