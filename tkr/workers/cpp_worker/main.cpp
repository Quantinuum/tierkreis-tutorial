#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <numeric>
#include <nlohmann/json.hpp>

static const std::string CHECKPOINTS_DIRECTORY = std::string(std::getenv("HOME")) + "/.tierkreis/checkpoints/";

// Use the nlohmann namespace for JSON parsing
using json = nlohmann::json;

struct Ansatz {
    float a;
    float b;
    float c;
};

void print_usage(const char *prog_name)
{
  std::cout << "Usage: " << prog_name << " <path_to_config.json>" << std::endl;
}

void parse_json(const std::string &call_args_path, json &call_args)
{
  std::ifstream call_args_file(call_args_path);
  if (!call_args_file.is_open()) // check if open is necessary for << syntax
  {
    std::cerr << "Error: Could not open configuration file: " << call_args_path << std::endl;
    return;
  }
  try
  {
    call_args = json::parse(call_args_file);
  }
  catch (json::parse_error &e)
  {
    std::cerr << "Error: JSON parsing failed: " << e.what() << std::endl;
    return;
  }
  call_args_file.close();
}

void parse_input(const json &call_args, std::string &input_data)
{
  json inputs = call_args["inputs"];
  std::cout << inputs << std::endl;
  for (auto &[key, path] : inputs.items())
  {
    if (key != "value")
      continue; // we only want to load value

    auto abs_path = CHECKPOINTS_DIRECTORY + path.template get<std::string>();
    std::cout << "parsing input: " << key << " at: " << abs_path << std::endl;
    json data;
    parse_json(abs_path, data);
    std::cout << "Read data" << data << std::endl;
    auto tmp = data.template get<std::string>();
    input_data = tmp;
  }
}

void write_output(const json &call_args, const Ansatz &output)
{

  json outputs = call_args["outputs"];
  for (auto &[key, path] : outputs.items())
  {
    if (key != "value")
      continue; // we only want to write value
    std::cout << "writing output: " << key << " at: " << path << std::endl;
    auto out_path = CHECKPOINTS_DIRECTORY + path.template get<std::string>();
    std::ofstream output_file(out_path);
    if (!output_file.is_open())
    {
      std::cerr << "Error: Could not open output file for writing: " << out_path << std::endl;
      return;
    }
    json data = {
        {"a", output.a},
        {"b", output.b},
        {"c", output.c}
    };
    output_file << data << std::endl;
    output_file.close();
  }

  auto done_file_path = CHECKPOINTS_DIRECTORY + call_args["done_path"].template get<std::string>();
  std::ofstream done_file(done_file_path);
  if (done_file.is_open())
  {
    done_file.close();
  }
  else
  {
    std::cerr << "Error: Could not create done file at " << done_file_path << std::endl;
  }
}

int main(int argc, char **argv)
{

    json call_args;
    std::string input_data;

    if (argc != 2)
    {
        print_usage(argv[0]);
        return 1;
    }

    // parse worker_call_args
    std::cout << "parsing json" << std::endl;
    parse_json(argv[1], call_args);
    std::cout << "parsing inputs" << std::endl;
    parse_input(call_args, input_data);
  

    // Dummy program
    Ansatz output;
    if (input_data == "JW")
    {
        output = {1.0f, 2.0f, 3.0f};
    }
    else
    {
        output = {0.1f, 0.2f, 0.3f};
    }


  // write to output
  write_output(call_args, output);

  return 0;
}
