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


def generate(size=None, idxs=None, colors=(6, 2, 1, 7)):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
    idxs: a list of indices into the colors list
    colors: a list of colors to be used for the pixels
  """
  if size is None:
    size = common.randint(3, 9)
    idxs = [common.choice(range(len(colors))) for _ in range(size * size)]

  grid = []
  for r in range(size):
    grid.append([colors[idxs[r * size + c]] for c in range(size)])
  output = [row[::-1] for row in grid]
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=4, idxs=[0, 0, 0, 1,
                             0, 2, 0, 1,
                             3, 1, 3, 1,
                             2, 3, 1, 1]),
      generate(size=7, idxs=[3, 3, 3, 0, 0, 0, 1,
                             0, 3, 2, 2, 3, 3, 2,
                             3, 3, 1, 2, 1, 0, 0,
                             1, 1, 3, 3, 3, 1, 1,
                             3, 1, 3, 2, 1, 3, 1,
                             0, 0, 0, 1, 1, 2, 2,
                             0, 1, 0, 0, 0, 0, 0]),
      generate(size=6, idxs=[2, 1, 3, 2, 2, 2,
                             1, 2, 3, 3, 1, 0,
                             1, 2, 1, 0, 1, 2,
                             2, 1, 2, 3, 0, 1,
                             1, 3, 2, 1, 3, 2,
                             1, 2, 0, 1, 3, 3]),
  ]
  test = [
      generate(size=3, idxs=[3, 0, 2,
                             0, 3, 0,
                             0, 1, 1]),
  ]
  return {"train": train, "test": test}
