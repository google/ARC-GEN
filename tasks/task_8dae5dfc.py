# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Generator."""

import common


def generate(width=None, height=None, wides=None, talls=None, brows=None,
             bcols=None, thicks=None, colors=None, groups=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    thicks: The thicknesses of the colors.
    colors: The colors of the colors.
    groups: The groups of the colors.
  """

  if width is None:
    width, height = common.randint(16, 20), common.randint(16, 20)
    num_boxes = common.randint(1, 3)
    # First, choose the sizes and locations of the boxes.
    while True:
      wides = [common.randint(6, 12) for _ in range(num_boxes)]
      talls = [common.randint(6, 12) for _ in range(num_boxes)]
      brows = [common.randint(0, height - tall) for tall in talls]
      bcols = [common.randint(0, width - wide) for wide in wides]
      if not common.overlaps(brows, bcols, wides, talls, 1): break
    # Second, choose the thicknesses and colors of the lines.
    # (it gets tricky because we don't want a middle thickness of 3/4 units)
    thicks, colors, groups = [], [], []
    for group in range(num_boxes):
      length, i, strata = min(wides[group], talls[group]), 0, []
      while True:
        if i >= length: break
        stratum = common.randint(1, 1 if i + 4 >= length else 2)
        strata.append(stratum)
        i += 2 * stratum
      thicks.extend(strata)
      colors.extend(common.random_colors(len(strata)))
      groups.extend([group] * len(strata))

  grid, output = common.grids(width, height)
  for i, (wide, tall, brow, bcol) in enumerate(zip(wides, talls, brows, bcols)):
    the_thicks = [thick for thick, group in zip(thicks, groups) if group == i]
    the_colors = [color for color, group in zip(colors, groups) if group == i]
    r, c, w, t = brow, bcol, wide, tall
    for thick, color in zip(the_thicks, the_colors):
      for _ in range(thick):
        common.hollow_rect(grid, w, t, r, c, color)
        w, t, r, c = w - 2, t - 2, r + 1, c + 1
    the_colors = the_colors[::-1]
    r, c, w, t = brow, bcol, wide, tall
    for thick, color in zip(the_thicks, the_colors):
      for _ in range(thick):
        common.hollow_rect(output, w, t, r, c, color)
        w, t, r, c = w - 2, t - 2, r + 1, c + 1
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=17, height=17, wides=[6, 12], talls=[6, 10], brows=[0, 7],
               bcols=[0, 4], thicks=[1, 1, 1, 1, 1, 1, 1, 1],
               colors=[8, 2, 1, 6, 3, 4, 2, 1],
               groups=[0, 0, 0, 1, 1, 1, 1, 1]),
      generate(width=16, height=18, wides=[12], talls=[12], brows=[2],
               bcols=[2], thicks=[2, 1, 2, 1], colors=[1, 3, 8, 2],
               groups=[0, 0, 0, 0]),
      generate(width=19, height=17, wides=[9, 12], talls=[7, 8], brows=[0, 9],
               bcols=[3, 1], thicks=[2, 1, 1, 1, 1, 1, 1],
               colors=[1, 6, 8, 2, 4, 1, 8], groups=[0, 0, 0, 1, 1, 1, 1]),
      generate(width=19, height=18, wides=[10, 6], talls=[13, 6], brows=[1, 2],
               bcols=[2, 13], thicks=[1, 2, 1, 1, 1, 1, 1],
               colors=[8, 7, 4, 3, 2, 1, 3], groups=[0, 0, 0, 0, 1, 1, 1]),
  ]
  test = [
      generate(width=19, height=20, wides=[10, 6, 13], talls=[9, 6, 9],
               brows=[1, 4, 11], bcols=[1, 13, 3],
               thicks=[2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
               colors=[3, 6, 1, 4, 5, 4, 8, 6, 8, 2, 4, 3],
               groups=[0, 0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 2]),
  ]
  return {"train": train, "test": test}
