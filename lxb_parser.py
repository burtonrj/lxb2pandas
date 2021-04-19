import pandas as pd
import numpy as np
import flowio
import sys
import os


def _get_channel_mappings(fluoro_dict: dict) -> list:
    """
    Parse the standard dictionary of FCS channels from flowio.FlowData to
    generate a list of channel, marker mappings.

    :param dict fluoro_dict: standard dictionary of FCS channels from flowio.FlowData
    :return: list of dictionaries of type {'channel': str, 'marker': str}
    :rtype: list
    """
    fm = [(int(k), x) for k, x in fluoro_dict.items()]
    fm = [x[1] for x in sorted(fm, key=lambda x: x[0])]
    mappings = []
    for fm_ in fm:
        channel = fm_['PnN'].replace('_', '-')
        if 'PnS' in fm_.keys():
            marker = fm_['PnS'].replace('_', '-')
        else:
            marker = ''
        mappings.append({'channel': channel, 'marker': marker})
    return mappings


def parse_lxb(path: str):
    """
    Read the contents of a Luminex FCS file (file extension 'lxb') and generate a
    DataFrame of bead fluorescence. The function should be targeted at a directory containing
    the lxb files for a luminex plate. The files must have in their filename the well ID, in
    the format somefilename_{well_id}.lxb. This well identifier will be included in the
    returned dataframe.

    :param str path: directory containing lxb files
    :return: Pandas.DataFrame
    """
    raw_data = list()
    files = os.listdir(path)
    for well_file in files:
        lxb = flowio.FlowData(os.path.join(path, well_file))
        event_data = np.reshape(np.array(lxb.events, dtype=np.float32), (-1, lxb.channel_count))
        lxbdata = pd.DataFrame(event_data, columns=[x.get("marker") for x in _get_channel_mappings(lxb.channels)])
        well_id = well_file.split("_")
        well_id = well_id[len(well_id) - 1].replace(".lxb", "")
        lxbdata["Well"] = well_id
        raw_data.append(lxbdata)
    return pd.concat(raw_data)
    
if __name__ == "__main__":
    assert os.path.isdir(sys.argv[1]), f"{sys.argv[1]} is not a valid directory"
    data = parse_lxb(sys.argv[1])
    try:
        data.to_csv(sys.argv[2], index=False)
    except IndexError:
        data.to_csv("luminex_data.csv", index=False)
    

