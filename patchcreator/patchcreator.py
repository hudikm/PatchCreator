import subprocess
import os
import argparse
import json
import sys
import re
from pprint import pprint
from asciitree import LeftAligned
from asciitree.drawing import BoxStyle, BOX_LIGHT, BOX_BLANK
from collections import OrderedDict as OD

VERTICAL_CHAR = '│'
HORIZONTAL_STR = "├──"
LAST_HORIZONTAL_STR = "└──"

class OutputFormat:
    commitMsgs = None
    commitHash = None
    remoteUrl = None
    commitDiff = None
    fileList = None

    def __init__(self, commitTag, commitMsg, commitHash, remoteUrl, commitDiff, fileList):
        self.commitTag = commitTag
        self.commitMsg = commitMsg
        self.commitHash = commitHash
        self.commitDiff = commitDiff
        self.remoteUrl = remoteUrl
        self.fileList = fileList


def build_nested_helper(path, text, container):
    segs = path.split('/')
    head = segs[0]
    tail = segs[1:]
    if not tail:
        container[head] = OD()
        # container.move_to_end(head, last=False)
    else:
        if head not in container:
            container[head] = OD()
            container.move_to_end(head, last=False)
        build_nested_helper('/'.join(tail), text, container[head])


def build_nested(paths):
    container = OD()
    for path in paths:
        build_nested_helper(path, path, container)
    return container


def build_tree(container, level, divider, tree_str):
    if level == 0:
        tree_str = "."

    if len(container.items()) > 0:
        if tree_str[:-1] != '\n':
            tree_str += "\n"

    for k, v in container.items():
        if not isinstance(v, dict) and v != "":
            tree_str += (level + v + "\n")

    for k, v in container.items():
        if isinstance(v, dict):
            if len(container) == 1:
                tree_str += (k + '\n')
            else:
                tree_str += level + divider + k
            tree_str = build_tree(v, level + "  ", "/", tree_str)

    return tree_str


def tree_structure(file_list):
    list_dict = {" .": OD(build_nested(file_list))}
    tr = LeftAligned(draw=BoxStyle(gfx=BOX_LIGHT, horiz_len=1))
    return tr(list_dict)


def main():
    cliParser = argparse.ArgumentParser(description='Generate code patch file')
    cliParser.add_argument('gitdir', metavar='gitdir', type=str, nargs=1, help='Location of git repo.')
    cliParser.add_argument('outfile', nargs='?', type=argparse.FileType('w'), default=sys.stdout)
    # cliParser.add_argument('outfile', metavar='outfile', type=str, nargs=1, help='Output file')
    # cliParser.add_argument('-d', '--diff_file', metavar='diff_file', type=str, nargs='?', help='Git diff file/url')
    cliParser.add_argument('-e', '--encoding', metavar='encoding', type=str, nargs='?', help='Encodning', default='UTF-8')
    cliParser.add_argument('--git-path', metavar='git_path', type=str, nargs='?', default="./", help="When paths are given, show them (note that this isn’t really raw pathnames, but rather a list of patterns to match). Otherwise implicitly uses the root level  of the tree as the sole path argument. Example: \"app/src/main/res/layout/ app/src/main/java/\"")
    args = cliParser.parse_args()
    assert os.path.isdir(args.gitdir[0])
    encoding = args.encoding
    git_path = args.git_path

    os.chdir(args.gitdir[0])

    output = subprocess.run(["git", "log", "--pretty=%s", "--reverse"], capture_output=True)
    listOfCommitsTags = []

    listOfCommitsMsgs = list(filter(None, output.stdout.decode(encoding).split('\n')))
    for i, msg in enumerate(listOfCommitsMsgs):
        groups = re.findall(r"^\s*('|\")?(?(1)(.*?)('|\")|(\S*)) *(.*)", msg, re.M)
        listOfCommitsTags.append(groups[0][1] + groups[0][3])
        listOfCommitsMsgs[i] = groups[0][4]

    output = subprocess.run(["git", "log", "--pretty=%H", "--reverse"], capture_output=True)
    listOfCommitsHASH = list(filter(None, output.stdout.decode().split('\n')))

    remoteUrl = subprocess.run(["git", "remote", "get-url", "--push", "origin"], capture_output=True).stdout\
        .decode(encoding).replace('\n', '')

    outputDiff = []
    itercars = iter(listOfCommitsHASH)
    next(itercars)
    for index, hash in enumerate(itercars, start=1):
        ls = ["git", "ls-tree", "--name-only", "-r", hash]
        ls.extend(git_path.split(' '))
        file_list = subprocess.run(ls, capture_output=True).stdout.decode(encoding).split('\n')
        file_list = list(filter(None, file_list))

        outputDiff.append(OutputFormat(listOfCommitsTags[index]
                                       , listOfCommitsMsgs[index]
                                       , listOfCommitsHASH[index]
                                       , remoteUrl
                                       , subprocess.run(["git", "diff", hash+"^!"], capture_output=True)
                                       .stdout.decode(encoding)
                                       , tree_structure(file_list)))

    json.dump(outputDiff, default=lambda a: a.__dict__, indent=4, fp=args.outfile, ensure_ascii=False)
    # jsontxt = json.dumps(outputDiff, default=lambda a: a.__dict__, indent=4, ensure_ascii=False)
    # obj = json.loads(jsontxt,encoding=encoding)


if __name__ == "__main__":
    main()

