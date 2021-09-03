import argparse
import os
import json


# Global Variables
waypoints = dict()


def get_xaero_format(info, isNether=False):
    if isNether:
        info['x'],info['z'] = int(info['x']) // 8, int(info['z']) // 8
    return "waypoint:{name}:{initials}:{x}:{y}:{z}:{color}:{disabled}:{type}:{set}:{rotate_on_tp}:{tp_yaw}:{global}".format_map(info)


def info_to_file():

    overworldFile = open("waypoints.txt", "w")
    netherworldFile = open("waypointsNether.txt", "w")
    endworldFile = open("waypointsEnd.txt", "w")

    for x in waypoints:
        dimension = waypoints[x]["Xaero"]["dimensions"]

        if dimension == "overworld":
            # Write to OverWorld File
            text = get_xaero_format(waypoints[x]["Xaero"])
            overworldFile.write(text)
            overworldFile.write("\n")

        elif dimension == "the_nether":
            # Write to Nether File
            text = get_xaero_format(waypoints[x]["Xaero"], isNether=True)
            netherworldFile.write(text)
            netherworldFile.write("\n")

        elif dimension == "the_end":
            # Write to End File
            text = get_xaero_format(waypoints[x]["Xaero"])
            endworldFile.write(text)
            endworldFile.write("\n")

    overworldFile.close()
    netherworldFile.close()
    endworldFile.close()


def info_converter():
    # waypoint:name:initials:x  :y :z  :color:disabled:type:set              :rotate_on_tp:tp_yaw:global
    # waypoint:Sand:S       :338:81:836:5    :false   :0   :gui.xaero_default:false       :0     :false

    for x in waypoints:
        waypoints[x]["Xaero"] = dict()
        # TODO: This for loop is kinda desnecessary but OK
        for key in waypoints[x]["Voxel"]:
            if key == "x":
                waypoints[x]["Xaero"]["x"] = waypoints[x]["Voxel"]["x"]
            if key == "y":
                waypoints[x]["Xaero"]["y"] = waypoints[x]["Voxel"]["y"]
            if key == "z":
                waypoints[x]["Xaero"]["z"] = waypoints[x]["Voxel"]["z"]
            if key == "name":
                name = waypoints[x]["Voxel"]["name"]
                waypoints[x]["Xaero"]["name"] = name
                waypoints[x]["Xaero"]["initials"] = name[0:2]
            if key == "enabled":
                if waypoints[x]["Voxel"]["enabled"] == "false":
                    waypoints[x]["Xaero"]["disabled"] = "true"
                else:
                    waypoints[x]["Xaero"]["disabled"] = "false"
            if key == "red":
                pass
            if key == "green":
                pass
            if key == "blue":
                pass
            if key == "suffix":
                pass
            if key == "dimensions":
                waypoints[x]["Xaero"]["dimensions"] = waypoints[x]["Voxel"]["dimensions"]

        waypoints[x]["Xaero"]["color"] = "1"
        waypoints[x]["Xaero"]["type"] = "0"
        waypoints[x]["Xaero"]["set"] = "gui.xaero_default"
        waypoints[x]["Xaero"]["rotate_on_tp"] = "false"
        waypoints[x]["Xaero"]["tp_yaw"] = "0"
        waypoints[x]["Xaero"]["global"] = "false"


def info_spliter():
    for x in waypoints:
        waypoints[x]["Voxel"] = dict()
        for info in waypoints[x]["text"].split(','):
            info_splitted = info.split(':')
            key, value = info_splitted

            waypoints[x]["Voxel"][key] = value


def info_loader(waypoints_text):
    for i, x in enumerate(waypoints_text):
        waypoint = dict()
        waypoint["text"] = x[0:-2]
        waypoints[i] = waypoint


def load_voxel_file(file_path):
    f = open(file_path, "r")

    for x in f:
        # Get only waypoints and nothing more
        if "name" == x[0:4]:
            yield x

    f.close()


def check_args(args):
    if not os.path.isfile(args.file_name):
        raise FileNotFoundError('VoxelMap name path does not exist.')


def arg_parser():
    parser = argparse.ArgumentParser(description='Process some integers.')
    # parser.add_argument('filename', metavar='fileName', type=str, help='Xaero file name in directory')
    parser.add_argument('-f', '--file', dest='file_name', metavar='fileName', required=True, type=str, help='Xaero file name in directory')

    args = parser.parse_args()
    return args


def run():
    # Read file

    args = arg_parser()
    # TODO: Adding robustness(cause people)

    check_args(args)
    # ------------
    if args.file_name is not None:
        voxelFilePath = args.file_name
    else:
        voxelFilePath = "D2.points"
    # ------------

    print("Voxel File path: ", voxelFilePath)
    voxelFile = load_voxel_file(voxelFilePath)

    info_loader(voxelFile)
    info_spliter()
    info_converter()

    # Split information about the different dimensions and put them on different files
    info_to_file()

    ## Debug purposes, if necessary:
    # print(json.dumps(waypoints, sort_keys=True, indent=2))


if __name__ == '__main__':
    run()
