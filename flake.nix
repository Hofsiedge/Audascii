{
  description = "A flake with Python 3.10 dev tools";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    self,
    nixpkgs,
    flake-utils,
    ...
  } @ inputs:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {
        inherit system;
        config.allowUnfree = true;
      };

      nixpkgsAlternative = package: alt:
        if (builtins.hasAttr package pkgs.python310Packages)
        then (abort "${package} is already in nixpkgs")
        else alt;

      asciinema = nixpkgsAlternative "asciinema" pkgs.python310Packages.buildPythonPackage rec {
        pname = "asciinema";
        version = "2.2.0";
        src = pkgs.python310Packages.fetchPypi {
          inherit version pname;
          sha256 = "XsXE5dMXS7fFWeRdtGgOuPpsQMBY+l5QBe6WodmXN7Q=";
        };
        propagatedBuildInputs = with pkgs.python310Packages; [setuptools wheel];
        format = "pyproject";
      };

      customPython = pkgs.python310.buildEnv.override {
        extraLibs =
          (with pkgs.python310Packages; [
            debugpy
            mypy
            jedi-language-server
            black # blue is better

            sounddevice
            soundfile
          ])
          ++ [asciinema];
      };
    in {
      devShells.default = pkgs.mkShell {
        buildInputs = with pkgs; [
          customPython
          alsa-utils
          audacity
          ffmpeg
        ];
      };
    });
}
