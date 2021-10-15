import os
import argparse
import pkg_resources

# dictionary of packages with PyPi different names
acronim = {'cv2': 'opencv-contrib-python'}

# Standard python libs set
std_python_lib = set(['os', 'sys', 'time', 'copy', 'datetime', 'deepcopy', 'argparse', 'pkg_resources', 'collections'])

if __name__ == '__main__':
	# get path input
	parser = argparse.ArgumentParser(description='Python scrip for creating requirements.txt files.')
	parser.add_argument('src_path', type=str, help='Path to the source code folder.')
	args = parser.parse_args()
	src_folder_path = args.src_path

	src_files = set()
	import_lines = []
	requirements_pkg = set()

	# read all .py files in dir
	for filename in os.listdir(src_folder_path):
		full_path = os.path.join(src_folder_path, filename)
		if os.path.isfile(full_path) and full_path[-3:]=='.py':
			src_files.add(filename[:-3])

			# open a .py file parse text lines and keep the ones with import word
			with open(full_path, 'r') as f:
				text = f.read().splitlines()
				for line in text:
					if 'import' in line:
						import_lines.append(line)
	
	# split import lines into words and extract packages names
	for line in import_lines:
		words = line.split(' ')
		for i, word in enumerate(words):
			if word=='from':
				w = words[i + 1].split('.')
				requirements_pkg.add(w[0])
				break
			if word=='import':
				for w in words[i + 1:]:
					if w[-1]==',':
						w = w[:-1]
						w = w.split('.')
						requirements_pkg.add(w[0])
					else:
						w = w.split('.')
						requirements_pkg.add(w[0])
						break

	# subtract local files names and standard python libs from collected packages set
	requirements_pkg = requirements_pkg - src_files - std_python_lib

	# create a new requirements.txt file in source folder
	with open(os.path.join(src_folder_path, 'requirements.txt'), 'w') as f:
		for pkg in requirements_pkg:
			if pkg in acronim.keys():
				pkg = acronim[pkg]
			f.write(pkg + '==' + pkg_resources.get_distribution(pkg).version + '\n')








