# SPDX-FileCopyrightText: 2024 Jan Schmitz <schmitz@num.uni-sb.de>
#
# SPDX-License-Identifier: AGPL-3.0-only
{
  inputs,
  cell,
}: let
  inherit (inputs) nixpkgs std;
  l = nixpkgs.lib // builtins;
in
  l.mapAttrs (_: std.lib.dev.mkShell) {
    std = {...}: {
      name = "epstein devshell";
      imports = [std.std.devshellProfiles.default];
      packages = with nixpkgs; cell.packages.epsteinlib.nativeBuildInputs ++ [git doxygen_gui neovim gcovr python3Packages.twine python3Packages.build];

      commands = [
        {
          name = "tests";
          command = "pushd $(git rev-parse --show-toplevel) &&
                     meson setup --reconfigure build -Db_coverage=true &&
                     meson compile -C build &&
                     meson test -v -C build
                     mkdir -p html && gcovr --html-details html/coverage.html &&
                     popd
                    ";
          help = "run the unit tests";
          category = "Testing";
        }
        {
          name = "format";
          command = "nix fmt";
          help = "format all files";
          category = "Tooling";
        }
        {
          name = "generate_python_stubs";
          command = "pushd $(git rev-parse --show-toplevel)/python &&
                     stubgen epsteinlib.pyx -o .out &&
                     mv .out/__main__.pyi epsteinlib.pyi &&
                     rm -r .out &&
                     nix fmt &&
                     popd";
          help = "regenerate the python stub files";
          category = "Tooling";
        }
        {
          name = "docs";
          command = "doxygen Doxyfile && ${nixpkgs.xdg-utils}/bin/xdg-open html/index.html";
          help = "generate and show documentation";
          category = "Tooling";
        }
        {
          name = "build_release";
          command = "rm -rf dist && pyproject-build --sdist";
          help = "Build release which creates dists folder";
          category = "Releasing";
        }
        {
          name = "testpypi_upload";
          command = "twine upload --repository testpypi dist/*";
          help = "Upload dist/* folder to https://tests.pypi.org";
          category = "Releasing";
        }
        {
          name = "testpypi_install";
          command = "python -m pip install --force -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ epsteinlib";
          help = "Install latest uploaded version from https://tests.pypi.org";
          category = "Releasing";
        }
      ];
    };
  }
