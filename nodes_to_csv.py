#!/usr/bin/env python

import inkex
import os
import simpletransform
import cubicsuperpath


class NodesToCSV(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)
        self.OptionParser.add_option(
            "--output_dir", type="string", dest="output_dir", default="/tmp"
        )
        self.OptionParser.add_option(
            "--output_filename",
            type="string",
            dest="output_filename",
            default="points.csv",
        )
        self.OptionParser.add_option(
            "--seperator", type="string", dest="seperator", default=","
        )
        self.OptionParser.add_option(
            "--origin", type="string", dest="origin", default="south_west_corner"
        )
        self.OptionParser.add_option(
            "--x_offset", type="float", dest="x_offset", default="0.0"
        )
        self.OptionParser.add_option(
            "--y_offset", type="float", dest="y_offset", default="0.0"
        )

    def effect(self):
        sep = self.options.seperator
        f = open(
            os.path.join(self.options.output_dir, self.options.output_filename), "w"
        )
        x_off = self.options.x_offset
        y_off = self.options.y_offset
        # Get document height and trim the units string off the end
        doc_h = float(self.getDocumentHeight()[:-2])

        for node in self.selected.values():
            if node.tag == inkex.addNS("path", "svg"):
                # Make sure the path is in absolute coords
                simpletransform.fuseTransform(node)
                path = cubicsuperpath.parsePath(node.get("d"))
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
    nodesToCSV.affect()