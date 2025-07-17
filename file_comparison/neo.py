# Neo
from collections.abc import Iterable
import neo.io
import file_comparison.report_generator as rg
from packaging.version import Version

neo_version = str(neo.__version__)


def compute_score (number_of_errors, number_of_values):
    score = 100. - (number_of_errors*100./number_of_values)
    return (score)

def check_array_size_warning (array1, array2):
    # Assert blocks or segments have same size
    if len(array1) != len(array2):
        # print ("NEO Error:" + self.file1.url + self.file1.name + " and " + self.file2.url + self.file2.name + " do not have the same number of " + str(type(array1).__name__))
        print ("NEO Warning: Number of " + str(type(array1).__name__) + " are not equal: not all " + str(type(array1).__name__) + " will be compared" )

def check_file_formats (filepath):
    try:
        neo.io.get_io(filepath)
        return True, None
    except Exception as e:
        print ("Error " + str(type(e)) + " :: Neo method: " + str(e))
        return False, str(e)



def extract_neo_block (block, path, data):
    # assert(len(neoblock1.segments) == len(neoblock2.segments))
    # print ("nombre de segment = " + str(len(neoblock1.segments)))
    for isegment_idx in range(len(block.segments)):
        extract_neo_segment (block.segments[isegment_idx], path + "->segment[" + str(isegment_idx) + "]", data)

    if Version(neo_version) >= Version("0.9.0"):
        for igroup_idx in range(len(block.groups)):
            extract_neo_group (block.groups[igroup_idx], path + "->group[" + str(igroup_idx) + "]", data)

def extract_neo_group (group, path, data):

    for igroup_idx in range(len(group.groups)):
        extract_neo_group (group.groups[igroup_idx], path + "->group[" + str(igroup_idx) + "]", data)

    extract_neo_segment (group, path, data)

def extract_neo_data (file, data):
    try:
        file_path = file.url + file.name

        neo_reader = neo.io.get_io(file_path)

        blocks = neo_reader.read()

        for iblock_idx in range(len(blocks)):
            extract_neo_block (blocks[iblock_idx], "R->block[" + str(iblock_idx) + "]", data)
    except Exception as e:
        print ("Neo :: " + str(type(e).__name__) + " " + str(e))


def extract_neo_segment (segment, path, data):
    try:
        # Group objects
        # print (path + "->channelview")
        # print (segment1.channelview)
        for ivar_idx in range(len(segment.channelview)):
            data[str(path+str("->channelview[" + str(ivar_idx) + "]") + "->")] = segment.channelview[ivar_idx]
    except Exception as e:
        print (type(segment.channelview))
        print (type(segment))
        print ("Error Neo :: " + str(e))

    try:
        # print (path + "->analogsignals")
        for ivar_idx in range(len(segment.analogsignals)):
            data[str(path+str("->analogsignals[" + str(ivar_idx) + "]") + "->")] = segment.analogsignals[ivar_idx]
    except Exception as e:
        print ("Error Neo :: " + str(e))

    try:
    #     print (path + "->irregularlysampledsignals")
        for ivar_idx in range(len(segment.irregularlysampledsignals)):
            data[str(path+str("->irregularlysampledsignals[" + str(ivar_idx) + "]") + "->")] = segment.irregularlysampledsignals[ivar_idx]
    except Exception as e:
        print ("Error Neo :: " + str(e))

    try:
    #     print (path + "->spiketrains")
        for ivar_idx in range(len(segment.spiketrains)):
            data[str(path+str("->spiketrains[" + str(ivar_idx) + "]") + "->")] = segment.spiketrains[ivar_idx]
    except Exception as e:
        print ("Error Neo :: " + str(e))

    try:
        for ivar_idx in range(len(segment.events)):
            data[str(path+str("->events[" + str(ivar_idx) + "]") + "->")] = segment.events[ivar_idx]
    except Exception as e:
        print ("Error Neo :: " + str(e))

    try:
        for ivar_idx in range(len(segment.epochs)):
            data[str(path+str("->epochs[" + str(ivar_idx) + "]") + "->")] = segment.epochs[ivar_idx]
    except Exception as e:
        print ("Error Neo :: " + str(e))

