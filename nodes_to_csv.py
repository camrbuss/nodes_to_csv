#!/usr/bin/env python

import inkex
import os
import simpletransform


class NodesToCSV(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.arg_parser.add_argument(
                "--output_dir", type=str, default="/tmp"
                )
        self.arg_parser.add_argument(
                "--output_filename",
                type=str,
                default="points.csv",
                )
        self.arg_parser.add_argument(
                "--seperator", type=str, default=","
                )
        self.arg_parser.add_argument(
                "--origin", type=str, default="south_west_corner"
                )
        self.arg_parser.add_argument(
                "--x_offset", type=float, default="0.0"
                )
        self.arg_parser.add_argument(
                "--y_offset", type=float, default="0.0"
                )

    def effect(self):
        sep = self.options.seperator
        f = open(
                os.path.join(self.options.output_dir, self.options.output_filename), "w"
                )
        x_off = self.options.x_offset
        y_off = self.options.y_offset
        # Get document height
        doc_h = self.svg.viewport_height

        for node in self.svg.selected:
            if node.tag == inkex.addNS("path", "svg"):
                # Make sure the path is in absolute coords
                # simpletransform.fuseTransform(node)
                node.apply_transform()
                path = inkex.paths.CubicSuperPath(node.get("d"))
                for sub_path in path:
                    # sub_path represents a list of all nodes in the path
                    for node in sub_path:
                        # node type is SubPath[(point_a, bezier, point_b)
                        # We dont want the control points, we only want the bezier
                        # point_a, bezier, and point_b is a list of length 2 and type float
                        x = node[1][0]
                        y = node[1][1]
                        x = x + x_off
                        if self.options.origin == "south_west_corner":
                            y = doc_h - y + y_off
                        else:
                            y = y + y_off
                        f.write(str(x) + sep + str(y) + sep + "\n")

        f.close()


if __name__ == "__main__":
    nodesToCSV = NodesToCSV()
    nodesToCSV.run()
