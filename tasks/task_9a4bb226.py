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


def generate(brows=None, bcols=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    colors: A list of colors to use.
  """

  if brows is None:
    colors = []
    # First, choose the 3-color box.
    subset = common.random_colors(3)
    while True:
      box = common.choices(subset, 9)
      if len(set(box)) == 3: break
    colors.extend(box)
    # Second, choose the 2-color box.
    for _ in range(3):
      subset = common.random_colors(2)
      while True:
        box = common.choices(subset, 9)
        if len(set(box)) == 2: break
      colors.extend(box)
    colors = "".join(str(c) for c in colors)
    # Third, choose the box locations.
    while True:
      brows = [common.randint(1, 11) for _ in range(4)]
      bcols = [common.randint(1, 11) for _ in range(4)]
      if not common.overlaps(brows, bcols, [3] * 4, [3] * 4, 1): break

  grid, output = common.grid(15, 15), common.grid(3, 3)
  for i, (brow, bcol) in enumerate(zip(brows, bcols)):
    for r in range(3):
      for c in range(3):
        grid[brow + r][bcol + c] = int(colors[i * 9 + r * 3 + c])
        if i == 0: output[r][c] = int(colors[i * 9 + r * 3 + c])
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(brows=[2, 4, 9, 10], bcols=[3, 8, 7, 3], colors="555688655999449499171717777322222323"),
      generate(brows=[6, 2, 2, 9], bcols=[8, 2, 8, 2], colors="133122132999889889744747744366333663"),
      generate(brows=[2, 1, 7, 9], bcols=[8, 2, 2, 8], colors="162611261755575577833338833944494449"),
  ]
  test = [
      generate(brows=[8, 1, 1, 6], bcols=[2, 2, 8, 8], colors="944444222366333636717177711885555558"),
  ]
  return {"train": train, "test": test}
