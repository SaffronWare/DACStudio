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
    delay(1000 * 120);
  }
if ((i+1) * sizeof(float) < 256)
  {
    IMU.update(); 
    IMU.getAccel(&accelData);
    Serial.println("wow\n");
  
    EEPROM.put((i) * sizeof(float), accelData.accelX);

    Serial.println(accelData.accelX);
    Serial.println("wow\n");
  }
  delay(50);
  i+=1;
}
    Gyroscope0_GyroscopeX = s_GyroX;
    Gyroscope0_GyroscopeY = s_GyroY;
    Gyroscope0_GyroscopeZ = s_GyroZ;

    Gyroscope1_GyroscopeX = s_GyroX;
    Gyroscope1_GyroscopeY = s_GyroY;
    Gyroscope1_GyroscopeZ = s_GyroZ;

    Accelerometer0_AccelerationX = s_AccX;
    Accelerometer0_AccelerationY = s_AccY;
    Accelerometer0_AccelerationZ = s_AccZ;

    s_ServoYaw = Gyroscope0_GyroscopeX;
    s_ServoRoll = Gyroscope1_GyroscopeX;
    s_ServoPitch = Accelerometer0_AccelerationX;
