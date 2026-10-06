OPENQASM 3.0;
include "stdgates.inc";
qubit[5] q;
bit release;
bit out;
// Structural reference. Target support for control flow and reset must be checked before submission.
ctrl @ ctrl @ x q[0], q[1], q[3];
ctrl @ ctrl @ x q[3], q[2], q[4];
h q[3];
release = measure q[3];
if (release == 1) {
  cz q[0], q[1];
}
reset q[3];
out = measure q[4];
