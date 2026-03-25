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


def generate(size=None, length=None, bgcolor=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: The size of the grids.
    length: The length of the input border.
    bgcolor: The color of the border.
    colors: The colors of the pattern.
  """

  if size is None:
    size = common.randint(6, 24)
    length = common.randint(1, size // 2)
    bgcolor = common.random_color()
    num_colors = common.randint(2, min(4, size // 2))
    colors = common.random_colors(num_colors, exclude=[bgcolor])

  grid, output = common.grids(size, size, bgcolor)
  half = len(colors) // 2
  for r in range(size):
    for c in range(size):
      color = colors[(c + half * (r % 2) + 1) % len(colors)]
      output[r][c] = color
      if r + length >= size or c + length >= size: continue
      color = colors[(c + half * (r % 2)) % len(colors)]
      grid[r][c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=20, length=9, bgcolor=8, colors=[6, 3, 5, 7]),
      generate(size=8, length=1, bgcolor=1, colors=[5, 2]),
      generate(size=9, length=1, bgcolor=4, colors=[7, 6, 3]),
  ]
  test = [
      generate(size=6, length=1, bgcolor=3, colors=[6, 8]),
  ]
  return {"train": train, "test": test}
