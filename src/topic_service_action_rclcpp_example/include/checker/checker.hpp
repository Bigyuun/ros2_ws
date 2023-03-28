#ifndef CHECKER__CHECKER_HPP_
#define CHECKER__CHECKER_HPP_

#include <memory>
#include <string>
#include <utility>

#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "msg_srv_actoin_interface_example/action/arithmetic_checker.hpp"


class Checker : public rclcpp::Node
{
public:
  using ArithmeticChecker = msg_srv_action_interface_example::action::ArithmeticChecker;
  using GoalHandleArithmeticChecker = rclcpp_action::ClientGoalHandle<ArithmeticChecker>;

  explicit Checker(
    float goal_sum,
    const rclcpp::NodeOptions & node_option = rclcpp::NodeOptions());
  virtual ~Checker();

private:
  rclcpp_action::Client<ArithmeticChecker>::SharedPtr arithmetic_action_client_;

  void send_goal_total_sum(float goal_sum);
  void get_arithmetic_action_goal(
    std::shared_future<GoalHandleArithmeticChecker::SharedPtr> future);
  void get_arithmetic_action_feedback(
    GoalHandleArithmeticChecker::SharedPtr,
    const std::shared_ptr<const ArithmeticChecker::Feedback> feedback);
  void get_arithmetic_action_result(
    const GoalHandleArithmeticChecker::WrappedResult & result);
};
#endif  // CHECKER__CHECKER_HPP_