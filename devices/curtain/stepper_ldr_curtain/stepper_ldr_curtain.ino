// 28BYJ-48 스텝모터와 LDR(조도센서) 기반 자동 커튼 제어
#include <Stepper.h>

class CurtainController {
public:
  CurtainController(
    int motorPin1,
    int motorPin2,
    int motorPin3,
    int motorPin4,
    int lightSensorPin,
    int lightThreshold,
    long fullOpenSteps,
    int motorRpm
  )
    : stepsPerRevolution(2048),
      stepper(stepsPerRevolution, motorPin1, motorPin2, motorPin3, motorPin4),
      ldrPin(lightSensorPin),
      threshold(lightThreshold),
      curtainMaxSteps(fullOpenSteps),
      currentStep(0),
      motorDirection(0),
      lastTelemetryTime(0),
      motorSpeedRpm(motorRpm),
      controlMode(MODE_AUTO),
      targetStep(0),
      targetActive(false),
      commandIndex(0) {
  }

  void begin() {
    Serial.begin(9600);
    pinMode(ldrPin, INPUT);
    stepper.setSpeed(motorSpeedRpm);
  }

  void update() {
    processSerialInput();

    unsigned long now = millis();
    if (now - lastTelemetryTime >= 3000) {
      int lightValue = analogRead(ldrPin);
      lastTelemetryTime = now;
      emitTelemetry(lightValue);
      if (controlMode == MODE_AUTO && !targetActive) {
        applyAutoLogic(lightValue);
      }
    }

    if (motorDirection == 1 && currentStep < curtainMaxSteps) {
      stepper.setSpeed(motorSpeedRpm);
      stepper.step(1);
      currentStep++;
    } else if (motorDirection == -1 && currentStep > 0) {
      stepper.setSpeed(motorSpeedRpm);
      stepper.step(-1);
      currentStep--;
    }

    if ((motorDirection == 1 && currentStep >= curtainMaxSteps) ||
        (motorDirection == -1 && currentStep <= 0)) {
      if (targetActive) {
        targetActive = false;
        sendError("LIMIT");
      }
      motorDirection = 0;
    }

    updateTargetTracking();
    delay(5);
  }

private:
  enum ControlMode { MODE_AUTO, MODE_MANUAL };

  void processSerialInput() {
    while (Serial.available()) {
      char incoming = Serial.read();
      if (incoming == '\r') {
        continue;
      }
      if (incoming == '\n') {
        if (commandIndex > 0) {
          commandBuffer[commandIndex] = '\0';
          handleFrame(String(commandBuffer));
          commandIndex = 0;
        }
        continue;
      }

      if (commandIndex < sizeof(commandBuffer) - 1) {
        commandBuffer[commandIndex++] = incoming;
      }
    }
  }

  void handleFrame(const String& frameRaw) {
    String frame = frameRaw;
    frame.trim();
    int firstComma = frame.indexOf(',');
    if (firstComma == -1) {
      sendError("FORMAT");
      return;
    }

    String typeToken = frame.substring(0, firstComma);
    typeToken.trim();
    typeToken.toUpperCase();
    if (typeToken != "CMO") {
      return;  // only handle PC-originated commands
    }

    int secondComma = frame.indexOf(',', firstComma + 1);
    if (secondComma == -1) {
      sendError("FORMAT");
      return;
    }

    String metric = frame.substring(firstComma + 1, secondComma);
    metric.trim();
    String value = frame.substring(secondComma + 1);
    value.trim();
    if (metric.length() == 0 || value.length() == 0) {
      sendError("FORMAT");
      return;
    }

    String metricUpper = metric;
    metricUpper.toUpperCase();
    String valueUpper = value;
    valueUpper.toUpperCase();

    if (metricUpper == "MOTOR") {
      handleMotorCommand(valueUpper);
    } else if (metricUpper == "TARGET") {
      handleTargetCommand(value);
    } else if (metricUpper == "MODE") {
      handleModeCommand(valueUpper);
    } else if (metricUpper == "THRESHOLD") {
      handleThresholdCommand(value);
    } else if (metricUpper == "CALIB") {
      handleCalibrationCommand(valueUpper);
    } else {
      sendError("UNKNOWN");
    }
  }

  void handleMotorCommand(const String& valueUpper) {
    controlMode = MODE_MANUAL;
    targetActive = false;

    if (valueUpper == "OPEN") {
      if (setMotorDirection(1)) {
        sendAck("MOTOR", "OPEN");
      }
    } else if (valueUpper == "CLOSE") {
      if (setMotorDirection(-1)) {
        sendAck("MOTOR", "CLOSE");
      }
    } else if (valueUpper == "STOP") {
      setMotorDirection(0);
      sendAck("MOTOR", "STOP");
    } else {
      sendError("UNKNOWN");
    }
  }

