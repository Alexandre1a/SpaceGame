{
  description = "General Python dev environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs {
          inherit system;
          config.allowUnfree = true;
        };

        python = pkgs.python314;
      in
      {
        devShells.default = pkgs.mkShell {
          name = "python";

          packages = with pkgs; [
            python
	          python.pkgs.pygame
          ];

          shellHook = ''
            echo "Python loaded"
          '';
        };
      });
}
