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


def generate(width=None, height=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: The width of the input grid.
    height: The height of the input grid.
    colors: A list of colors to use.
  """

  color_map = {1: 1, 2: 2, 3: 3, 4: 7}
  box_choices = [3] + [4] * 2 + [5] * 3 + [6] * 4 + [7] * 3 + [8] * 2 + [9]
  cell_choices = [4] * 16 + [3] * 9 + [2] * 4 + [1]
  pixel_choices = [1] * 9 + [2]

  if width is None:
    base = common.randint(17, 18)
    width, height = base + common.randint(-1, 1), base + common.randint(-1, 1)
    num_boxes = common.randint(4, 6)
    while True:
      wides = [common.choice(box_choices) for _ in range(num_boxes)]
      talls = [common.choice(box_choices) for _ in range(num_boxes)]
      brows = [common.randint(0, height - tall) for tall in talls]
      bcols = [common.randint(0, width - wide) for wide in wides]
      if not common.overlaps(brows, bcols, wides, talls, 1): break
    grid = common.grid(width, height)
    for wide, tall, brow, bcol in zip(wides, talls, brows, bcols):
      while True:
        cells = common.choice(cell_choices)
        ws = [(1 if wide == 3 else common.choice(pixel_choices)) for _ in range(cells)]
        ts = [(1 if tall == 3 else common.choice(pixel_choices)) for _ in range(cells)]
        rs = [common.randint(1, tall - 1 - t) for t in ts]
        cs = [common.randint(1, wide - 1 - w) for w in ws]
        if not common.overlaps(rs, cs, ws, ts, 1): break
      common.rect(grid, wide, tall, brow, bcol, color_map[cells])
      for w, t, r, c in zip(ws, ts, rs, cs):
        common.rect(grid, w, t, brow + r, bcol + c, 0)
    colors = common.flatten(grid)

  grid, output = common.grids(width, height)
  for i, color in enumerate(colors):
    output[i // width][i % width] = color
    grid[i // width][i % width] = 8 if color else 0
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=17, height=17,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 3, 3, 3, 3, 3, 0,
                       0, 0, 2, 0, 0, 2, 0, 2, 0, 0, 0, 3, 0, 3, 3, 3, 0,
                       0, 0, 2, 0, 0, 2, 2, 2, 0, 0, 0, 3, 3, 3, 0, 3, 0,
                       0, 0, 2, 2, 2, 2, 2, 2, 0, 0, 0, 3, 0, 3, 3, 3, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0,
                       0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0, 1, 1, 1, 1, 0, 0,
                       0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 1, 0, 0, 1, 0, 0,
                       0, 0, 0, 0, 0, 2, 2, 0, 2, 0, 0, 1, 1, 1, 1, 0, 0,
                       0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0, 1, 1, 1, 1, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 2, 2, 2, 2, 2, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 0,
                       0, 2, 2, 2, 0, 2, 0, 0, 0, 7, 0, 7, 7, 7, 0, 7, 0,
                       0, 2, 0, 2, 2, 2, 0, 0, 0, 7, 7, 7, 0, 7, 0, 7, 0,
                       0, 2, 2, 2, 2, 2, 0, 0, 0, 7, 0, 7, 7, 7, 7, 7, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 0]),
      generate(width=17, height=19,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 1, 1, 1, 0, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0,
                       0, 1, 1, 1, 0, 3, 3, 3, 3, 3, 0, 3, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 3, 0, 3, 3, 3, 0, 3, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 3, 3, 3, 0, 3, 3, 3, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0,
                       0, 0, 0, 1, 1, 1, 1, 0, 0, 2, 0, 0, 2, 0, 0, 2, 0,
                       0, 0, 0, 1, 1, 1, 1, 0, 0, 2, 2, 2, 2, 2, 2, 2, 0,
                       0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0,
                       0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 2, 0, 0, 2, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 2, 2, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 2, 2, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
      generate(width=16, height=17,
               colors=[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 3, 0, 0, 3, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 3, 0, 0, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 0, 0,
                       0, 3, 3, 3, 3, 0, 3, 0, 3, 0, 0, 3, 0, 3, 0, 0,
                       0, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3, 3, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 0, 0, 3, 3, 0, 0,
                       0, 0, 7, 7, 7, 7, 7, 0, 3, 3, 3, 3, 3, 3, 0, 0,
                       0, 0, 7, 0, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 7, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 7, 7, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 7, 0, 7, 7, 7, 0, 0, 0, 7, 7, 7, 7, 7, 7,
                       0, 0, 7, 7, 7, 7, 7, 0, 0, 0, 7, 0, 7, 0, 7, 7,
                       0, 0, 7, 7, 0, 0, 7, 0, 0, 0, 7, 7, 7, 7, 7, 7,
                       0, 0, 7, 7, 7, 7, 7, 0, 0, 0, 7, 0, 7, 0, 0, 7,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7]),
  ]
  test = [
      generate(width=18, height=17,
               colors=[0, 0, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 2, 0, 2, 0, 2, 0, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0,
                       0, 0, 2, 0, 2, 2, 2, 0, 3, 0, 3, 3, 0, 0, 3, 0, 0, 0,
                       0, 0, 2, 2, 2, 2, 2, 0, 3, 3, 3, 3, 0, 0, 3, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 3, 3, 3, 3, 0, 0, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0,
                       0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                       0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 0,
                       0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 7, 0, 0, 7, 7, 7, 7, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 0, 0, 7, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 0, 0, 7, 0,
                       0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 7, 0, 7, 7, 7, 7, 7, 0,
                       0, 2, 0, 0, 2, 2, 2, 2, 0, 0, 7, 0, 7, 7, 7, 7, 7, 0,
                       0, 2, 0, 0, 2, 2, 2, 2, 0, 0, 7, 7, 7, 0, 0, 7, 7, 0,
                       0, 2, 2, 2, 2, 0, 2, 2, 0, 0, 7, 7, 7, 0, 0, 7, 7, 0,
                       0, 2, 2, 2, 2, 2, 2, 2, 0, 0, 7, 7, 7, 7, 7, 7, 7, 0,
                       0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
  ]
  return {"train": train, "test": test}
