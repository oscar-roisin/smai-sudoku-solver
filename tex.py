import pathlib


class Solution:
    BT, BJ, CBJ = range(3)
    _TYPE_STR_TO_INT = {"BT": 0, "BJ": 1, "CBJ": 2}
    _TYPE_INT_TO_STR = ["BT", "BJ", "CBJ"]

    def __init__(self, line):
        ind, alg, nodes, time, sol = (lambda a, b: (*a.split(), b))(*line.split(" ["))

        self.solution = list(map(int, sol.strip()[:-1].split(", ")))
        self.type = Solution._TYPE_STR_TO_INT[alg.split(".")[1]]
        self.puzzle = int(ind)
        self.nodes_expanded = int(nodes)
        self.time = float(time)


class SolutionData:
    # This file's directory
    _PATH = pathlib.Path(__file__).parent.absolute()

    @classmethod
    def construct_from_file(cls, file_path):
        data = ([], [], [])
        with open(SolutionData._PATH.joinpath(file_path)) as f:
            for line in f.readlines():
                solution = Solution(line)
                data[solution.type].append(solution)
        return cls(data)

    def __init__(self, data=None):
        self.data = ([], [], []) if data is None else data

    def to_latex_table(self, tab="  ", caption="TODO", label="TODO"):
        """Create a latex table from output data. Requires 'usepackage[table]{xcolor}'.
        """
        return "".join(
            (
                "\\begin{center}\n",
                f"{tab}\\begin{{table}}[ht]\n",
                f"{tab*2}\\centering\n",
                f'{tab*2}\\rowcolors{{2}}{{white}}{{gray!25}}\n'
                f"{tab*2}\\begin{{tabular}}{{crrrrrr}}\n",
                (
                    f"{tab*3}\\cellcolor[gray]{{0.7}} & \\multicolumn{{2}}{{c}}"
                    "{BT\\cellcolor[gray]{0.7}} & \\multicolumn{2}{c}{BJ"
                    "\\cellcolor[gray]{0.7}}  & \\multicolumn{2}{c}"
                    "{CBJ\\cellcolor[gray]{0.7}} \\\\\n"
                ),
                (
                    f"{tab*3}\\cellcolor[gray]{{0.7}} Test suite & "
                    "\\multicolumn{1}{c}{\\cellcolor[gray]{0.7}Nodes} & "
                    "\\multicolumn{1}{c}{\\cellcolor[gray]{0.7}Time(s)} & "
                    "\\multicolumn{1}{c}{\\cellcolor[gray]{0.7}Nodes} & "
                    "\\multicolumn{1}{c}{\\cellcolor[gray]{0.7}Time(s)} & "
                    "\\multicolumn{1}{c}{\\cellcolor[gray]{0.7}Nodes} & "
                    "\\multicolumn{1}{c}{\\cellcolor[gray]{0.7}Time(s)}\\\\\n"
                ),
                "".join(
                    (
                        f"{tab*3}{i} & {bt.nodes_expanded} & {bt.time} "
                        f"& {bj.nodes_expanded} & {bj.time} & {cbj.nodes_expanded} & "
                        f"{cbj.time}\\\\\n"
                        for i, (bt, bj, cbj) in enumerate(zip(*self.data))
                    )
                ),
                f"{tab*2}\\end{{tabular}}\n"
                f"{tab*2}\\caption{{{caption}}}\n"
                f"{tab*2}\\label{{tab:{label}}}\n"
                f"{tab}\\end{{table}}\n"
                "\\end{center}",
            )
        )

def main():
    # Before use:
    # Remove everything from output.txt
    # Run an experiment with ony BT, BJ and CBJ enabled
    # Make sure the following
    #   -g off
    #   -t on [is by default]
    # Arc consistency can be either on or off

    # Path is relative from the file containing this class
    sol_data = SolutionData.construct_from_file('output-benchmark-a.txt')
    print(sol_data.to_latex_table())
    # add \usepackage[table]{xcolor} to your .tex
    # copy-paste to your .tex
    # profit


if __name__ == "__main__":
    main()