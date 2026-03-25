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


def generate(width=None, height=None, lengths=None, colors=None, ocols=None,
             irows=None, icols=None, angles=None, bgcolor=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    lengths: The lengths of the boxes.
    colors: The colors of the boxes.
    ocols: The output columns of the boxes.
    irows: The input rows of the boxes.
    icol: The input columns of the boxes.
    angles: Whether the boxes are rotated.
    bgcolor: The color of the floor / background.
  """

  if width is None:
    num_boxes = common.randint(1, 3)
    lengths = sorted(common.sample(list(range(1, 5)), num_boxes))
    bgcolor = common.random_color()
    colors = common.random_colors(num_boxes, exclude=[bgcolor])
    angles = [common.randint(0, 1) for _ in range(num_boxes)]
    col, ocols = 1, []
    for length in lengths:
      ocols.append(col)
      col += length + common.randint(1, 3)
    width, height = col, max(sum(lengths) + 3, 5)
    talls = [length if angle else 2 for length, angle in zip(lengths, angles)]
    wides = [2 if angle else length for length, angle in zip(lengths, angles)]
    while True:
      irows = [common.randint(0, height - 3 - tall) for tall in talls]
      icols = [common.randint(0, width - wide) for wide in wides]
      if not common.overlaps(irows, icols, wides, talls, 1): break

  grid, output = common.grids(width, height)
  common.rect(grid, width, 2, height - 2, 0, bgcolor)
  common.rect(output, width, 2, height - 2, 0, bgcolor)
  for length, color, ocol, irow, icol, angle in zip(lengths, colors, ocols, irows, icols, angles):
    common.rect(grid, 2 if angle else length, length if angle else 2, irow, icol, color)
    common.rect(grid, length, 2, height - 3, ocol, 0)
    common.rect(output, length, 2, height - 3, ocol, color)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=5, height=4, lengths=[1], colors=[8], ocols=[1], irows=[0], icols=[2], angles=[1, 1], bgcolor=3),
      generate(width=8, height=8, lengths=[2, 3], colors=[5, 2], ocols=[1, 4], irows=[3, 1], icols=[5, 0], angles=[0, 0], bgcolor=8),
      generate(width=12, height=9, lengths=[1, 2, 3], colors=[5, 6, 7], ocols=[1, 3, 7], irows=[0, 3, 3], icols=[7, 0, 4], angles=[0, 1, 1], bgcolor=1),
      generate(width=6, height=7, lengths=[1, 2], colors=[2, 3], ocols=[1, 3], irows=[1, 2], icols=[1, 4], angles=[1, 1], bgcolor=1),
  ]
  test = [
      generate(width=11, height=7, lengths=[1, 2, 4], colors=[6, 1, 2], ocols=[1, 3, 6], irows=[0, 2, 0], icols=[3, 7, 0], angles=[1, 1, 1], bgcolor=5),
  ]
  return {"train": train, "test": test}
