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


def generate(width=None, height=None, brows=None, bcols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the grid.
    height: The height of the grid.
    brows: The rows of the boxes.
    bcols: The columns of the boxes.
    colors: The colors of the grid.
  """

  if width is None:
    width, height = common.randint(7, 14), common.randint(7, 14)
    num_boxes = 1
    if width * height > 70: num_boxes = 2
    if width * height > 100: num_boxes = 3
    if width * height > 130: num_boxes = 4
    while True:
      brows = [common.randint(1, height - 4) for _ in range(num_boxes)]
      bcols = [common.randint(1, width - 4) for _ in range(num_boxes)]
      if not common.overlaps(brows, bcols, [3] * num_boxes, [3] * num_boxes, 1):
        break
    colors = []
    for _ in range(num_boxes):
      pair = common.random_colors(2)
      while True:
        values = [common.randint(0, 1) for _ in range(9)]
        if sum(values) >= 2 and sum(values) <= 7: break
      colors.extend([pair[value] for value in values])

  grid, output = common.grids(width, height)
  for i, (brow, bcol) in enumerate(zip(brows, bcols)):
    pair = list(set([int(c) for c in colors[i*9:(i+1)*9]]))
    for r in range(3):
      for c in range(3):
        color = int(colors[i * 9 + r * 3 + c])
        grid[brow + r][bcol + c] = color
        output[brow + r][bcol + c] = pair[0] if pair[1] == color else pair[1]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=7, height=7, brows=[1], bcols=[1], colors="585585888"),
      generate(width=10, height=13, brows=[1, 4, 8], bcols=[1, 6, 2],
               colors="884484884322332322363363333"),
      generate(width=12, height=12, brows=[1, 2, 6, 8], bcols=[1, 7, 3, 8],
               colors="111818888323222232611166166445455555"),
  ]
  test = [
      generate(width=9, height=8, brows=[1, 4], bcols=[1, 5],
               colors="322332322666111166"),
  ]
  return {"train": train, "test": test}
