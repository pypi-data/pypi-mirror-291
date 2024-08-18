from argparse import ArgumentParser


def main():

  parser = ArgumentParser()
  parser.add_argument('-i', '--input', required=True)
  parser.add_argument('-o', '--output', required=True)
  parser.add_argument('-b', '--blobs', required=True)
  parser.add_argument('--url')

  parser.add_argument('-p', '--port', type=int, default=8000)
  parser.add_argument('--host', default='0.0.0.0')

  args = parser.parse_args()

  from dslog import Logger
  logger = Logger.click().prefix('[ANNOTATION]')
  logger('Starting annotation pipeline...')
  logger('- Input:', args.input)
  logger('- Output:', args.output)
  logger('- Blobs conn str:', args.blobs)
  logger('Pipeline URL:', args.url)

  from kv import KV, LocatableKV, ServerKV
  from pipeteer import QueueKV
  import uvicorn
  from fastapi.middleware.cors import CORSMiddleware
  from moveread.pipelines.annotation import Annotation

  images = KV[bytes].of(args.images)
  if not isinstance(images, LocatableKV):
    if not args.url:
      raise ValueError('Provide a LocatableKV (--images) or a base URL (--url)')
    images = images.served(args.url.rstrip('/') + '/images')

  task = Annotation()
  Qin = QueueKV.sqlite(Annotation.Input, args.input)
  Qout = QueueKV.sqlite(Annotation.Output, args.output) # type: ignore

  api = task.run({'Qin': Qin, 'Qout': Qout}, {'logger': logger, 'images': images })
  api.add_middleware(CORSMiddleware, allow_origins=['*'], allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
  api.mount('/images', ServerKV(images))
  uvicorn.run(api, host=args.host, port=args.port)

if __name__ == '__main__':
  print('What the fuck vscode')
  main()