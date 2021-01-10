import os


def combine_sectors(chunk_paths: list, result_path):
	from PIL import Image

	chunk_paths.sort(key=os.path.getmtime)
	result = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
	for chunk_path in chunk_paths:
		result = Image.alpha_composite(Image.open(chunk_path), result)
	result.save(result_path)


def get_atlas(path):
	names = os.listdir(path)
	dims = [name for name in names if os.path.basename(name) != 'waypoints']

	atlas = dict([(
		dim,
		dict([(
			level,
			dict(map(
				lambda sector: (sector, [os.path.join(path, dim, level, sector)]),
				os.listdir(os.path.join(path, dim, level))))
		) for level in os.listdir(os.path.join(path, dim))])
	) for dim in dims])

	return atlas


def combine_atlases(atlases: list):
	combined_atlas = {}
	for atlas in atlases:
		for dim in atlas.keys():
			if dim not in combined_atlas:
				combined_atlas[dim] = {}
			for level in atlas[dim].keys():
				if level not in combined_atlas[dim]:
					combined_atlas[dim][level] = {}
				for sector in atlas[dim][level].keys():
					if sector not in combined_atlas[dim][level]:
						combined_atlas[dim][level][sector] = atlas[dim][level][sector]
					else:
						combined_atlas[dim][level][sector] += atlas[dim][level][sector]
	return combined_atlas


def write_atlas(atlas, path):
	for dim in atlas.keys():
		for level in atlas[dim].keys():
			for sector in atlas[dim][level].keys():
				level_dir = os.path.join(path, dim, level)
				if not os.path.exists(level_dir):
					os.makedirs(level_dir)
				combine_sectors(
					atlas[dim][level][sector],
					os.path.join(level_dir, sector)
				)


def journeypatch(atlas_paths: list, result_path):
	atlases = [get_atlas(atlas_path) for atlas_path in atlas_paths]
	combined_atlas = combine_atlases(atlases)
	write_atlas(combined_atlas, result_path)