def compare_segments (original_segment, new_segment, path, block_diff):

    if type(original_segment) == type(None) or type(original_segment) == type(None):
        block_diff["error"].append (path + " Segment is None ")
        block_diff["nerrors"] += 1
    else:
        try:
            # Channelview data
            if len(original_segment.channelview) != len(new_segment.channelview):
                block_diff["error"].append (path + " channelview are not the same size")
                block_diff["nerrors"] += 1
                block_diff["ndiff"] += abs(len(original_segment.channelview) - len(new_segment.channelview))
                block_diff["log"].append (path + " channelview are not the same size")
              
            for ivar_idx in range(min(len(original_segment.channelview), len(new_segment.channelview))):
                if original_segment.channelview[ivar_idx].all() != new_segment.channelview[ivar_idx].all():
                    block_diff["report"].append (rg.compute_1el_difference (original_segment.channelview[ivar_idx], new_segment.channelview[ivar_idx]))
        except Exception as e:
            block_diff["log"].append (path + " " + str(e))

        try:
            # Analog Signals
            if len(original_segment.analogsignals) != len(new_segment.analogsignals):
                block_diff["error"].append (path + " analogsignals are not the same size")
                block_diff["nerrors"] += 1
                block_diff["ndiff"] += abs(len(original_segment.analogsignals) - len(new_segment.analogsignals))
                block_diff["log"].append (path + " analogsignals are not the same size")

            for ivar_idx in range(min(len(original_segment.analogsignals), len(new_segment.analogsignals))):
                if original_segment.analogsignals[ivar_idx].all() != new_segment.analogsignals[ivar_idx].all():
                    block_diff["report"].append (rg.compute_1el_difference (original_segment.analogsignals[ivar_idx], new_segment.analogsignals[ivar_idx]))
        except Exception as e:
            block_diff["log"].append (path + " " + str(e))

        try:
            # irregularly sampled signals
            if len(original_segment.irregularlysampledsignals) != len(new_segment.irregularlysampledsignals):
                block_diff["error"].append (path + " irregularlysampledsignals are not the same size")
                block_diff["nerrors"] += 1
                block_diff["ndiff"] += abs(len(original_segment.irregularlysampledsignals) - len(new_segment.irregularlysampledsignals))
                block_diff["log"].append (path + " irregularlysampledsignals are not the same size")

            for ivar_idx in range(min(len(original_segment.irregularlysampledsignals), len(new_segment.irregularlysampledsignals))):
                if original_segment.irregularlysampledsignals[ivar_idx].all() != new_segment.irregularlysampledsignals[ivar_idx].all():
                    block_diff["report"].append (rg.compute_1el_difference (original_segment.irregularlysampledsignals[ivar_idx], new_segment.irregularlysampledsignals[ivar_idx]))
        
        except Exception as e:
            block_diff["log"].append (path + " " + str(e))

        try:
            # Spiketrains
            if len(original_segment.spiketrains) != len(new_segment.spiketrains):
                block_diff["error"].append (path + " spiketrains are not the same size")
                block_diff["nerrors"] += 1
                block_diff["ndiff"] += abs(len(original_segment.spiketrains) - len(new_segment.spiketrains))
                block_diff["log"].append (path + " spiketrains are not the same size")

            for ivar_idx in range(min(len(original_segment.spiketrains), len(new_segment.spiketrains))):
                if original_segment.spiketrains[ivar_idx].all() != new_segment.spiketrains[ivar_idx].all():
                    block_diff["report"].append (rg.compute_1el_difference (original_segment.spiketrains[ivar_idx], new_segment.spiketrains[ivar_idx]))
        except Exception as e:
            block_diff["log"].append (path + " " + str(e))

        try:
            # Events
            if len(original_segment.events) != len(new_segment.events):
                block_diff["error"].append (path + " events are not the same size")
                block_diff["nerrors"] += 1
                block_diff["ndiff"] += abs(len(original_segment.events) - len(new_segment.events))
                block_diff["log"].append (path + " events are not the same size")

            for ivar_idx in range(min(len(original_segment.events), len(new_segment.events))):
                if original_segment.events[ivar_idx].all() != new_segment.events[ivar_idx].all():
                    block_diff["report"].append (rg.compute_1el_difference (original_segment.events[ivar_idx], new_segment.events[ivar_idx]))
        except Exception as e:
            block_diff["log"].append (path + " " + str(e))

        try:
            # Epochs
            if len(original_segment.epochs) != len(new_segment.epochs):
                block_diff["error"].append (path + " epochs are not the same size")
                block_diff["nerrors"] += 1
                block_diff["ndiff"] += abs(len(original_segment.epochs) - len(new_segment.epochs))
                block_diff["log"].append (path + " epochs are not the same size")

            for ivar_idx in range(min(len(original_segment.epochs), len(new_segment.epochs))):
                if original_segment.epochs[ivar_idx].all() != new_segment.epochs[ivar_idx].all():
                    block_diff["report"].append (rg.compute_1el_difference (original_segment.epochs[ivar_idx], new_segment.epochs[ivar_idx]))
        except Exception as e:
            block_diff["log"].append (path + " " + str(e))

    return block_diff


