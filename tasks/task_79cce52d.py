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


def generate(hoff=None, voff=None, colors=None):
  """Returns input and output grids according to the given parameters.

  Args:
    hoff: The horizontal offset.
    voff: The vertical offset.
    colors: A list of colors to use.
  """

  if colors is None:
    voff = common.randint(0, 5)
    hoff = common.randint(0, 5)
    colors = [0] * 36
    while True:
      length = common.randint(2, 5)
      off = common.randint(0, 6 - length)
      pos = common.randint(0, 5)
      cdir = common.randint(0, 1)
      color = common.choice([1, 3, 4, 5, 8, 9])
      for i in range(off, off + length):
        if cdir: colors[pos * 6 + i] = color
        else: colors[i * 6 + pos] = color
      if 0 in colors: continue
      if len(set(colors)) != 6: continue
      counts = [colors.count(c) for c in set(colors)]
      if min(counts) < 4: continue
      break
    colors = "".join(str(c) for c in colors)

  grid, output = common.grid(7, 7, 6), common.grid(6, 6)
  grid[0][0] = 7
  grid[0][hoff + 1] = grid[voff + 1][0] = 2
  for i, color in enumerate(colors):
    grid[1 + i // 6][1 + i % 6] = int(color)
    output[(i // 6 + voff) % 6][(i % 6 + hoff) % 6] = int(color)
  return {"input": grid, "output": output}


def validate():
  """Validates the generator."""
  train = [
      generate(hoff=0, voff=0, colors="888444988844933354939355999355111115"),
      generate(hoff=2, voff=2, colors="559988555981844981844991883331833311"),
      generate(hoff=3, voff=1, colors="355555335999334949114449114849118888"),
  ]
  test = [
      generate(hoff=1, voff=5, colors="553399555398133398114488114448114448"),
  ]
  return {"train": train, "test": test}
