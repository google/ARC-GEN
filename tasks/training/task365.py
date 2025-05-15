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


def generate(wides=None, talls=None, rows=None, cols=None, colors=None,
             size=10):
  """Returns input and output grids according to the given parameters.

  Args:
    wides: a list of box widths
    talls: a list of box heights
    rows: a list of vertical coordinates where boxes should be placed
    cols: a list of horizontal coordinates where boxes should be placed
    colors: a list of digits representing the colors to be used
    size: the width and height of the (square) grid
  """
  if wides is None:
    num_boxes = min(3, common.randint(2, 5))
    # Choose nonoverlapping locations for the boxes.
    while True:
      wides = [common.randint(3, 6) for _ in range(num_boxes)]
      talls = [common.randint(3, 6) for _ in range(num_boxes)]
      rows = [common.randint(0, size - tall) for tall in talls]
      cols = [common.randint(0, size - wide) for wide in wides]
      if not common.overlaps(rows, cols, wides, talls, 1): break
    num_reds = sorted(common.sample(range(1, 5), num_boxes), reverse=True)
    # Fill the boxes with blue/cyan, then sprinkle the requisite number of reds.
    colors = []
    for idx in range(num_boxes):
      wide, tall, num_red = wides[idx], talls[idx], num_reds[idx]
      pixels = [common.choice([1, 8]) for _ in range(wide * tall)]
      reds = common.sample(range(wide * tall), num_red)
      for red in reds:
        pixels[red] = common.red()
      colors.extend(pixels)

  grid, output = common.grid(size, size), common.grid(wides[0], talls[0])
  i = 0
  for idx in range(len(wides)):
    wide, tall, row, col = wides[idx], talls[idx], rows[idx], cols[idx]
    for r in range(tall):
      for c in range(wide):
        grid[row + r][col + c] = colors[i]
        if not idx: output[r][c] = colors[i]
        i += 1
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(wides=[4, 4, 6], talls=[5, 4, 4], rows=[0, 1, 6], cols=[6, 1, 3],
               colors=[8, 8, 8, 8, 8, 2, 2, 8, 8, 8, 8, 8, 8, 2, 1, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 1, 8, 8, 8, 8, 2, 8, 8, 8, 8, 8, 8, 8,
                       8, 8, 8, 8, 8, 8, 8, 2, 8, 8, 8, 2, 8, 1, 8, 8, 8, 1, 8,
                       8, 8, 8]),
      generate(wides=[3, 4, 5], talls=[3, 5, 7], rows=[7, 0, 1], cols=[1, 0, 5],
               colors=[8, 2, 2, 2, 2, 1, 2, 1, 8, 1, 1, 1, 8, 1, 8, 1, 1, 8, 2,
                       8, 1, 1, 1, 1, 8, 8, 1, 8, 8, 1, 8, 8, 1, 8, 8, 1, 8, 2,
                       8, 8, 8, 8, 8, 1, 8, 1, 2, 8, 2, 8, 8, 8, 1, 8, 1, 1, 8,
                       1, 8, 8, 1, 1, 8, 2]),
      generate(wides=[4, 4], talls=[6, 6], rows=[0, 3], cols=[0, 6],
               colors=[2, 8, 8, 8, 8, 8, 1, 8, 1, 8, 8, 8, 8, 8, 8, 2, 8, 2, 8,
                       1, 8, 1, 8, 8, 1, 8, 8, 2, 8, 8, 1, 8, 8, 2, 8, 8, 8, 8,
                       8, 1, 1, 8, 8, 8, 8, 8, 1, 8]),
  ]
  test = [
      generate(wides=[3, 4, 4], talls=[6, 4, 3], rows=[1, 0, 6], cols=[6, 0, 1],
               colors=[2, 8, 1, 8, 8, 8, 2, 1, 8, 8, 8, 2, 2, 8, 1, 1, 8, 8, 2,
                       8, 8, 8, 8, 8, 1, 8, 1, 2, 8, 1, 8, 8, 8, 8, 1, 2, 8, 2,
                       8, 8, 1, 8, 1, 2, 8, 1]),
  ]
  return {"train": train, "test": test}
