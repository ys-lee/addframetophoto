import dcmstack
from glob import glob
src_paths = glob('/media/gregory/Acer2/Users/grego/Documents/CNI/CNI_BOSTON_DATA/WOLFSON_SUBSET_REDUCED2/sub-005/ses-4yr/Rest210_2/*.dcm')
stacks = dcmstack.parse_and_stack(src_paths,force=True)