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


def generate(size=None):
  """Returns input and output grids according to the given parameters.

  Args:
    size: the width and height of the (square) grid
  """
  if size is None:
    size = common.randint(5, 20)

  grid, output = common.grids(size, size)
  r, c, rdir, cdir = 0, 0, 0, 1
  while True:
    if output[r][c] == common.green(): break
    if r + rdir >= 0 and r + rdir < size and c + cdir >= 0 and c + cdir < size:
      if output[r + rdir][c + cdir] == common.green(): break
    output[r][c] = common.green()
    if cdir == 1 and c + 1 == size:
      rdir, cdir = 1, 0
    if cdir == 1 and c + 2 < size and output[r][c + 2] == common.green():
      rdir, cdir = 1, 0
    elif rdir == 1 and r + 1 == size:
      rdir, cdir = 0, -1
    elif rdir == 1 and r + 2 < size and output[r + 2][c] == common.green():
      rdir, cdir = 0, -1
    elif cdir == -1 and c == 0:
      rdir, cdir = -1, 0
    elif cdir == -1 and c - 2 >= 0 and output[r][c - 2] == common.green():
      rdir, cdir = -1, 0
    elif rdir == -1 and output[r - 2][c] == common.green():
      rdir, cdir = 0, 1
    c += cdir
    r += rdir
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(size=6),
      generate(size=8),
      generate(size=15),
      generate(size=13),
      generate(size=10),
  ]
  test = [
      generate(size=18),
  ]
  return {"train": train, "test": test}
