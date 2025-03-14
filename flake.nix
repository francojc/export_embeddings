{
  description = "A Nix flake for creating a Python environment";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-23.11-darwin";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = {
    nixpkgs,
    flake-utils,
    ...
  }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs {inherit system;};

      packages = with pkgs; [
        pandoc
        quarto
      ];

      # Python environment with packages
      python = pkgs.python3.withPackages pythonPackages;

      # Python packages
      pythonPackages = ps:
        with ps; [
          fasttext
          gensim
          ipython
          jupyter
          numpy
          tqdm
        ];

      allPackages = packages ++ [python];
    in {
      devShell = pkgs.mkShell {
        buildInputs = allPackages;
        shellHook = ''
          # Add the current python to the path
          export PATH=$python/bin:$PATH
        '';
      };
    });
}
