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


def generate(width=None, height=None, colors=None, rows=None, cols=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    colors: a list of colors to be used
    rows: a list of vertical coordinates where straightaways should be placed
    cols: a list of horizontal coordinates where straightaways should be placed
  """
  if rows is None:
    width, height = common.randint(10, 30), common.randint(10, 30)
    rows = common.sample(range(1, height - 1), common.randint(0, 3))
    cols = common.sample(range(1, width - 1), common.randint(0, 3))
    color = common.random_color(exclude=[common.red()])
    # Create static, but ensure that all rows and cols have it.
    while True:
      colors = []
      for _ in range(height):
        for _ in range(width):
          colors.append(common.black() if not common.randint(0, 4) else color)
      legal = True
      for r in range(height):
        if len(set([colors[r * width + c] for c in range(width)])) < 2:
          legal = False
      for c in range(width):
        if len(set([colors[r * width + c] for r in range(height)])) < 2:
          legal = False
      if legal: break
    # Draw lines
    for r in range(height):
      for c in range(width):
        if r in rows or c in cols: colors[r * width + c] = common.black()

  grid, output = common.grids(width, height)
  for r in range(height):
    for c in range(width):
      output[r][c] = grid[r][c] = colors[r * width + c]
      output[r][c] = common.red() if r in rows or c in cols else output[r][c]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
     generate(width=19, height=12,
              colors=[1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 1,
                      1, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1,
                      1, 1, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0,
                      1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
                      1, 1, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1,
                      1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0,
                      1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1,
                      1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 1,
                      1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 1],
              rows=[8], cols=[8]),
     generate(width=14, height=12,
              colors=[8, 8, 8, 8, 0, 8, 8, 8, 8, 8, 0, 0, 8, 8, 0, 8, 0, 0, 0,
                      0, 8, 8, 8, 8, 0, 8, 8, 8, 8, 8, 0, 8, 0, 8, 8, 8, 8, 8,
                      0, 0, 8, 8, 8, 0, 8, 8, 0, 8, 8, 0, 0, 8, 0, 8, 8, 0, 8,
                      8, 8, 8, 0, 8, 8, 0, 0, 0, 0, 8, 8, 8, 8, 8, 8, 0, 0, 8,
                      8, 0, 8, 0, 0, 8, 8, 8, 8, 0, 8, 8, 0, 8, 8, 8, 8, 8, 0,
                      0, 0, 8, 8, 8, 0, 0, 0, 8, 0, 0, 8, 8, 0, 0, 8, 8, 8, 0,
                      0, 8, 0, 8, 8, 8, 0, 8, 0, 8, 8, 8, 8, 8, 0, 8, 0, 8, 8,
                      8, 8, 8, 0, 0, 8, 0, 0, 8, 0, 8, 0, 0, 0, 0, 0, 0, 0, 8,
                      0, 8, 8, 8, 8, 8, 0, 8, 8, 8, 8, 8, 0, 0, 8, 0],
              rows=[], cols=[4, 10]),
     generate(width=15, height=17,
              colors=[3, 0, 3, 3, 3, 3, 3, 0, 3, 3, 3, 0, 3, 0, 3, 3, 0, 3, 0,
                      3, 3, 3, 0, 3, 0, 3, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 3, 0, 0, 3, 3, 0, 3, 0, 3,
                      3, 0, 0, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3,
                      0, 3, 3, 3, 3, 3, 3, 0, 0, 3, 3, 0, 3, 3, 0, 0, 3, 0, 3,
                      0, 3, 0, 3, 0, 0, 3, 3, 3, 0, 3, 0, 0, 3, 3, 3, 0, 0, 3,
                      0, 3, 3, 0, 0, 3, 3, 0, 3, 3, 3, 3, 3, 0, 3, 3, 3, 3, 3,
                      0, 3, 3, 0, 0, 3, 3, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 3, 0,
                      3, 3, 3, 3, 3, 3, 0, 3, 3, 3, 0, 3, 3, 3, 0, 3, 3, 3, 0,
                      3, 0, 0, 3, 0, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 3, 0, 3, 0, 0, 3, 0, 3, 3, 0, 3, 3, 3, 3,
                      0, 3, 0, 0, 3, 0, 3, 3, 0, 3, 0, 3, 3, 0, 0, 3, 3, 0, 0,
                      3, 3, 3, 3, 3, 0, 3, 3, 0, 0, 3, 3, 0, 0, 3, 3, 0, 3, 3,
                      0, 0, 3, 0, 3, 0, 3, 0],
              rows=[2, 12], cols=[1]),
  ]
  test = [
     generate(width=25, height=27,
              colors=[4, 0, 4, 0, 4, 4, 0, 0, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 0,
                      4, 4, 0, 4, 0, 0, 4, 4, 4, 0, 0, 4, 0, 4, 4, 0, 4, 4, 4,
                      4, 4, 4, 0, 4, 4, 4, 4, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4,
                      0, 4, 4, 4, 0, 0, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 4,
                      4, 0, 4, 4, 0, 4, 4, 0, 4, 4, 4, 0, 0, 0, 0, 4, 4, 4, 4,
                      0, 4, 4, 4, 0, 4, 4, 0, 4, 4, 4, 4, 4, 4, 0, 4, 4, 0, 4,
                      4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 4, 0, 4, 0, 4, 0, 4, 4, 0,
                      0, 4, 0, 4, 0, 4, 4, 4, 4, 4, 4, 0, 4, 0, 4, 4, 4, 0, 4,
                      0, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 4, 0, 4, 0, 0, 4, 4, 0,
                      0, 4, 4, 4, 0, 0, 0, 0, 4, 0, 0, 4, 4, 0, 4, 4, 0, 4, 4,
                      0, 4, 4, 0, 4, 4, 0, 0, 4, 0, 4, 0, 0, 4, 0, 4, 4, 4, 4,
                      0, 4, 4, 0, 0, 4, 4, 4, 4, 4, 0, 0, 4, 0, 4, 4, 4, 0, 0,
                      4, 4, 4, 4, 0, 4, 4, 4, 0, 0, 4, 0, 4, 4, 0, 4, 4, 0, 4,
                      4, 0, 4, 4, 0, 0, 0, 0, 4, 4, 4, 0, 4, 0, 0, 0, 4, 4, 4,
                      0, 4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 0, 4, 4, 4, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 4, 4, 4, 4, 0, 4, 4, 0, 0,
                      4, 4, 4, 4, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4,
                      0, 4, 0, 4, 4, 0, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 4, 4, 4,
                      0, 0, 4, 0, 4, 0, 0, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 4, 0,
                      4, 0, 4, 4, 4, 4, 4, 0, 4, 4, 4, 4, 4, 0, 4, 0, 4, 4, 0,
                      4, 4, 4, 0, 4, 4, 0, 0, 4, 4, 4, 4, 0, 0, 4, 4, 4, 0, 4,
                      0, 4, 0, 4, 4, 4, 4, 4, 4, 0, 0, 4, 4, 4, 4, 4, 0, 4, 4,
                      0, 0, 4, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 0, 0, 0,
                      4, 4, 0, 4, 4, 4, 0, 4, 4, 0, 4, 4, 4, 0, 4, 4, 4, 0, 4,
                      4, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                      0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 4, 0, 4, 0,
                      4, 0, 4, 4, 4, 0, 0, 0, 0, 4, 0, 4, 4, 4, 0, 4, 4, 4, 0,
                      4, 4, 4, 4, 4, 0, 4, 0, 4, 0, 4, 4, 0, 4, 4, 0, 4, 4, 0,
                      4, 0, 4, 4, 4, 4, 4, 4, 4, 4, 4, 0, 4, 4, 0, 0, 0, 0, 4,
                      4, 4, 0, 0, 4, 4, 4, 0, 4, 4, 0, 4, 0, 4, 0, 4, 4, 0, 4,
                      0, 0, 0, 4, 4, 4, 4, 4, 0, 4, 0, 4, 4, 0, 0, 4, 0, 4, 4,
                      0, 4, 0, 4, 0, 0, 4, 0, 4, 4, 0, 4, 4, 0, 0, 0, 4, 0, 4,
                      0, 4, 4, 4, 4, 0, 0, 4, 4, 4, 0, 4, 0, 4, 4, 4, 4, 4, 0,
                      4, 4, 4, 4, 0, 0, 0, 4, 4, 4],
              rows=[2, 12, 20], cols=[6, 21]),
  ]
  return {"train": train, "test": test}