def compare_groups (original_group, new_group, path, block_diff):

    if len(original_group.groups) != len(new_group.groups):
        block_diff["error"].append (path + " group have different number of groups")
        block_diff["nerrors"] += 1
        block_diff["ndiff"] += abs(len(original_group.groups) - len(new_group.groups))
        block_diff["log"].append (path + " group have different number of groups")

    for igroup_idx in range(min(len(original_group.groups, new_group.groups))):
        block_diff = compare_groups (original_group.groups[igroup_idx], new_group.groups[igroup_idx], path + "->group[" + str(igroup_idx) + "]", block_diff)

    block_diff = compare_segments (original_group, original_group, path, block_diff)

    return block_diff

def compare_neo_blocks (original_block, new_block, path, block_diff):

    # Compare segments
    if len(original_block.segments) != len(new_block.segments):
        block_diff["error"].append (path + " block have different number of segments")
        block_diff["nerrors"] += 1
        block_diff["ndiff"] += abs(len(original_block.segments) - len(new_block.segments))
        block_diff["log"].append (path + " block have different number of segments")

    for isegment_idx in range(min (len(original_block.segments), len(new_block.segments))):
        block_diff = compare_segments (original_block.segments[isegment_idx], new_block.segments[isegment_idx], path + "->segment[" + str(isegment_idx) + "]", block_diff)

    # Compare groups
    if Version(neo_version) >= Version("0.9.0"):
        print ("Use Neo version " + str(Version(neo_version)) + " >= " + str(Version("0.9.0")) + " == " + str(Version(neo_version) >= Version("0.9.0")))
        if len(original_block.groups) != len(new_block.groups):
            block_diff["error"].append (path + " block have different number of groups")
            block_diff["nerrors"] += 1
            block_diff["ndiff"] += abs(len(original_block.groups) - len(new_block.groups))
            block_diff["log"].append (path + " block have different number of groups")
        
        for igroup_idx in range(min (len(original_block.groups), len(new_block.groups))):
            block_diff = compare_groups (original_block.groups[igroup_idx], new_block.groups[igroup_idx], path + "->group[" + str(igroup_idx) + "]", block_diff)

    return block_diff


def compute_differences_report (original_file, new_file):
    block_diff = {"report": [], "nerrors": 0, "nvalues": 0, 'ndiff': 0, "log": [], "error": []}
    comparison_path = "R"
    try:
        original_neo_reader = neo.io.get_io(original_file["path"])
        new_neo_reader = neo.io.get_io(new_file["path"])

        original_blocks = original_neo_reader.read()
        new_blocks = new_neo_reader.read()

        if len(original_blocks) != len(new_blocks):
            block_diff["error"].append ("NEO Error:" + original_file["path"] + " and " + new_file["path"] + " do not have the same number of neo:blocks")
            block_diff["nerrors"] += 1
            block_diff["ndiff"] += abs(len(original_blocks) - len(new_blocks))
            block_diff["log"].append ("NEO Warning: Number of blocks are not equal: not all blocks will be compared" )

        for iblock_idx in range(min(len(original_blocks), len(new_blocks))):
            block_diff = compare_neo_blocks(original_blocks[iblock_idx], new_blocks[iblock_idx], comparison_path + "->block[" + str(iblock_idx) + "]", block_diff)

    except Exception as e:
        block_diff["error"].append("Neo :: " + str(type(e).__name__) + " " + str(e))
        block_diff["nerrors"] += 1

    return block_diff

