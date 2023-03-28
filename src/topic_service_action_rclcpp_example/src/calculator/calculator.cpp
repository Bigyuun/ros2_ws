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
          this->get_logger(),
          "Timestamp of the message : sec %ld nanosec %ld",
          msg->stamp.sec,
          msg->stamp.nanosec);

        RCLCPP_INFO(this->get_logger(), "Subscribed argument a : %.2f", argument_a_);
        RCLCPP_INFO(this->get_logger(), "Subscribed argument b : %.2f", argument_b_);
      }
    );

  /*********************************
   * @author DY
   * @brief Service Server part
   *********************************/
  auto get_arithmetic_operator = 
  [this](
  const std::shared_ptr<ArithmeticOperator::Request> request,
  std::shared_ptr<ArithmeticOperator::Response> response) -> void
  {
    argument_operator_ = request->arithmetic_operator;
    argument_result_ = this->calculate_given_formula(argument_a_, argument_b_, argument_operator_);
    response->artimetic_result = argument_result_;

    std::ostringstream oss;
    oss << std::to_string(argument_a_) << ' ' <<
           operator_[argument_operator_-1] << ' ' <<
           std::to_string(argument_b_) << ' = ' <<
           argument_result_ << std::endl;
    argument_formula_ = oss.str();

    RCLCPP_INFO(
      this-> get_logger(),
      "%s",
      argument_formula_.c_str());
  };

  // create service_server
  arithmetic_service_server_ = 
  //this->create_service<ArithmeticOperator>("arithmetic_operator", get_arithmetic_operator);
    create_service<ArithmeticOperator>("arithmetic_operator", get_arithmetic_operator);

  /*********************************
   * @author DY
   * @brief Action Server part
   *********************************/
  arithmetic_action_server_ = 
    rclcpp_action::Client<ArithmeticChecker>();

}

Calculator::~Calculator()
{
  
}


float Calculator::calculate_given_formula(
  const float & a,
  const float & b,
  const int8_t & operators)
{
  float result = 0.0;
  ArithmeticOperator::Request arithmetic_operator;

  if     (operators == arithmetic_operator.PLUS)    {result = a+b;}
  else if(operators == arithmetic_operator.MINUS)   {result = a-b;}
  else if(operators == arithmetic_operator.MULTIPLY){result = a*b;}
  else if(operators == arithmetic_operator.DIVISION){result = a/b;}
  else{
    RCLCPP_ERROR(
      this->get_logger(),
      "Please make sure arithmetic operator(PLUS, MINUS, MULTIPLY, DIVISION).");
    result = 0.0;
  }

  return result;
}

 














