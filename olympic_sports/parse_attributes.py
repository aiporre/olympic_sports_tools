import numpy as np
import matplotlib.pyplot as plt
import os

N_classes_default = 16
N_attributes_default = 40
class_names_default = ['basketball_layup',
               'bowling',
               'clean_and_jerk',
               'discus_throw',
               'diving_platform_10m',
               'diving_springboard_3m',
               'hammer_throw',
               'high_jump',
               'javelin_throw',
               'long_jump',
               'pole_vault',
               'shot_put',
               'snatch',
               'tennis_serve',
               'triple_jump',
               'vault'
               ]


def parse_attributes(attr_file=None,
                     save_npz=True,
                     attr_npz_file='attributes',
                     attr_npz_path=None,
                     N_classes=None,
                     N_attributes=None,
                     class_names=None):
    '''
    Parse a Olympic_Attributes like txt file, that contains attributes list and a 0's and 1's code assigning to each class. Defaults reading the resources attribute annotations, however also receives a path to a custom txt. It can save into a npz file for faster access or just parse. If saved you shoud call method read_attributes(path_to_npz_attributes) for fast access.

    :param attr_file: File to the 0's and 1's assignment txt file
    :param save_npz: boolean to save npz file
    :param attr_npz_file:  name of the attribute file, defaults attributes.npz
    :param attr_npz_path: path to directory where npz file is saved, defaults None, uses the current directory
    :param N_classes: number of classes considered in the file of assignment, defaults 16
    :param N_attributes: number of attributes considere in the file of assignment, defaults 40
    :param class_names: names of the classes defaults to `olympic_sports.class_names`
    :return: tuple of tree arrays: attributes N_classes X N_attributes, string array of class names, string array of attributes
    '''
    if class_names is None:
        class_names = class_names_default

    if N_classes is None:
        N_classes = N_classes_default

    if N_attributes is None:
        N_attributes = N_attributes_default

    if attr_file is None:
        attr_file = os.path.join(os.path.split(__file__)[0], "resources", "Olympic_Attributes.txt")

    if attr_npz_path is None:
        attr_npz_path = os.path.join(os.getcwd(), attr_npz_file)
    cnt_line = 0
    cnt_classes = 0
    cnt_attributes = 0
    attribute_names = []
    attributes = np.zeros((N_classes, N_attributes))

    file = open(attr_file, 'r')
    for line in file:
        line = line.rstrip('\n')
        if cnt_line == 0:
            print('----------------------------------------------')
            print('Parsing attribute name')
            print('')
            cnt_classes = 0
            cnt_attributes += 1
            # parsing attribute name and index
            attribute_names.append(line)
        else:
            # parsing attribute value
            attributes[cnt_classes, cnt_attributes - 1] = int(line)
            print('Class {:02d} \t| Attribute {:02d}'.format(cnt_classes + 1, cnt_attributes + 1))
            cnt_classes += 1
        if cnt_classes == N_classes:
            cnt_line = 0
        else:
            cnt_line += 1
    if save_npz:
        print('Saving arrays into a npz file: ', attr_npz_path)
        np.savez(attr_npz_path, attributes, class_names, attribute_names)
    return attributes, class_names, attribute_names


def plot_attibutes_table(attr_file=None):
    '''
    Plots assignemnt file .txt (e.g. resources/Olympic_Attributes) as color matrix image.

    :param attr_file: path the 0's and 1's attributs file.
    :return: None
    '''
    if attr_file is None:
        attr_file = os.path.join(os.path.split(__file__)[0], "resources", "Olympic_Attributes.txt")
    attributes, class_names, attribute_names = parse_attributes(attr_file=attr_file, save_npz=False)
    plt.figure(figsize=(5, 20))
    fig, ax = plt.subplots()
    im = ax.imshow(attributes)
    # We want to show all ticks...
    ax.set_xticks(np.arange(len(attribute_names)))
    ax.set_yticks(np.arange(len(class_names)))
    # ... and label them with the respective list entries
    ax.set_xticklabels(attribute_names)
    ax.set_yticklabels(class_names)
    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right",
             rotation_mode="anchor")
    # Loop over data dimensions and create text annotations.
    for i in range(len(class_names)):
        for j in range(len(attribute_names)):
            text = ax.text(j, i, attributes[i, j],
                           ha="center", va="center", color="w")
    ax.set_title("Classes & attributes")
    fig.tight_layout()
    plt.show()


def read_attributes(attr_file=None):
    '''
    Read attributes file npz already parsed or a txt file

    :param attr_file: If None, defaults to resources module file).
    :type attr_file: str
    :return: tuple of tree arrays: attributes N_classes X N_attributes, string array of class names, string array of attributes
    '''
    if attr_file is None:
        attr_file = os.path.join(os.path.split(__file__)[0], "resources", "attributes.npz")
        nzfile = np.load(attr_file)
        attributes, class_names, attribute_names = nzfile.files
        attributes = nzfile[attributes]
        class_names = nzfile[class_names]
        attribute_names = nzfile[attribute_names]
    elif attr_file.endswith('.npz'):
        nzfile = np.load(attr_file)
        attributes, class_names, attribute_names = nzfile.files
        attributes = nzfile[attributes]
        class_names = nzfile[class_names]
        attribute_names = nzfile[attribute_names]
    elif attr_file.endswith('.txt'):
        attributes, class_names, attribute_names = parse_attributes(attr_file=attr_file, save_npz=False)

    return attributes, class_names, attribute_names
