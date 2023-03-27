#pragma once

#include <memory>
#include <sstream>
#include <string>
#include <utility>
#include <vector>
#include <stdexcept>

#include "calculator/calculator.hpp"




Calculator::Calculator(const rclcpp::NodeOptions & node_options)
: Node("calculator", node_options),
  argument_a_(0.0),
  argument_b_(0.0),
  argument_operator_(0),
  argument_result_(0.0),
  argument_fomula_("")
{
  RCLCPP_INFO(get_logger(), "Run calculator");

  operator_.reserve(4);
  operator_.push_back("+");
  operator_.push_back("-");
  operator_.push_back("*");
  operator_.push_back("/");

  this->declare_parameter("qos_depth", 10);
  int8_t qos_depth = this->get_parameter("qos_depth",qos_depth);
  // int8_t qos_depth = this->get_parameter("qos_depth").get_value<int8_t>();


/*********************************
 * @author DY
 * @brief Topic subscriber part
 *********************************/
  const auto QOS_RKL10V = 
    rclcpp::QoS(rclcpp::KeepLast(qos_depth)).reliable().durability_volatile();

  arithmetic_argument_subscriber_ =
    this->create_subscription<ArithmeticArgument>(
      "arithmetic_argument",
      QOS_RKL10V,
      [this](const ArithmeticArgument::SharedPtr msg) -> void
      {
        argument_a_ = msg->argument_a;
        argument_b_ = msg->argument_b;

        RCLCPP_INFO(
          this->get_logger(), "Timestamp of the message : sec %ld nanosec %ld",
          msg->stamp.sec,
          msg->stamp.nanosec);

        RCLCPP_INFO(this->get_logger(), "Subscribed argument a : %.2f", argument_a_);
        RCLCPP_INFO(this->get_logger(), "Subscribed argument b : %.2f", argument_b_);
      }
    );

  auto get_arithmetic_operator = 










}

















