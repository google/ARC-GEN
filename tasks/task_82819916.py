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


def generate(width=None, height=None, pattern=None, rows=None, lights=None,
             darks=None):
  """Returns input and output grids according to the given parameters.

  Args:
    width: the width of the input grid
    height: the height of the input grid
    pattern: a list of integers representing the pattern
    rows: a list of rows to place the colors
    lights: a list of "first" colors
    darks: a list of "second" colors
  """
  if width is None:
    width, height = 2 * common.randint(4, 5), 2 * common.randint(3, 7)
    while True:
      pattern = [common.randint(0, 1) for _ in range(width)]
      if len(set(pattern)) > 1: break
    rows, lights, darks, r = [], [], [], 1
    while r < height:
      colors = common.random_colors(2)
      rows.append(r)
      lights.append(colors[0])
      darks.append(colors[1])
      r += common.randint(2, 4)

  grid, output = common.grids(width, height)
  for idx, row in enumerate(rows):
    light, dark = lights[idx], darks[idx]
    colors_seen = set()
    for c in range(width):
      output[row][c] = dark if pattern[c] else light
      if idx > 0 and len(colors_seen) > 1: continue
      grid[row][c] = output[row][c]
      colors_seen.add(output[row][c])
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(width=8, height=10, pattern=[0, 0, 1, 0, 0, 1, 0, 0],
               rows=[1, 4, 6], lights=[3, 8, 1], darks=[2, 4, 6]),
      generate(width=8, height=10, pattern=[0, 0, 1, 0, 1, 0, 1, 1],
               rows=[1, 3, 7], lights=[2, 3, 8], darks=[1, 1, 2]),
      generate(width=8, height=12, pattern=[0, 1, 0, 1, 1, 0, 1, 0],
               rows=[1, 4, 6, 8], lights=[1, 2, 8, 6], darks=[4, 3, 2, 5]),
      generate(width=8, height=6, pattern=[0, 0, 1, 1, 1, 0, 1, 0],
               rows=[1, 4], lights=[3, 8], darks=[4, 2]),
  ]
  test = [
      generate(width=10, height=14, pattern=[0, 0, 1, 0, 1, 0, 1, 1, 0, 1],
               rows=[1, 3, 6, 9, 11], lights=[2, 8, 1, 6, 1],
               darks=[1, 3, 4, 8, 6]),
  ]
  return {"train": train, "test": test}
