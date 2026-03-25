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
    colors = ""
    counts = common.shuffle(common.sample(range(10), 9))
    for count in counts:
      pixels = common.sample([(0, 0), (0, 1), (0, 2),
                              (1, 0), (1, 1), (1, 2),
                              (2, 0), (2, 1), (2, 2)], count)
      for r in range(3):
        for c in range(3):
          colors += "1" if (r, c) in pixels else "2"

  grid, output = common.grids(11, 11)
  blue_to_groups = {}
  for gr in range(3):
    for gc in range(3):
      blues = 0
      for r in range(3):
        for c in range(3):
          color = int(colors[gr * 27 + gc * 9 + r * 3 + c])
          grid[4 * gr + r][4 * gc + c] = color
          if color == 1: blues += 1
      blue_to_groups[blues] = 3 * gr + gc
  for i, blues in enumerate(sorted(blue_to_groups.keys())):
    group = blue_to_groups[blues]
    for r in range(3):
      for c in range(3):
        color = int(colors[group * 9 + r * 3 + c])
        output[4 * (2 - i // 3) + r][4 * (i % 3) + c] = color
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(colors="112212122212212122211111112121211122111111121222212222122221222121211121111111111"),
      generate(colors="221122222222222122121112212221122212212121221222222222211121121111111121111211112"),
      generate(colors="222221222222222222221122212211121212111111111111211121211121211121121222211111111"),
  ]
  test = [
      generate(colors="222122212212122212221121212112121121111111111111112111211111112211121122222222222"),
  ]
  return {"train": train, "test": test}
