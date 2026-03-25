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


def generate(width=None, height=None, brows=None, bcols=None, colors=None,
             fills=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    colors: The colors of the boxes.
    fills: Whether to fill the boxes.
  """

  def get_cdir():
    sorted_brows = sorted([brow for brow, fill in zip(brows, fills) if not fill])
    sorted_bcols = sorted([bcol for bcol, fill in zip(bcols, fills) if not fill])
    brow_diffs = [sorted_brows[i] - sorted_brows[i - 1] for i in range(1, len(sorted_brows))]
    bcol_diffs = [sorted_bcols[i] - sorted_bcols[i - 1] for i in range(1, len(sorted_bcols))]
    min_brow_diff, min_bcol_diff = min(brow_diffs), min(bcol_diffs)
    if min_brow_diff < 4 and min_bcol_diff > 4: return 0
    if min_brow_diff > 4 and min_bcol_diff < 4: return 1
    return -1

  if width is None:
    num_boxes = common.randint(4, 6)
    colors = common.random_colors(num_boxes)
    # First, choose roughly an equal number of filled and non-filled boxes.
    while True:
      fills = [common.randint(0, 1) for _ in range(num_boxes)]
      filled = len([f for f in fills if f])
      nonfilled = len([f for f in fills if not f])
      if abs(filled - nonfilled) <= 1: break
    # Second, find dimensions & placements that are nonoverlapping and where
    # the "direction" of boxes is clear.
    while True:
      width, height = common.randint(15, 25), common.randint(15, 25)
      brows = [common.randint(0, height - 4) for _ in range(num_boxes)]
      bcols = [common.randint(0, width - 4) for _ in range(num_boxes)]
      if common.overlaps(brows, bcols, [5] * num_boxes, [5] * num_boxes, 0):
        continue
      if get_cdir() != -1: break

  grid = common.grid(width, height)
  for brow, bcol, color, fill in zip(brows, bcols, colors, fills):
    if fill: common.rect(grid, 4, 4, brow, bcol, color)
    else: common.hollow_rect(grid, 4, 4, brow, bcol, color)

  cdir = get_cdir()
  fillsum = sum([1 - fill for fill in fills])
  outwidth = 4 if cdir == 1 else (4 * fillsum)
  outheight = 4 if cdir == 0 else (4 * fillsum)
  output = common.grid(outwidth, outheight)
  if cdir:
    sorted_brows = sorted([(brow, color) for brow, color, fill in zip(brows, colors, fills) if not fill])
    for i, sorted_brow in enumerate(sorted_brows):
      _, color = sorted_brow
      common.hollow_rect(output, 4, 4, 4 * i, 0, color)
  else:
    sorted_bcols = sorted([(bcol, color) for bcol, color, fill in zip(bcols, colors, fills) if not fill])
    for i, sorted_bcol in enumerate(sorted_bcols):
      _, color = sorted_bcol
      common.hollow_rect(output, 4, 4, 0, 4 * i, color)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=16, height=21, brows=[1, 6, 12, 15], bcols=[8, 1, 3, 10], colors=[8, 1, 2, 4], fills=[1, 0, 0, 1]),
      generate(width=17, height=18, brows=[1, 2, 7, 12], bcols=[1, 9, 3, 10], colors=[2, 4, 3, 8], fills=[0, 0, 1, 1]),
      generate(width=22, height=24, brows=[2, 3, 6, 14, 15, 15], bcols=[16, 1, 8, 12, 2, 18], colors=[8, 1, 3, 6, 4, 2], fills=[1, 1, 0, 1, 0, 0]),
  ]
  test = [
      generate(width=21, height=22, brows=[1, 2, 6, 13, 17], bcols=[3, 16, 6, 3, 12], colors=[3, 8, 2, 4, 1], fills=[0, 1, 0, 1, 0]),
  ]
  return {"train": train, "test": test}