  void handleTargetCommand(const String& literalValue) {
    bool ok = false;
    long desiredStep = parseStepTarget(literalValue, ok);
    if (!ok) {
      sendError("LIMIT");
      return;
    }

    controlMode = MODE_MANUAL;
    targetStep = desiredStep;

    if (abs(currentStep - targetStep) <= targetTolerance) {
      targetActive = false;
      setMotorDirection(0);
      sendAck("TARGET", "REACHED");
      return;
    }

    targetActive = true;
    bool applied = false;
    if (targetStep > currentStep) {
      applied = setMotorDirection(1);
    } else {
      applied = setMotorDirection(-1);
    }

    if (!applied) {
      targetActive = false;
      sendAck("TARGET", "FAIL");
    }

    // TARGET 명령은 완료 시점에만 ACK를 보냄 (REACHED/FAIL)
  }

  void handleModeCommand(const String& valueUpper) {
    if (valueUpper == "AUTO") {
      controlMode = MODE_AUTO;
      targetActive = false;
      setMotorDirection(0);
    } else if (valueUpper == "MANUAL") {
      controlMode = MODE_MANUAL;
      targetActive = false;
      setMotorDirection(0);
    } else {
      sendError("UNKNOWN");
    }
  }

  void handleThresholdCommand(const String& literalValue) {
    if (literalValue.length() == 0) {
      sendError("LIMIT");
      return;
    }

    int newThreshold = literalValue.toInt();
    if (newThreshold <= 0) {
      sendError("LIMIT");
      return;
    }

    threshold = newThreshold;
  }

  void handleCalibrationCommand(const String& valueUpper) {
    if (valueUpper == "ZERO") {
      currentStep = 0;
      targetActive = false;
      setMotorDirection(0);
      sendAck("CALIB", "DONE");
    } else {
      sendError("UNKNOWN");
    }
  }

  void emitTelemetry(int lightValue) {
    sendFrame("SEN", "LIGHT", String(lightValue));
    sendFrame("SEN", "CUR_STEP", currentStep);
    sendFrame("SEN", "MOTOR_DIR", motorDirection);
  }

  void applyAutoLogic(int lightValue) {
    if (lightValue > threshold && currentStep < curtainMaxSteps) {
      motorDirection = 1;
    } else if (lightValue < threshold && currentStep > 0) {
      motorDirection = -1;
    } else {
      motorDirection = 0;
    }
  }

  void updateTargetTracking() {
    if (!targetActive) {
      return;
    }

    if (labs(currentStep - targetStep) <= targetTolerance) {
      targetActive = false;
      setMotorDirection(0);
      sendAck("TARGET", "REACHED");
      return;
    }

    if ((motorDirection == 1 && currentStep >= curtainMaxSteps) ||
        (motorDirection == -1 && currentStep <= 0)) {
      targetActive = false;
      sendAck("TARGET", "FAIL");
      sendError("LIMIT");
    }
  }

  long parseStepTarget(const String& literalValue, bool& ok) {
    ok = false;
    if (literalValue.length() == 0) {
      return 0;
    }

    if (literalValue.indexOf('%') != -1) {
      String percentText = literalValue;
      percentText.replace("%", "");
      float percent = percentText.toFloat();
      if (percent < 0.0 || percent > 100.0) {
        return 0;
      }
      ok = true;
      return static_cast<long>((percent / 100.0f) * curtainMaxSteps);
    }

    long absolute = literalValue.toInt();
    if (absolute < 0 || absolute > curtainMaxSteps) {
      return 0;
    }
    ok = true;
    return absolute;
  }

  bool setMotorDirection(int direction) {
    if (direction > 0 && currentStep >= curtainMaxSteps) {
      motorDirection = 0;
      sendError("LIMIT");
      return false;
    }
    if (direction < 0 && currentStep <= 0) {
      motorDirection = 0;
      sendError("LIMIT");
      return false;
    }

    motorDirection = direction;
    return true;
  }

  void sendFrame(const char* dataType, const char* metric, const String& value) {
    Serial.print(dataType);
    Serial.print(",");
    Serial.print(metric);
    Serial.print(",");
    Serial.println(value);
  }

  void sendFrame(const char* dataType, const char* metric, long value) {
    Serial.print(dataType);
    Serial.print(",");
    Serial.print(metric);
    Serial.print(",");
    Serial.println(value);
  }

  void sendAck(const char* metric, const String& value) {
    sendFrame("ACK", metric, value);
  }

  void sendError(const char* code) {
    sendFrame("ACK", "ERROR", String(code));
  }

  const int stepsPerRevolution;
  Stepper stepper;

  const int ldrPin;
  int threshold;
  const long curtainMaxSteps;

  long currentStep;
  int motorDirection;
  unsigned long lastTelemetryTime;
  int motorSpeedRpm;

  ControlMode controlMode;
  long targetStep;
  bool targetActive;
  static constexpr int targetTolerance = 10;

  char commandBuffer[64];
  size_t commandIndex;
};

CurtainController curtainController(
  8,
  10,
  9,
  11,
  A0,
  500,
  1.3L * 2048,
  20
);

void setup() {
  curtainController.begin();
}

void loop() {
  curtainController.update();
}