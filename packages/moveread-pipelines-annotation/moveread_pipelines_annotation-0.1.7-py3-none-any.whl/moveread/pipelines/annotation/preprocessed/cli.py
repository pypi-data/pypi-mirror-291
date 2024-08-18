from argparse import ArgumentParser

def main():

  parser = ArgumentParser()
  parser.add_argument('-b', '--base-path', required=True)
  parser.add_argument('--token', default='secret')
  parser.add_argument('--url')
  parser.add_argument('--no-autocorrect', action='store_true')

  parser.add_argument('-p', '--port', type=int, default=8000)
  parser.add_argument('--host', default='0.0.0.0')
  parser.add_argument('--cors', default=['*'], nargs='*', type=str, help='CORS allowed origins')

  args = parser.parse_args()

  import os
  from dslog import Logger

  base_path = os.path.abspath(args.base_path)
  logger = Logger.click().prefix('[ANNOTATION]')
  logger(f'Running annotation pipeline at "{base_path}"...')

  import asyncio
  from multiprocessing import Process
  from pipeteer import http
  from kv import ServerKV
  from fastapi import Request, Response
  import uvicorn
  from fastapi.middleware.cors import CORSMiddleware
  from moveread.pipelines.annotation.preprocessed import PreprocessedAnnotation, local_storage, queue_factory

  pipe = PreprocessedAnnotation()

  queues_path = os.path.join(base_path, 'queues.sqlite')
  get_queue = queue_factory(queues_path)
  storage = local_storage(base_path, images_url=args.url.rstrip('/') + '/images')
  params = PreprocessedAnnotation.Params(logger=logger, **storage)

  Qout = get_queue(('output',), PreprocessedAnnotation.Output)
  Qs = pipe.connect(Qout, get_queue, params)

  artifs = pipe.run(Qs, params)
  artifs.api.mount('/queues', http.mount(pipe, Qout, get_queue, params))
  artifs.api.mount('/images', ServerKV(storage['images']))

  artifs.api.add_middleware(CORSMiddleware, allow_origins=args.cors, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
  @artifs.api.middleware('http')
  async def auth_middleware(request: Request, call_next):
    images_path = request.url.path.startswith('/images/') and not '..' in request.url.path # could that hack work? let's just be safe
    if images_path or request.method == 'OPTIONS':
      return await call_next(request) 

    auth = request.headers.get('Authorization')
    if not auth or len(parts := auth.split(' ')) != 2 or parts[0] != 'Bearer':
      logger(f'Bad authorization:', auth, level='DEBUG')
      return Response(status_code=401)
    if parts[1] != args.token:
      logger(f'Bad token: "{parts[1]}"', level='DEBUG')
      return Response(status_code=401) 

    return await call_next(request)

  ps = {
    id: Process(target=asyncio.run, args=(f,))
    for id, f in artifs.processes.items()
  } | {
    'api': Process(target=uvicorn.run, args=(artifs.api,), kwargs={'host': args.host, 'port': args.port})
  }
  for id, p in ps.items():
    p.start()
    logger(f'Process "{id}" started at PID {p.pid}')
  for p in ps.values():
    p.join()


if __name__ == '__main__':
  # import debugpy
  # debugpy.listen(("0.0.0.0", 5678))
  # print("Waiting for debugger attach...")
  # debugpy.wait_for_client()
  # print("Debugger attached")

  import os
  import sys

  os.chdir('/home/m4rs/mr-github/rnd/annotation/annotation/dev/full-demo')
  sys.argv.extend(['-b', '.'])
  main()