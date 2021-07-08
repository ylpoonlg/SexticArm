#include <AccelStepper.h>
#include <MultiStepper.h>


// Configuration
const long STEPS_PER_REV[6] = {
  (long)(200*16*6.13),
  (long)(200*16*7.69),
  (long)(200*16*7.69),
  (long)(200*16*1),
  (long)(200*16*1),
  (long)(200*16*1)
}; // full * microsteps * gearing

const int STEPPERS_REVERSE[6] = {1, -1, -1, -1, -1, 1}; // [-1, 1] only
const float STEPPERS_MAX_SPEED = 6000;
const float STEPPERS_MIN_SPEED = 400;
const float STEPPERS_ACCELERATION = 50; // in steps per second squared
const bool SHORTEST_PATH = true;


// AccelStepper(type, stepPin, dirPin);
AccelStepper stepper1(AccelStepper::DRIVER, 22, 23);
AccelStepper stepper2(AccelStepper::DRIVER, 24, 25);
AccelStepper stepper3(AccelStepper::DRIVER, 26, 27);
AccelStepper stepper4(AccelStepper::DRIVER, 28, 29);
AccelStepper stepper5(AccelStepper::DRIVER, 30, 31);
AccelStepper stepper6(AccelStepper::DRIVER, 32, 33);



MultiStepper steppers;

// a[deg1, deg2, deg3, deg4, deg5, deg6, time (s)
double a[7];
long steps[6], lastSteps[6], pos[6];

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



// Main
void loop() {

  if (Serial.available()) {
        String cmd = Serial.readString();
        
        if (cmd.charAt(0) == 'M') { // move
          getAngles(cmd);
          getSteps();
          setSpeed();

          steppers.moveTo(pos);
          steppers.runSpeedToPosition();

          if (SHORTEST_PATH)
            resetPosition();
        } else if (cmd.charAt(0) == 'A') { // acceleration
          String tmp = "";
          long acc = STEPPERS_ACCELERATION;
          for (int i=2; i<cmd.length(); i++) {
            char ch = cmd.charAt(i);
            if (ch == ' ' || ch == '\n') {
              acc = tmp.toInt();
              break;
            } else {
              tmp += ch;
            }
          }
          setAcceleration(acc);
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
  // reset last steps
  for (int i=0; i<6; i++) {
    lastSteps[i] = steps[i];
  }

  Serial.print("pos: ");
  for (int i=0; i<6; i++) {
    steps[i] = STEPS_PER_REV[i] * a[i] / 360 * STEPPERS_REVERSE[i];
    pos[i] = steps[i];

    if (SHORTEST_PATH) {
      if (abs( lastSteps[i] + degToSteps(360, STEPS_PER_REV[i]) - steps[i] ) < degToSteps(180, STEPS_PER_REV[i])) {
        pos[i] -= degToSteps(360, STEPS_PER_REV[i]);
      } else if (abs( steps[i] + degToSteps(360, STEPS_PER_REV[i]) -  lastSteps[i]) < degToSteps(180, STEPS_PER_REV[i])) {
        pos[i] += degToSteps(360, STEPS_PER_REV[i]);
      }
    }

    Serial.print(pos[i]);
    Serial.print(", ");
  }
  Serial.println();
  Serial.println();


  Serial.println("Steps[0]: "+String(steps[0]));
  Serial.println("Pos[0]: "+String(pos[0]));
  Serial.println("Last[0]: "+String(lastSteps[0]));
  Serial.println();
}

void setSpeed() {
  Serial.print("time: ");
  Serial.println(a[6]);

  long maxStep = 0;
  for (int i=0; i<6; i++) {
    maxStep = max( maxStep, abs(pos[i] - lastSteps[i]) );
  }

  Serial.print("maxStep: ");
  Serial.println(maxStep);

  float stepsPerSecond = max(STEPPERS_MIN_SPEED, min(maxStep / a[6], STEPPERS_MAX_SPEED));

  Serial.print("maxSpeed: ");
  Serial.println(stepsPerSecond);
  Serial.println();

  stepper1.setMaxSpeed(stepsPerSecond);
  stepper2.setMaxSpeed(stepsPerSecond);
  stepper3.setMaxSpeed(stepsPerSecond);
  stepper4.setMaxSpeed(stepsPerSecond);
  stepper5.setMaxSpeed(stepsPerSecond);
  stepper6.setMaxSpeed(stepsPerSecond);
}

void resetPosition() {
  stepper1.setCurrentPosition(steps[0]);
  stepper2.setCurrentPosition(steps[1]);
  stepper3.setCurrentPosition(steps[2]);
  stepper4.setCurrentPosition(steps[3]);
  stepper5.setCurrentPosition(steps[4]);
  stepper6.setCurrentPosition(steps[5]);

  Serial.print("stepper1.curPos: ");
  Serial.println(stepper1.currentPosition());
  Serial.print("stepper2.curPos: ");
  Serial.println(stepper2.currentPosition());
  Serial.println();
}

void setAcceleration(long acc) {
  Serial.println("Set Acceleration: "+String(acc));

  // Set acceleration
  stepper1.setAcceleration(acc);
  stepper2.setAcceleration(acc);
  stepper4.setAcceleration(acc);
  stepper5.setAcceleration(acc);
  stepper6.setAcceleration(acc);
  stepper3.setAcceleration(acc);
}

double stepsToDeg(long steps, long stepsPerRev) {
  return steps / stepsPerRev * 360;
}

long degToSteps(double deg, long stepsPerRev) {
  return deg / 360 * stepsPerRev;
}