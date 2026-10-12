#include "greeting.hpp"

std::string make_greeting(const std::string& name) {
    const std::string recipient = name.empty() ? "world" : name;
    return "Hello, " + recipient + "!";
}