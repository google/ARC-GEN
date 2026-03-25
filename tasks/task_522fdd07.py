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


def generate(rows=None, cols=None, lengths=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: The rows of the centers.
    cols: The columns of the centers.
    lengths: The lengths of the boxes.
    colors: The colors of the boxes.
  """

  if rows is None:
    num_boxes = common.randint(3, 5)
    while True:
      lengths = [common.randint(1, 5) for _ in range(num_boxes)]
      eff_lengths = [length if length > 1 else 5 for length in lengths]
      rows = [common.randint(length - 1, 16 - length) for length in eff_lengths]
      cols = [common.randint(length - 1, 16 - length) for length in eff_lengths]
      sides = [2 * length - 1 for length in lengths]
      brows = [row - side // 2 for row, side in zip(rows, sides)]
      bcols = [col - side // 2 for col, side in zip(cols, sides)]
      if common.overlaps(brows, bcols, sides, sides, 1): continue
      sides = [(2 * length - 3) if length > 1 else 9 for length in lengths]
      brows = [row - side // 2 for row, side in zip(rows, sides)]
      bcols = [col - side // 2 for col, side in zip(cols, sides)]
      if common.overlaps(brows, bcols, sides, sides, 1): continue
      break
    colors = common.random_colors(num_boxes)
    colors = [color if color != 7 else 0 for color in colors]

  grid, output = common.grids(16, 16, 7)
  for row, col, length, color in zip(rows, cols, lengths, colors):
    common.rect(grid,
                2 * length - 1,
                2 * length - 1,
                row - length + 1,
                col - length + 1,
                color)
    new_length = length - 1
    if new_length == 0: new_length = 5
    common.rect(output,
                2 * new_length - 1,
                2 * new_length - 1,
                row - new_length + 1,
                col - new_length + 1,
                color)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[1, 4, 6, 10, 13], cols=[14, 4, 12, 14, 5],
               lengths=[2, 4, 2, 2, 3], colors=[4, 3, 6, 9, 1]),
      generate(rows=[2, 9, 10], cols=[13, 4, 11], lengths=[3, 5, 2],
               colors=[9, 6, 0]),
      generate(rows=[4, 5, 11, 13], cols=[1, 9, 2, 12], lengths=[2, 1, 2, 3],
               colors=[0, 5, 2, 8]),
      generate(rows=[4, 4, 12, 13], cols=[4, 11, 6, 13], lengths=[2, 1, 3, 2],
               colors=[5, 1, 8, 2]),
  ]
  test = [
      generate(rows=[1, 3, 3, 11, 13], cols=[1, 5, 12, 4, 13],
               lengths=[2, 2, 4, 1, 3], colors=[3, 1, 9, 0, 4]),
  ]
  return {"train": train, "test": test}
