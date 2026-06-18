{ pkgs, lib, ... }:

{

  packages = [
    pkgs.nlohmann_json
  ];

  # https://devenv.sh/languages/
  languages.python = {
    enable = true;
    uv.enable = true;
  };


  languages.cplusplus.enable = true;

}
