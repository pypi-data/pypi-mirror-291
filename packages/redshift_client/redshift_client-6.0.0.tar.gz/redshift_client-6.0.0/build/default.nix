{
  makesLib,
  nixpkgs,
  python_version,
  src,
}: let
  deps = import ./deps {
    inherit makesLib nixpkgs python_version;
  };
  build_required_deps = python_pkgs: {
    runtime_deps = with python_pkgs; [
      boto3
      deprecated
      fa-purity
      psycopg2
      mypy-boto3-redshift
      types-boto3
      types-deprecated
      types-psycopg2
    ];
    build_deps = with python_pkgs; [flit-core];
    test_deps = with python_pkgs; [
      arch-lint
      mypy
      pytest
      pylint
    ];
  };
  publish = nixpkgs.mkShell {
    packages = [
      nixpkgs.git
      deps.python_pkgs.flit
    ];
  };
  bundle_builder = lib: pkgDeps:
    makesLib.makePythonPyprojectPackage {
      inherit (lib) buildEnv buildPythonPackage;
      inherit pkgDeps src;
    };
  build_bundle = builder:
  # builder: Deps -> (PythonPkgs -> PkgDeps) -> (Deps -> PkgDeps -> Bundle) -> Bundle
  # Deps: are the default project dependencies
  # PythonPkgs -> PkgDeps: is the required dependencies builder
  # Deps -> PkgDeps -> Bundle: is the bundle builder
    builder deps build_required_deps bundle_builder;
  bundle = build_bundle (default: required_deps: builder: builder default.lib (required_deps default.python_pkgs));
  dev_shell = import ./dev_env {
    inherit nixpkgs;
    dev_env = bundle.env.dev;
  };
in
  bundle // {inherit build_bundle dev_shell publish;}
