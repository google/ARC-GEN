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
             wides=None, talls=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    colors: The colors of the boxes.
    wides: The widths of the boxes.
    talls: The heights of the boxes.
  """

  if width is None:
    width, height = common.randint(6, 16), common.randint(6, 16)
    num_boxes = width * height // 30
    colors = common.choices([2, 3, 4, 8], num_boxes)
    while True:
      cdirs = [common.randint(0, 2) for _ in range(num_boxes)]
      wides = [4 if cdir == 1 else 3 for cdir in cdirs]
      talls = [4 if cdir == 2 else 3 for cdir in cdirs]
      brows = [common.randint(0, height - tall) for tall in talls]
      bcols = [common.randint(0, width - wide) for wide in wides]
      if not common.overlaps(brows, bcols, wides, talls, 1): break

  grid, output = common.grids(width, height)
  for brow, bcol, color, wide, tall in zip(brows, bcols, colors, wides, talls):
    bgcolor = 7 if wide == 4 or tall == 4 else 5
    common.rect(output, wide, tall, brow, bcol, bgcolor)
    common.hollow_rect(grid, wide, tall, brow, bcol, color)
    common.hollow_rect(output, wide, tall, brow, bcol, color)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=6, height=6, brows=[1], bcols=[0], colors=[4], wides=[3],
               talls=[4]),
      generate(width=6, height=6, brows=[1], bcols=[1], colors=[8], wides=[3],
               talls=[3]),
      generate(width=12, height=16, brows=[1, 2, 9, 9, 13],
               bcols=[1, 7, 3, 8, 5], colors=[4, 3, 3, 2, 2],
               wides=[4, 3, 3, 4, 3], talls=[3, 4, 3, 3, 3]),
      generate(width=13, height=13, brows=[1, 1, 5, 9, 10],
               bcols=[1, 7, 3, 7, 0], colors=[4, 2, 3, 3, 8],
               wides=[3, 3, 4, 3, 4], talls=[3, 3, 3, 3, 3]),
  ]
  test = [
      generate(width=12, height=13, brows=[1, 2, 7, 7, 9],
               bcols=[1, 6, 0, 4, 9], colors=[4, 2, 3, 2, 3],
               wides=[3, 4, 3, 3, 3], talls=[3, 3, 4, 3, 3]),
  ]
  return {"train": train, "test": test}
