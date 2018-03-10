#!/usr/bin/env python

import commands
import re
import subprocess



def get_gpu_map():
    """
    get the hive gpu to pci mapping

    """
    # empty python dict to hold the results
    gpu_map = {}
    # exec nvidia-smi command to get GPU mappings
    output = commands.getoutput('nvidia-smi')
    # regex match multiline to grab a list of matches for the data we want
    match = re.finditer('^\|\s+(\d+)\s.+\|\s\d+:(\d+):\d+\.\d', output, re.MULTILINE)
    if match:
        # if we made any matches iterate through them and add mfg data to gpu_map
        for m in match:
            pci_gpu_id = int(m.group(2))
            hiveos_gpu_id = int(m.group(1))
            gpu_map[pci_gpu_id] = [hiveos_gpu_id, '']

    return gpu_map


def get_gpu_mfg_info(gpu_map):
    """
    get mfg info for each gpu card
    """
    # execute fancy linux command to get verbose pci/gpu data
    # lspci | grep ' VGA ' | cut -d" " -f 1 | xargs -i lspci -v -s {}
    output = commands.getoutput('lspci | grep \' VGA \' | cut -d" " -f 1 | xargs -i lspci -v -s {}')
    # regex match multiline to grab a list of matches for the data we want
    match = re.finditer('^(\d+):\d+\.\d.+\n\s+Subsystem:\s(.+)', output, re.MULTILINE)
    if match:
        # if we made any matches iterate through them and add mfg data to gpu_map
        for m in match:
            gpu_map[int(m.group(1))][1] = m.group(2)

    return gpu_map


def main():
    # get the hive gpu to pci mapping
    gpu_map = get_gpu_map()
    # get mfg info for each gpu card
    get_gpu_mfg_info(gpu_map)

    #iterate through results and print map
    for pcigpu in gpu_map.iterkeys():
        print 'GPU{}, PCI{}, {}'.format(gpu_map[pcigpu][0], pcigpu, gpu_map[pcigpu][1])


if __name__ == "__main__":
    main()
