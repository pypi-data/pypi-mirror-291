from argparse import ArgumentParser

def main():
  parser = ArgumentParser()
  parser.add_argument('-o', '--output', help="Path to the typescript package's base folder", required=True)
  args = parser.parse_args()

  import sys
  from openapi_ts import generate_client
  from moveread.pipelines.annotation import api

  app = api({}) # type: ignore
  spec = app.openapi()
  generate_client(spec, args.output, logstream=sys.stderr, args={
    '--client': '@hey-api/client-fetch',
  })

if __name__ == '__main__':
  main()