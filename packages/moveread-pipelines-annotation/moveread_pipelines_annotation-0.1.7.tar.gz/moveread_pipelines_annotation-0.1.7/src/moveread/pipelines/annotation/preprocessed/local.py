from typing import Sequence, TypeVar
import os
from pipeteer import QueueKV
from kv import FilesystemKV, SQLiteKV
import moveread.pipelines.preprocess as pre
from moveread.pipelines.game_preprocess import StorageParams, Game

T = TypeVar('T')

def queue_factory(db_path: str):
  def get_queue(path: Sequence[str|int], type: type[T]) -> QueueKV[T]:
    return QueueKV.sqlite(type, db_path, '-'.join(str(p) for p in (path or ['Qin'])))
  return get_queue

def local_storage(
  base_path: str, *,
  db_relpath: str = 'data.sqlite',
  images_relpath: str = 'images',
  images_url: str,
) -> StorageParams:
  """Scaffold local storage for the DFY pipeline."""

  db_path = os.path.join(base_path, db_relpath)
  images_path = os.path.join(base_path, images_relpath)
  os.makedirs(images_path, exist_ok=True)
  return StorageParams(
    images=FilesystemKV[bytes](images_path).served(images_url),
    games=SQLiteKV.at(db_path, Game, table='games'),
    imgGameIds=SQLiteKV[str].at(db_path, str, table='game-ids'),
    buffer=SQLiteKV.at(db_path, dict[str, pre.Output], table='received-imgs'),
  )