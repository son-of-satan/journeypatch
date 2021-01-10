from journeypatch import journeypatch
import argparse

if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		prog='journeyparser',
		description='Patch journeymap\'s map files'
	)
	parser.add_argument(
		'source', type=str, nargs='+',
	)
	parser.add_argument(
		'dest', type=str,
	)

	args = parser.parse_args()
	journeypatch(args.source+ [args.dest], args.dest)
