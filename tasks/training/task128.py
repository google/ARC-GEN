# Copyright 2025 Google LLC
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


def generate(cols=None, wides=None, talls=None, colors=None, size=15, boxes=3):
  """Returns input and output grids according to the given parameters.

  Args:
    cols: a list of horizontal coordinates where pixels should be placed
    wides: a list of box widths
    talls: a list of box heights
    colors: a list of colors to be used
    size: the width and height of the (square) grid
    boxes: the number of boxes to be placed
  """
  if cols is None:
    while True:
      wides = [common.randint(1, 5) for _ in range(boxes)]
      cols = [common.randint(0, size - wide) for wide in wides]
      if not common.overlaps(cols, cols, wides, wides, 1): break
    talls = [common.randint(1, 7) for _ in range(boxes)]
    colors = common.shuffle([1, 2, 4])

  grid, output = common.grids(size, size)
  for col, wide, tall, color in zip(cols, wides, talls, colors):
    for r in range(size - tall, size):
      for c in range(col, col + wide):
        grid[r][c] = color
        output[r - tall][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(cols=[1, 4, 9], wides=[2, 4, 4], talls=[4, 2, 4],
               colors=[1, 2, 4]),
      generate(cols=[1, 7, 11], wides=[4, 2, 2], talls=[6, 2, 5],
               colors=[4, 1, 2]),
      generate(cols=[1, 7, 11], wides=[4, 1, 2], talls=[1, 4, 3],
               colors=[2, 1, 4]),
  ]
  test = [
      generate(cols=[0, 5, 10], wides=[4, 3, 5], talls=[7, 6, 3],
               colors=[2, 4, 1]),
  ]
  return {"train": train, "test": test}
