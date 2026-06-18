{ pkgs, lib, ... }:
let
  darwinRuntimeLibraries = with pkgs; [
    libiconv
  ];
  darwinRuntimeLibraryPath = lib.makeLibraryPath darwinRuntimeLibraries;
in
{
 config = {
  packages = [
    pkgs.just
    pkgs.zlib
    pkgs.maturin
    pkgs.bacon
    pkgs.cargo-nextest
    pkgs.sqlite
    pkgs.nlohmann_json
  ] ++ lib.optionals pkgs.stdenv.isDarwin darwinRuntimeLibraries;


  # https://devenv.sh/languages/
  languages.python = {
    enable = true;
    uv.enable = true;
  };


  languages.cplusplus.enable = true;
   enterShell =
    if pkgs.stdenv.isDarwin && pkgs.stdenv.isAarch64 then ''
      unset UV_PYTHON;
      export MATURIN_NO_PROGRESS=1
      export RUST_LOG=error
    '' else ''
      export LD_LIBRARY_PATH=${pkgs.stdenv.cc.cc.lib}/lib:$LD_LIBRARY_PATH
      export MATURIN_NO_PROGRESS=1
      export RUST_LOG=error
    '';
 };
}
