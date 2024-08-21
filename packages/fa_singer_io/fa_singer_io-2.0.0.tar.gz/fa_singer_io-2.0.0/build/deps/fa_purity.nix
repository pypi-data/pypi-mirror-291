{
  lib,
  makes_lib,
  nixpkgs,
  python_pkgs,
  python_version,
}: let
  make_bundle = {
    commit,
    sha256,
  }: let
    raw_src = builtins.fetchTarball {
      inherit sha256;
      url = "https://gitlab.com/dmurciaatfluid/purity/-/archive/${commit}/purity-${commit}.tar";
    };
    src = import "${raw_src}/build/filter.nix" nixpkgs.nix-filter raw_src;
  in
    import "${raw_src}/build" {
      inherit nixpkgs python_version src;
      makesLib = makes_lib;
    };
  bundle = make_bundle {
    # v2.0.0
    commit = "bc2621cb8b330474edc2d36407fc5a7e0b0db09c";
    sha256 = "1cjrjhbypby2s0q456dja3ji3b1f3rfijmbrymk13blxsxavq183";
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
