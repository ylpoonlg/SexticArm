#include <AccelStepper.h>
#include <MultiStepper.h>

const long STEPS_PER_REV = 200 * 16; // full * microsteps
const int STEPPERS_REVERSE = -1; // [-1, 1] only

const float STEPPERS_MAX_SPEED = 6000;
const float STEPPERS_MIN_SPEED = 400;
const float STEPPERS_ACCELERATION = 6000;

// AccelStepper(type, stepPin, dirPin);
AccelStepper stepper1(AccelStepper::DRIVER, 22, 23);
AccelStepper stepper2(AccelStepper::DRIVER, 24, 25);
AccelStepper stepper3(AccelStepper::DRIVER, 26, 27);
AccelStepper stepper4(AccelStepper::DRIVER, 28, 29);
AccelStepper stepper5(AccelStepper::DRIVER, 30, 31);
AccelStepper stepper6(AccelStepper::DRIVER, 32, 33);



MultiStepper steppers;

// a[deg1, deg2, deg3, deg4, deg5, deg6, time (s), null, null, null]
double a[10];
long steps[6], lastSteps[6];

void setup() {
  Serial.begin(9600);
  
  // Set max speed
  a[6] = 1;
  stepper1.setMaxSpeed(STEPPERS_MAX_SPEED);
  stepper2.setMaxSpeed(STEPPERS_MAX_SPEED);
  stepper3.setMaxSpeed(STEPPERS_MAX_SPEED);
  stepper4.setMaxSpeed(STEPPERS_MAX_SPEED);
  stepper5.setMaxSpeed(STEPPERS_MAX_SPEED);
  stepper6.setMaxSpeed(STEPPERS_MAX_SPEED);

  // Set acceleration
  stepper1.setAcceleration(STEPPERS_ACCELERATION);
  stepper2.setAcceleration(STEPPERS_ACCELERATION);
  stepper3.setAcceleration(STEPPERS_ACCELERATION);
  stepper4.setAcceleration(STEPPERS_ACCELERATION);
  stepper5.setAcceleration(STEPPERS_ACCELERATION);
  stepper6.setAcceleration(STEPPERS_ACCELERATION);

  // Add to multistepper
  steppers.addStepper(stepper1);
  steppers.addStepper(stepper2);
  steppers.addStepper(stepper3);
  steppers.addStepper(stepper4);
  steppers.addStepper(stepper5);
  steppers.addStepper(stepper6);
}
void loop() {

  if (Serial.available()) {
        String cmd = Serial.readString();
        
        if (cmd.charAt(0) == 'M') { // move
          getAngles(cmd);
          delayMicroseconds(10);
          getSteps();

          steppers.moveTo(steps);
          delayMicroseconds(10);
          setSpeed();
          steppers.runSpeedToPosition();
          
          // reset last steps
          for (int i=0; i<6; i++) {
            lastSteps[i] = steps[i];
          }
        }
  }

}



// Functions
void getAngles(String cmd) {
    int j=0;
    String tmp = "";
    for (int i=2; i<cmd.length(); i++) {
        char ch = cmd.charAt(i);
        if (ch == ' ' || ch == '\n') {
            a[j] = tmp.toDouble();
            j++;
            tmp = "";
        } else {
            tmp += ch;
        }
    }
}

void getSteps() {
  Serial.print("steps: ");

  for (int i=0; i<6; i++) {
    steps[i] = STEPS_PER_REV * a[i] / 360 * STEPPERS_REVERSE;
    Serial.print(steps[i]);
    Serial.print(", ");
  }
  Serial.println();
}

void setSpeed() {
  Serial.print("time: ");
  Serial.println(a[6]);

  long maxStep = 0;
  for (int i=0; i<6; i++) {
    maxStep = max( maxStep, abs(steps[i] - lastSteps[i]) );
  }

  Serial.print("maxStep: ");
  Serial.println(maxStep);

  float stepsPerSecond = max(STEPPERS_MIN_SPEED, min(maxStep / a[6], STEPPERS_MAX_SPEED));

  Serial.print("maxSpeed: ");
  Serial.println(stepsPerSecond);

  stepper1.setMaxSpeed(stepsPerSecond);
  stepper2.setMaxSpeed(stepsPerSecond);
  stepper3.setMaxSpeed(stepsPerSecond);
  stepper4.setMaxSpeed(stepsPerSecond);
  stepper5.setMaxSpeed(stepsPerSecond);
  stepper6.setMaxSpeed(stepsPerSecond);
}