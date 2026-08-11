X_MAPS_TO = 0;
Y_MAPS_TO = 0;
Z_MAPS_TO = 0;
SERVO_YAW_PIN = 0;
SERVO_PITCH_PIN = 0;
SERVO_ROLL_PIN = 0;
DELAY_BEFORE_START_RECORDING_IN_SECONDS = 0;
SHOULD_RECORD_DATA = 1;

#include "FastIMU.h"
#include <Wire.h>
#include <EEPROM.h>

// This relies on the FastIMU library caught  from https://github.com/LiquidCGS/FastIMU/blob/main/examples/Calibrated_sensor_output/Calibrated_sensor_output.ino

MPU6500 IMU;
AccelData accelData;
GyroData gyroData;
calData calib = { 0 };

void setup()
{
  Wire.begin();
  Wire.setClock(400000);
  Serial.begin(115200);
  while (!Serial)
  {
    ;
  }

  int err = IMU.init(calib, 0x68);
  if (err != 0) {
    Serial.print("Error initializing IMU: ");
    Serial.println(err);
    while (true) {
      ;
    }
  }

  if (err != 0) {
    Serial.print("Error Setting range: ");
    Serial.println(err);
    while (true) {
      ;
    }
  }
}

int i = 0;
void loop()
{
  if (i == 0)
  {
    delay(10000 * 0);

    IMU.update(); 
    IMU.getAccel(&accelData);
    Serial.println("wow\n");

    

    Gyroscope0_GyroscopeX = s_GyroX;
    Gyroscope0_GyroscopeY = s_GyroY;
    Gyroscope0_GyroscopeZ = s_GyroZ;

    Accelerometer0_AccelerationX = s_AccX;
    Accelerometer0_AccelerationY = s_AccY;
    Accelerometer0_AccelerationZ = s_AccZ;

    s_ServoYaw = Gyroscope0_GyroscopeX;
    s_ServoRoll = Accelerometer0_AccelerationX;
    s_ServoPitch = Accelerometer0_AccelerationZ;
