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

  if colors is None:
    four = common.random_colors(4)
    twenty = [four[0]] * 10 + [four[1]] * 6 + [four[2]] * 3 + [four[3]]
    colors = [common.choice(twenty) for _ in range(100)]
    pass

  grid, output = common.grids(10, 10)
  for i, color in enumerate(colors):
    grid[i // 10][i % 10] = color
  counts = {item: colors.count(item) for item in colors}
  i = 0
  for color, count in sorted(counts.items(), key=lambda p: p[1], reverse=True):
    for _ in range(count):
      output[9 - i % 10][i // 10] = color
      i += 1
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors=[4, 4, 8, 9, 4, 9, 4, 4, 9, 4,
                       4, 9, 4, 4, 5, 4, 4, 5, 9, 4,
                       5, 9, 9, 4, 5, 9, 4, 5, 9, 4,
                       5, 9, 4, 4, 5, 9, 4, 9, 4, 4,
                       5, 9, 4, 9, 4, 4, 4, 4, 5, 4,
                       5, 9, 4, 9, 4, 4, 9, 4, 5, 4,
                       5, 9, 4, 5, 4, 5, 9, 4, 4, 4,
                       5, 9, 4, 9, 4, 5, 9, 4, 4, 9,
                       5, 9, 4, 9, 4, 4, 9, 5, 4, 8,
                       4, 9, 4, 4, 9, 4, 9, 5, 4, 4]),
      generate(colors=[2, 6, 6, 6, 6, 5, 6, 6, 6, 6,
                       2, 6, 2, 6, 6, 5, 2, 6, 2, 6,
                       6, 5, 2, 6, 2, 5, 2, 5, 2, 2,
                       6, 6, 6, 6, 2, 5, 6, 5, 6, 2,
                       6, 2, 6, 6, 2, 6, 6, 6, 6, 2,
                       8, 2, 6, 5, 6, 6, 2, 8, 6, 8,
                       5, 2, 2, 5, 6, 6, 2, 6, 6, 8,
                       5, 2, 2, 5, 2, 6, 6, 6, 2, 6,
                       6, 2, 6, 6, 2, 8, 6, 5, 2, 6,
                       6, 2, 6, 6, 2, 8, 6, 5, 6, 6]),
  ]
  test = [
      generate(colors=[3, 3, 3, 3, 9, 3, 3, 8, 3, 8,
                       8, 2, 9, 3, 3, 8, 3, 8, 3, 8,
                       8, 2, 9, 8, 9, 8, 3, 3, 3, 8,
                       8, 3, 9, 8, 3, 8, 2, 8, 2, 3,
                       8, 3, 9, 8, 3, 9, 2, 8, 2, 9,
                       8, 3, 9, 8, 3, 9, 3, 3, 2, 9,
                       8, 3, 9, 3, 3, 3, 8, 3, 2, 9,
                       8, 3, 3, 3, 9, 3, 3, 3, 8, 9,
                       3, 3, 8, 3, 9, 3, 8, 3, 8, 9,
                       3, 3, 8, 3, 9, 3, 8, 3, 8, 9]),
  ]
  return {"train": train, "test": test}
