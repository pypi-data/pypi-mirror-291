{
  lib,
  makesLib,
  nixpkgs,
  python_pkgs,
  python_version,
}: let
  raw_src = builtins.fetchGit {
    url = "https://gitlab.com/dmurciaatfluid/purity";
    rev = "bc2621cb8b330474edc2d36407fc5a7e0b0db09c";
    ref = "refs/tags/v2.0.0";
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
            inherit (default.python_pkgs) types-simplejson;
          }
        )
      )
  )
