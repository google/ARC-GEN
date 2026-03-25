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
             bcols=None, icolors=None, ocolors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    wides: The widths of the boxes.
    talls: The heights of the boxes.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    icolors: The colors of the input boxes.
    ocolors: The colors of the output boxes.
  """

  def make_boxes(num_boxes, wide, tall, brow, bcol, inner_container, outer_container):
    nonlocal wides, talls, brows, bcols, icolors, ocolors
    the_wides = [common.randint(1, wide) for _ in range(num_boxes)]
    the_talls = [common.randint(1, tall) for _ in range(num_boxes)]
    the_brows = [common.randint(brow, brow + tall - t) for t in the_talls]
    the_bcols = [common.randint(bcol, bcol + wide - w) for w in the_wides]
    exclude = []
    if inner_container != -1: exclude.append(inner_container)
    if outer_container != -1: exclude.append(outer_container)
    the_icolors = common.random_colors(num_boxes, exclude=exclude)
    the_ocolors = the_icolors
    if outer_container != -1: the_ocolors = [outer_container for _ in range(num_boxes)]
    if common.overlaps(the_brows, the_bcols, the_wides, the_talls, 1): return False
    wides.extend(the_wides)
    talls.extend(the_talls)
    brows.extend(the_brows)
    bcols.extend(the_bcols)
    icolors.extend(the_icolors)
    ocolors.extend(the_ocolors)
    for w, t, r, c, i, o in zip(the_wides, the_talls, the_brows, the_bcols, the_icolors, the_ocolors):
      if w < 3 or t < 3: continue  # Too small to contain other boxes.
      sub_boxes = common.randint(0, num_boxes)
      if not sub_boxes: continue  # No sub-boxes needed.
      if not make_boxes(sub_boxes, w - 2, t - 2, r + 1, c + 1, i, o): return False
    return True

  if width is None:
    while True:
      width, height = common.randint(10, 30), common.randint(10, 30)
      if width + height >= 30: break
    num_boxes = (width + height) // 10 - 2
    min_total_boxes = common.randint(2 * num_boxes, 3 * num_boxes)
    if num_boxes == 1:
      min_total_boxes = common.randint(3 * num_boxes, 4 * num_boxes)
    while True:
      wides, talls, brows, bcols, icolors, ocolors = [], [], [], [], [], []
      if not make_boxes(num_boxes, width, height, 0, 0, -1, -1): continue
      if len(wides) < min_total_boxes: continue
      break

  grid, output = common.grids(width, height)
  for w, t, r, c, i, o in zip(wides, talls, brows, bcols, icolors, ocolors):
    common.hollow_rect(grid, w, t, r, c, i)
    common.hollow_rect(output, w, t, r, c, o)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=28, height=22, wides=[19, 13, 7, 6, 4, 5],
               talls=[16, 11, 6, 11, 4, 5], brows=[3, 5, 8, 1, 5, 15],
               bcols=[1, 3, 7, 21, 22, 22], icolors=[2, 4, 1, 1, 6, 3],
               ocolors=[2, 2, 2, 1, 1, 3]),
      generate(width=27, height=23, wides=[14, 6, 2, 3, 9, 5, 11],
               talls=[11, 6, 1, 5, 16, 10, 7], brows=[1, 3, 5, 5, 5, 8, 14],
               bcols=[1, 3, 5, 10, 18, 20, 3], icolors=[8, 4, 3, 2, 7, 1, 4],
               ocolors=[8, 8, 8, 8, 7, 7, 4]),
      generate(width=18, height=12, wides=[15, 8, 2, 2], talls=[10, 6, 2, 2],
               brows=[1, 3, 5, 3], bcols=[2, 4, 6, 13], icolors=[1, 2, 8, 3],
               ocolors=[1, 1, 1, 1]),
  ]
  test = [
      generate(width=28, height=29, wides=[21, 16, 9, 2, 1, 13, 8, 2, 9, 3],
               talls=[15, 11, 7, 2, 2, 10, 6, 2, 7, 3],
               brows=[1, 3, 5, 7, 11, 18, 20, 22, 18, 20],
               bcols=[2, 5, 10, 12, 25, 2, 4, 8, 16, 19],
               icolors=[4, 3, 8, 1, 6, 1, 3, 2, 8, 4],
               ocolors=[4, 4, 4, 4, 6, 1, 1, 1, 8, 8]),
  ]
  return {"train": train, "test": test}
