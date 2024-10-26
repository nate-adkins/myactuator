from myactuator.helpers import _BaseMsg, _CanMsgParam


class ReadPIDParamsMsg(_BaseMsg):
    _cmd_byte = 0x30
    _sent_parameters = []
    _received_parameters = [
        _CanMsgParam('current_kp', 2, 1, lambda x: x),
        _CanMsgParam('current_ki', 3, 1, lambda x: x),
        _CanMsgParam('speed_kp', 4, 1, lambda x: x),
        _CanMsgParam('speed_ki', 5, 1, lambda x: x),
        _CanMsgParam('position_kp', 6, 1, lambda x: x),
        _CanMsgParam('position_ki', 7, 1, lambda x: x),
    ]


class WritePIDParamsRAMMsg(_BaseMsg):
    _cmd_byte = 0x31
    _sent_parameters = [
        _CanMsgParam('current_kp', 2, 1, lambda x: x),
        _CanMsgParam('current_ki', 3, 1, lambda x: x),
        _CanMsgParam('speed_kp', 4, 1, lambda x: x),
        _CanMsgParam('speed_ki', 5, 1, lambda x: x),
        _CanMsgParam('position_kp', 6, 1, lambda x: x),
        _CanMsgParam('position_ki', 7, 1, lambda x: x),
    ]
    _received_parameters = _sent_parameters


class WritePIDParamsROMMsg(_BaseMsg):
    _cmd_byte = 0x32
    _sent_parameters = [
        _CanMsgParam('current_kp', 2, 1, lambda x: x),
        _CanMsgParam('current_ki', 3, 1, lambda x: x),
        _CanMsgParam('speed_kp', 4, 1, lambda x: x),
        _CanMsgParam('speed_ki', 5, 1, lambda x: x),
        _CanMsgParam('position_kp', 6, 1, lambda x: x),
        _CanMsgParam('position_ki', 7, 1, lambda x: x),
    ]
    _received_parameters = _sent_parameters


class ReadAccelerationMsg(_BaseMsg):
    _cmd_byte = 0x42
    _sent_parameters = []
    _received_parameters = [
        _CanMsgParam('acceleration', 4, 4, lambda x: x),
    ]


class WriteAccelerationRAMROMMsg(_BaseMsg):
    _cmd_byte = 0x43
    _sent_parameters = [
        _CanMsgParam('func_index', 1, 1, lambda x: x),
        _CanMsgParam('acceleration', 4, 4, lambda x: x),
    ]
    _received_parameters = _sent_parameters


class ReadMultiTurnEncoderPositionMsg(_BaseMsg):
    _cmd_byte = 0x60
    _sent_parameters = []
    _received_parameters = [
        _CanMsgParam('encoder_position', 4, 4, lambda x: x),
    ]


class ReadMultiTurnEncoderOriginalPositionMsg(_BaseMsg):
    _cmd_byte = 0x61
    _sent_parameters = []
    _received_parameters = [
        _CanMsgParam('encoder_original_position', 4, 4, lambda x: x),
    ]


class ReadMultiTurnEncoderZeroOffsetMsg(_BaseMsg):
    _cmd_byte = 0x62
    _sent_parameters = []
    _received_parameters = [
        _CanMsgParam('encoder_zero_offset', 4, 4, lambda x: x),
    ]


class WriteEncoderMultiTurnZeroMsg(_BaseMsg):
    _cmd_byte = 0x63
    _sent_parameters = [
        _CanMsgParam('encoder_zero_offset', 4, 4, lambda x: x),
    ]
    _received_parameters = _sent_parameters


class WriteCurrentMultiTurnZeroMsg(_BaseMsg):
    _cmd_byte = 0x64
    _sent_parameters = []
    _sent_parameters = [
        _CanMsgParam('encoder_zero_offset', 4, 4, lambda x: x),
    ]


class ReadSingleTurnEncoderMsg(_BaseMsg):
    _cmd_byte = 0x90
    _sent_parameters = []
    _received_parameters = [
        _CanMsgParam('encoder_position', 2, 2, lambda x: x),
        _CanMsgParam('encoder_original_position', 4, 2, lambda x: x),
        _CanMsgParam('encoder_zero_offset', 6, 2, lambda x: x),
    ]


class ReadMultiTurnAngleMsg(_BaseMsg):
    _cmd_byte = 0x92
    _sent_parameters = []
    _received_parameters = [
        _CanMsgParam('multi_turn_angle', 4, 4, lambda x: x/100),
    ]


class ReadSingleTurnAngleMsg(_BaseMsg):
    # starting from the zero point of the encoder, increasing clockwise
    _cmd_byte = 0x94
    _sent_parameters = []
    _received_parameters = [
        _CanMsgParam('single_turn_angle', 6, 2, lambda x: x/100),
    ]


