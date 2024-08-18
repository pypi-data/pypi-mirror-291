from dataclasses import dataclass
from haskellian import either as E
from pipeteer.queues import ReadQueue, WriteQueue, ReadError
from .spec import Input, Output

@dataclass
class AnnotationSDK:
  Qin: ReadQueue[Input]
  Qout: WriteQueue[Output]

  def items(self):
    return self.Qin.items()
  
  @E.do[ReadError]()
  async def annotate(self, id: str, ann: Output):
    (await self.Qin.read(id)).unsafe()
    (await self.Qout.push(id, ann)).unsafe()
    (await self.Qin.pop(id)).unsafe()