#include <AccelStepper.h>
#include <MultiStepper.h>
#include <Servo.h>


// Configuration
const long STEPS_PER_REV[6] = {
  (long)(200*16*6.13),
  (long)(200*16*7.5),
  (long)(200*16*7.5),
  (long)(200*16*1),
  (long)(200*16*1),
  (long)(200*16*1)
}; // full * microsteps * gearing

const int STEPPERS_REVERSE[6] = {1, -1, -1, 1, -1, 1}; // [-1, 1] only
const float STEPPERS_MAX_SPEED = 6000;
const float STEPPERS_MIN_SPEED = 400;
const float STEPPERS_ACCELERATION = 50; // in steps per second squared
const bool SHORTEST_PATH = true;

// AccelStepper(type, stepPin, dirPin);
AccelStepper stepper1(AccelStepper::DRIVER, 22, 23);
AccelStepper stepper2(AccelStepper::DRIVER, 24, 25);
AccelStepper stepper3(AccelStepper::DRIVER, 26, 27);

MultiStepper steppers;

Servo servo4, servo5, servo6;
int SERVO_PINS[6] = { 0, 0, 0, 4, 5, 6 };


// a[deg1, deg2, deg3, deg4, deg5, deg6, time (s)
double a[7];
long steps[6], lastSteps[6], pos[3];

void setup() {
  Serial.begin(9600);
  
  // Set max speed
  a[6] = 1;
  stepper1.setMaxSpeed(STEPPERS_MAX_SPEED);
  stepper2.setMaxSpeed(STEPPERS_MAX_SPEED);
  stepper3.setMaxSpeed(STEPPERS_MAX_SPEED);

  // Set acceleration
  stepper1.setAcceleration(STEPPERS_ACCELERATION);
  stepper2.setAcceleration(STEPPERS_ACCELERATION);
  stepper3.setAcceleration(STEPPERS_ACCELERATION);

  // Add to multistepper
  steppers.addStepper(stepper1);
  steppers.addStepper(stepper2);
  steppers.addStepper(stepper3);

  // Initialize servos
  servo4.attach(SERVO_PINS[3]);
  servo5.attach(SERVO_PINS[4]);
  servo6.attach(SERVO_PINS[5]);
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

	  moveServos();
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

  // holdServos();

}



// Functions
// Steppers
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
  for (int i=0; i<3; i++) {
    lastSteps[i] = steps[i];
  }

  Serial.print("pos: ");
  for (int i=0; i<3; i++) {
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
}

void setSpeed() {

  long maxStep = 0;
  for (int i=0; i<3; i++) {
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
}

void resetPosition() {
  stepper1.setCurrentPosition(steps[0]);
  stepper2.setCurrentPosition(steps[1]);
  stepper3.setCurrentPosition(steps[2]);
}

void setAcceleration(long acc) {
  Serial.println("Set Acceleration: "+String(acc));

  // Set acceleration
  stepper1.setAcceleration(acc);
  stepper2.setAcceleration(acc);
  stepper3.setAcceleration(acc);
}

double stepsToDeg(long steps, long stepsPerRev) {
  return steps / stepsPerRev * 360;
}

long degToSteps(double deg, long stepsPerRev) {
  return deg / 360 * stepsPerRev;
}


// Servos

int servoPos[6];
int servoPW[6]; // 0-180
int SERVO_N[6] = { 0, 0, 0, 90, 90, 90 };
float SERVO_MAX_DPS[6] = { 0, 0, 0, 450, 380, 400 }; // Degrees per second

void moveServos() {
  
  for (int i=3; i<6; i++) {
    float DPS = (a[i] - servoPos[i]) / a[6];
    int PW = 90 * DPS / SERVO_MAX_DPS[i];
    servoPW[i] = SERVO_N[i] + PW * STEPPERS_REVERSE[i];
    servoPW[i] = min(180, max(servoPW[i], 0));

    servoPos[i] = a[i];

    Serial.print("DPS: "+String(DPS));
    Serial.print(" | PW: "+String(PW));
    Serial.println(" | servoPW: "+String(servoPW[i]));
  }
  
  servo4.write( servoPW[3] );
  servo5.write( servoPW[4] );
  servo6.write( servoPW[5] );

  delay( a[6]*1000 );

  servo4.write( SERVO_N[3] );
  servo5.write( SERVO_N[4] );
  servo6.write( SERVO_N[5] );

}

void holdServos() {

  servo4.write( SERVO_N[3] );
  servo5.write( SERVO_N[4] );
  servo6.write( SERVO_N[5] );

}

