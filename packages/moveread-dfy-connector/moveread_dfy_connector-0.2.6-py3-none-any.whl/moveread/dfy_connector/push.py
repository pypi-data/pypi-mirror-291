from dataclasses import dataclass, field
import asyncio
from sqlmodel import Session
from sqlalchemy import Engine
from haskellian import either as E
from kv import KV
from pipeteer import ReadQueue
from dslog import Logger
import chess_pairings as cp
from moveread.core import Core
from moveread.dfy import PGN, queries
from moveread.pipelines import dfy

@dataclass
class Pusher:
  Qout: ReadQueue[dfy.Output]
  pipeline_blobs: KV[bytes]
  dfy_blobs: KV[bytes]
  dfy_engine: Engine
  core: Core
  logger: Logger = field(default_factory=lambda: Logger.click().prefix('[PUSHER]'))

  async def push_game(self, output: dfy.Output):
    gid = output.gameId
    key = cp.stringifyId(**gid)
    e = await dfy.core.output_one(self.core, key, output, blobs=self.pipeline_blobs)
    if e.tag == 'left':
      self.logger(f'Error pushing output for game {output.gameId}:', e.value, level='ERROR')
      return False

    with Session(self.dfy_engine) as ses:
      api = queries.API(ses)
      game = api.select.game(**gid)
      if game is None:
        self.logger(f'Game not found: {gid}', level='ERROR')
        return False
      
      if game.pgn:
        ses.delete(game.pgn)
        ses.commit()

      game.pgn = PGN(moves=output.pgn, early=output.early)
      game.status = 'done'
      ses.add(game)
      ses.commit()
      self.logger(f'Pushed game: {gid}')
      return True
  
  @E.do()
  async def push_one(self):
    id, output = (await self.Qout.read()).unsafe()
    self.logger(f'Pushing "{id}"')
    r = await self.push_game(output)
    if r:
      (await self.Qout.pop(id)).unsafe()
      self.logger(f'Popped "{id}"')
      (await self.pipeline_blobs.prefix(id).clear()).unsafe()
      self.logger(f'Cleaned blobs of "{id}"')

  async def loop(self):
    while True:
      try:
        r = await self.push_one()
        if r.tag == 'left':
          self.logger('Error pushing:', r.value, level='ERROR')
          await asyncio.sleep(5)
      except Exception as e:
        self.logger('Unexpected exception:', e, level='ERROR')
        await asyncio.sleep(5)