class ReadMotorStatus1Msg(_BaseMsg):
    # can have multiples
    error_statuses = {
        0x0002: 'Motor stall',
        0x0004: 'low pressure',
        0x0008: 'overvoltage',
        0x0010: 'overcurrent',
        0x0040: 'Power overrun',
        0x0080: 'Calibration parameter writing error',
        0x0100: 'speeding',
        0x1000: 'Motor temperature over temperature',
        0x2000: 'Encoder calibration error',
    }
    _cmd_byte = 0x9A
    _sent_parameters = []
    _received_parameters = [
        _CanMsgParam('motor_temperature_c', 1, 1, lambda x: x),
        _CanMsgParam('MOS_temperature', 2, 1, lambda x: x),
        _CanMsgParam('break_state', 3, 1, lambda x: x),
        _CanMsgParam('voltage_volts', 4, 2, lambda x: x),
        _CanMsgParam('error_status', 6, 2, lambda x: x),
    ]


class ReadMotorStatus2Msg(_BaseMsg):
    _cmd_byte = 0x9C
    _sent_parameters = []
    _received_parameters = [
        _CanMsgParam('motor_temperature_c', 1, 1, lambda x: x),
        _CanMsgParam('current_amps', 2, 2, lambda x: x/100),
        _CanMsgParam('speed_dps', 4, 2, lambda x: x),
        _CanMsgParam('angle_degrees', 6, 2, lambda x: x),
    ]


class ReadMotorStatus3Msg(_BaseMsg):
    _cmd_byte = 0x9D
    _sent_parameters = []
    _received_parameters = [
        _CanMsgParam('motor_temperature_c', 1, 1, lambda x: x),
        _CanMsgParam('phase_a_current_amps', 2, 2, lambda x: x/100),
        _CanMsgParam('phase_b_current_amps', 4, 2, lambda x: x/100),
        _CanMsgParam('phase_c_current_amps', 6, 2, lambda x: x/100),
    ]


class MotorShutdownMsg(_BaseMsg):
    # turns of motor and clears running state
    _cmd_byte = 0x80
    _sent_parameters = []
    _received_parameters = []


class MotorStopMsg(_BaseMsg):
    # just stops close-loop movement
    _cmd_byte = 0x81
    _sent_parameters = []
    _received_parameters = []


class TorqueClosedLoopControlMsg(_BaseMsg):
    _cmd_byte = 0xA1
    _sent_parameters = [
        _CanMsgParam('torque_current_amps', 1, 1, lambda x: x*100),
    ]
    _received_parameters = [
        _CanMsgParam('motor_temperature_c', 1, 1, lambda x: x),
        _CanMsgParam('current_amps', 2, 2, lambda x: x/100),
        _CanMsgParam('speed_dps', 4, 2, lambda x: x),
        _CanMsgParam('angle_degrees', 6, 2, lambda x: x),
    ]


class SpeedClosedLoopControlMsg(_BaseMsg):
    # max of 65535
    _cmd_byte = 0xA2
    _sent_parameters = [
        _CanMsgParam('speed_dps', 4, 4, lambda x: x*100),
    ]
    _received_parameters = [
        _CanMsgParam('motor_temperature_c', 1, 1, lambda x: x),
        _CanMsgParam('current_amps', 2, 2, lambda x: x/100),
        _CanMsgParam('speed_dps', 4, 2, lambda x: x),
        _CanMsgParam('angle_degrees', 6, 2, lambda x: x),
    ]


class AbsolutePositionClosedLoopControlMsg(_BaseMsg):
    _cmd_byte = 0xA4
    _sent_parameters = [
        _CanMsgParam('speed_limit_dps', 2, 2, lambda x: x),
        _CanMsgParam('goal_angle_degrees', 4, 4, lambda x: x*100),
    ]
    _received_parameters = [
        _CanMsgParam('motor_temperature_c', 1, 1, lambda x: x),
        _CanMsgParam('current_amps', 2, 2, lambda x: x/100),
        _CanMsgParam('speed_dps', 4, 2, lambda x: x),
        _CanMsgParam('angle_degrees', 6, 2, lambda x: x),
    ]


class SingleTurnPositionControlMsg(_BaseMsg):
    rotation_directions = {
        'cw': 0x00,
        'ccw': 0x01,
    }
    _cmd_byte = 0xA6
    _sent_parameters = [
        _CanMsgParam('rotation_direction', 1, 1, lambda x: x),
        _CanMsgParam('speed_limit_dps', 2, 2, lambda x: x),
        _CanMsgParam('goal_angle_degrees', 4, 2, lambda x: x*100),
    ]
    _received_parameters = [
        _CanMsgParam('motor_temperature_c', 1, 1, lambda x: x),
        _CanMsgParam('current_amps', 2, 2, lambda x: x/100),
        _CanMsgParam('speed_dps', 4, 2, lambda x: x),
        _CanMsgParam('angle_degrees', 6, 2, lambda x: x),
    ]


