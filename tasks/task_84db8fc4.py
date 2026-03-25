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


def generate(colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: The colors of the pixels.
  """

  def draw():
    grid, output = common.grids(10, 10)
    queue = []
    for i, color in enumerate(colors):
      r, c = i // 10, i % 10
      output[r][c] = grid[r][c] = color
      if color == 0 and (r in [0, 9] or c in [0, 9]):
        output[r][c] = 2
        queue.append((r, c))
    while queue:
      r, c = queue.pop()
      for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if nr < 0 or nr >= 10 or nc < 0 or nc >= 10: continue
        if output[nr][nc] == 0:
          output[nr][nc] = 2
          queue.append((nr, nc))
    for row in range(10):
      for col in range(10):
        if output[row][col] == 0: output[row][col] = 5
    if len(set(common.flatten(output))) < 4: return None, None
    return grid, output

  if colors is None:
    while True:
      colors = common.choices([0, 1, 3], 100)
      grid, _ = draw()
      if grid: break

  grid, output = draw()
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[0, 3, 0, 3, 0, 0, 1, 3, 3, 1,
                       0, 1, 1, 1, 1, 3, 0, 0, 1, 1,
                       0, 3, 1, 0, 1, 0, 3, 0, 3, 0,
                       3, 3, 3, 0, 0, 3, 3, 3, 0, 0,
                       1, 1, 3, 1, 3, 0, 0, 0, 1, 0,
                       1, 0, 1, 0, 3, 0, 3, 3, 0, 3,
                       0, 0, 0, 0, 1, 1, 3, 0, 1, 0,
                       3, 0, 1, 3, 3, 1, 0, 3, 0, 0,
                       1, 1, 0, 0, 1, 3, 3, 1, 1, 3,
                       0, 0, 1, 1, 0, 1, 0, 0, 0, 0]),
      generate(colors=[0, 3, 3, 0, 3, 1, 0, 1, 1, 3,
                       1, 3, 0, 0, 1, 1, 3, 1, 0, 0,
                       1, 0, 1, 0, 0, 1, 3, 0, 3, 3,
                       0, 0, 3, 3, 1, 3, 3, 3, 0, 1,
                       0, 0, 3, 3, 0, 0, 0, 0, 3, 1,
                       3, 3, 0, 0, 3, 0, 0, 0, 3, 0,
                       0, 0, 3, 3, 3, 0, 3, 0, 3, 3,
                       3, 1, 1, 1, 3, 0, 1, 1, 1, 3,
                       0, 0, 1, 3, 1, 0, 0, 3, 3, 3,
                       0, 3, 3, 0, 3, 3, 1, 3, 1, 1]),
      generate(colors=[0, 0, 0, 0, 0, 0, 3, 1, 1, 3,
                       0, 0, 3, 1, 0, 1, 1, 0, 0, 3,
                       0, 1, 0, 0, 1, 3, 3, 1, 3, 1,
                       0, 1, 3, 0, 0, 0, 0, 0, 1, 0,
                       0, 1, 3, 1, 0, 1, 0, 3, 0, 1,
                       1, 0, 0, 3, 1, 3, 1, 0, 1, 0,
                       1, 0, 0, 3, 0, 1, 0, 3, 0, 0,
                       0, 1, 0, 1, 1, 0, 3, 1, 0, 3,
                       0, 3, 1, 1, 3, 0, 0, 3, 1, 0,
                       1, 1, 3, 3, 0, 0, 1, 3, 0, 3]),
      generate(colors=[3, 1, 0, 3, 3, 3, 3, 3, 0, 3,
                       1, 0, 0, 3, 3, 0, 1, 3, 1, 1,
                       0, 1, 1, 1, 0, 3, 0, 0, 0, 3,
                       0, 1, 3, 3, 0, 3, 1, 3, 0, 0,
                       1, 3, 1, 1, 0, 1, 3, 0, 0, 0,
                       0, 1, 1, 3, 0, 0, 3, 1, 1, 3,
                       3, 0, 1, 0, 0, 0, 0, 0, 3, 0,
                       0, 0, 0, 3, 3, 1, 0, 0, 1, 3,
                       3, 3, 1, 0, 0, 1, 1, 0, 0, 1,
                       0, 1, 3, 0, 1, 1, 1, 1, 1, 3]),
  ]
  test = [
      generate(colors=[1, 0, 0, 1, 0, 1, 1, 1, 1, 3,
                       0, 0, 0, 3, 0, 3, 0, 1, 0, 0,
                       0, 1, 0, 3, 3, 0, 1, 3, 3, 3,
                       3, 1, 3, 1, 1, 0, 3, 3, 0, 1,
                       1, 1, 3, 0, 1, 3, 0, 1, 1, 0,
                       0, 3, 0, 1, 3, 0, 1, 1, 0, 3,
                       1, 1, 3, 0, 0, 3, 0, 3, 3, 3,
                       3, 1, 1, 1, 1, 3, 1, 0, 3, 1,
                       3, 0, 0, 0, 3, 3, 1, 0, 1, 1,
                       1, 0, 3, 1, 1, 0, 0, 0, 1, 0]),
  ]
  return {"train": train, "test": test}
