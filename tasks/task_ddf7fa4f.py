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


def generate(rows=None, cols=None, wides=None, talls=None, lights=None,
             colors=None, size=10, num_lights=3):
  """Returns input and output grids according to the given parameters.

  Args:
    rows: a list of vertical coordinates where pixels should be placed
    cols: a list of horizontal coordinates where pixels should be placed
    wides: a list of box widths
    talls: a list of box heights
    lights: a list of light locations
    colors: a list of colors to be used
    size: the width and height of the (square) grid
    num_lights: the number of lights
  """
  if rows is None:
    colors = common.random_colors(3, exclude=[common.gray()])
    lights = [common.randint(0, 2), common.randint(4, 5), common.randint(7, 9)]
    while True:
      wides = [common.randint(2, 5) for _ in range(num_lights)]
      talls = [common.randint(2, 7) for _ in range(num_lights)]
      rows = [common.randint(2, size - tall) for tall in talls]
      cols = [common.randint(0, size - wide) for wide in wides]
      if len(set(rows)) == 1: continue  # Boxes need to have different rows.
      overlaps = False
      for j in range(num_lights):
        for i in range(num_lights):
          under = cols[j] <= lights[i] and cols[j] + wides[j] > lights[i]
          overlaps = overlaps or (under != (i == j))  # Only under right light.
        for i in range(j):
          if rows[i] + talls[i] < rows[j] or rows[j] + talls[j] < rows[i]:
            continue
          if cols[i] + wides[i] < cols[j] or cols[j] + wides[j] < cols[i]:
            continue
          overlaps = True
      if not overlaps: break

  grid, output = common.grids(size, size)
  for light, color in zip(lights, colors):
    output[0][light] = grid[0][light] = color
  for row, col, wide, tall, color in zip(rows, cols, wides, talls, colors):
    for r in range(row, row + tall):
      for c in range(col, col + wide):
        grid[r][c] = common.gray()
        output[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(rows=[4, 2, 7], cols=[1, 4, 7], wides=[2, 4, 3], talls=[5, 4, 3],
               lights=[2, 5, 9], colors=[2, 6, 8]),
      generate(rows=[2, 7, 2], cols=[0, 3, 7], wides=[4, 4, 3], talls=[4, 2, 4],
               lights=[1, 5, 8], colors=[1, 4, 7]),
      generate(rows=[2, 5, 3], cols=[1, 3, 7], wides=[2, 3, 3], talls=[3, 3, 2],
               lights=[1, 5, 8], colors=[1, 6, 7]),
  ]
  test = [
      generate(rows=[7, 2, 2], cols=[0, 2, 8], wides=[4, 5, 2], talls=[2, 4, 7],
               lights=[0, 4, 8], colors=[3, 6, 9]),
  ]
  return {"train": train, "test": test}