class IncrementalPositionClosedLoopControlMsg(_BaseMsg):
    _cmd_byte = 0xA8
    _sent_parameters = [
        _CanMsgParam('speed_limit_dps', 2, 2, lambda x: x),
        _CanMsgParam('goal_angle_degrees', 4, 4, lambda x: x*100),
    ]
    _received_parameters = [
        _CanMsgParam('motor_temperature_c', 1, 1, lambda x: x),
        _CanMsgParam('current_amps', 2, 2, lambda x: x/100),
        _CanMsgParam('speed_dps', 4, 2, lambda x: x),
        _CanMsgParam('angle_degrees', 6, 2, lambda x: x),
    ]


class SystemOperatingModeAcquisitionMsg(_BaseMsg):
    operating_modes = {
        'current_loop_control': 0x01,
        'speed_loop_control': 0x02,
        'position_loop_control': 0x03,
    }
    _cmd_byte = 0x70
    _sent_parameters = []
    _received_parameters = [
        _CanMsgParam('operating_mode', 7, 1, lambda x: x),
    ]


class MotorPowerAcquisitionMsg(_BaseMsg):
    _cmd_byte = 0x71
    _sent_parameters = []
    _received_parameters = [
        _CanMsgParam('motor_power_watts', 6, 2, lambda x: x/10),
    ]


class SystemResetMsg(_BaseMsg):
    # reset the system program ??
    _cmd_byte = 0x76
    _sent_parameters = []
    _received_parameters = []


class SystemBrakeReleaseMsg(_BaseMsg):
    # The system will release the holding brake, and the motor will be in a movable state without being restricted by the holding brake.
    _cmd_byte = 0x77
    _sent_parameters = []
    _received_parameters = []


class SystemBrakeLockMsg(_BaseMsg):
    # The holding brake locks the motor and the motor can no longer run. The holding brake is also in this state after the system is powered off.
    _cmd_byte = 0x78
    _sent_parameters = []
    _received_parameters = []


class SystemRuntimeReadMsg(_BaseMsg):
    _cmd_byte = 0xB1
    _sent_parameters = []
    _received_parameters = [
        _CanMsgParam('system_runtime_secs', 4, 4, lambda x: x/1000),
    ]


class SystemSoftwareVersionDateReadMsg(_BaseMsg):
    _cmd_byte = 0xB2
    _sent_parameters = []
    _received_parameters = [
        _CanMsgParam('software_version_date', 4, 4, lambda x: x),
    ]


class CommunicationInterruptionProtectionTimeSettingMsg(_BaseMsg):
    # time between communication interrupted and brake enabling
    _cmd_byte = 0xB3
    _sent_parameters = [
        _CanMsgParam('recieve_time_ms', 4, 4, lambda x: x),
    ]
    _received_parameters = _sent_parameters


class CommunicationBaudRateSettingMsg(_BaseMsg):
    serial_baudrates = {
        '115200': 0,
        '500000': 1,
        '1000000': 2,
        '1500000': 3,
        '2500000': 4,
    }
    can_baudrates = {
        '500000': 0,
        '1000000': 1,
    }
    _cmd_byte = 0xB4
    _sent_parameters = [
        _CanMsgParam('baudrate', 4, 4, lambda x: x),
    ]
    _received_parameters = []


class MotorModelReadingMsg(_BaseMsg):
    _cmd_byte = 0x90
    _sent_parameters = []
    _received_parameters = []
# class ActiveReplyFunctionMsg(_BaseMsg):
#
#
#         _cmd_byte = 0x91
#         _sent_parameters = []
#         _received_parameters = []
# class FunctionControlMsg(_BaseMsg):
#
#
#         _cmd_byte = 0x92
#         _sent_parameters = []
#         _received_parameters = []
# class MultiMotorCommandMsg(_BaseMsg):
#
#
#         _cmd_byte = 0x93
#         _sent_parameters = []
#         _received_parameters = []


class CANIDSettingMsg(_BaseMsg):
    # can_id parameter should be 0 if reading an id
    read_write_flags = {
        'read': 0,
        'write': 1,
    }
    _cmd_byte = 0x94
    _sent_parameters = [
        _CanMsgParam('read_write_flag', 2, 1, lambda x: x),
        _CanMsgParam('can_id', 7, 1, lambda x: x),
    ]
    _received_parameters = [
        _CanMsgParam('read_write_flag', 2, 1, lambda x: x),
        _CanMsgParam('can_id', 6, 2, lambda x: x),
    ]
# class MotionModeControlMsg(_BaseMsg):
#
#
#         _cmd_byte = 0x95
#         _sent_parameters = []
#         _received_parameters = []
# class RS485MultiMotorCommandMsg(_BaseMsg):
#
#
#         _cmd_byte = 0x96
#         _sent_parameters = []
#         _received_parameters = []
# class RS485IDSettingMsg(_BaseMsg):
#
#
#         _cmd_byte = 0x97
#         _sent_parameters = ['rs485_id']
#         _received_parameters = []
