from dataset_sh import create
from dataset_sh.utils.files import checksum
from dataset_sh.utils.misc import get_tqdm
from dataset_sh.constants import DEFAULT_COLLECTION_NAME


def dump_single_collection(fn, data, name=DEFAULT_COLLECTION_NAME, silent=False):
    with create(fn) as out:
        out.add_collection(name, data, data[0].__class__, tqdm=get_tqdm(silent=silent))
    return checksum(fn)


def dump_collections(fn, data_dict, report_item_progress=False, report_collection_progress=False):
    inner_tqdm = get_tqdm(silent=not report_item_progress)
    with create(fn) as out:
        for name, data in data_dict.items():
            if report_collection_progress:
                print(f'Importing collection {name}')
            if len(data) > 0:
                out.add_collection(name, data, data[0].__class__, tqdm=inner_tqdm)
    return checksum(fn)
