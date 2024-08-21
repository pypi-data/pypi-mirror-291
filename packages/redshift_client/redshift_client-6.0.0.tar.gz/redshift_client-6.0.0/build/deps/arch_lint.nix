{
  lib,
  makesLib,
  nixpkgs,
  python_pkgs,
  python_version,
}: let
  raw_src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/arch_lint";
    rev = "ae3f276eb43062e1c8841a24f277bafc082e7f78";
    ref = "refs/tags/v4.0.0";
  };
  src = import "${raw_src}/build/filter.nix" nixpkgs.nix-filter raw_src;
  bundle = import "${raw_src}/build" {
    inherit makesLib nixpkgs python_version src;
  };
in
  bundle.build_bundle (
    default: required_deps: builder:
      builder lib (
        required_deps (
          python_pkgs
          // {
            inherit (default.python_pkgs) grimp;
          }
        )
      )
  )
