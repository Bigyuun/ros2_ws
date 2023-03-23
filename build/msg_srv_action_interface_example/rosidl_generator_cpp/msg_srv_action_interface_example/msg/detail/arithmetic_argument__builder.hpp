// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from msg_srv_action_interface_example:msg/ArithmeticArgument.idl
// generated code does not contain a copyright notice

#ifndef MSG_SRV_ACTION_INTERFACE_EXAMPLE__MSG__DETAIL__ARITHMETIC_ARGUMENT__BUILDER_HPP_
#define MSG_SRV_ACTION_INTERFACE_EXAMPLE__MSG__DETAIL__ARITHMETIC_ARGUMENT__BUILDER_HPP_

#include <algorithm>
#include <utility>

#include "msg_srv_action_interface_example/msg/detail/arithmetic_argument__struct.hpp"
#include "rosidl_runtime_cpp/message_initialization.hpp"


namespace msg_srv_action_interface_example
{

namespace msg
{


}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::msg_srv_action_interface_example::msg::ArithmeticArgument>()
{
  return ::msg_srv_action_interface_example::msg::ArithmeticArgument(rosidl_runtime_cpp::MessageInitialization::ZERO);
}

}  // namespace msg_srv_action_interface_example

#endif  // MSG_SRV_ACTION_INTERFACE_EXAMPLE__MSG__DETAIL__ARITHMETIC_ARGUMENT__BUILDER_HPP_
